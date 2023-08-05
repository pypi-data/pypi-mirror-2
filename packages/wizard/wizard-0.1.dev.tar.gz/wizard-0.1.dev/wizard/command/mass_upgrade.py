import logging
import os
import os.path
import itertools
import sys
import shutil
import errno

from wizard import deploy, report, shell, sset, command
from wizard.command import upgrade

def main(argv, baton):
    options, args = parse_args(argv, baton)
    app = args[0]
    sh = shell.ParallelShell.make(options.no_parallelize, options.max_processes)
    command.create_logdir(options.log_dir)
    # setup reports
    human_status = {
        'up_to_date': 'are now up-to-date',
        'not_migrated': 'were not migrated',
        'merge': 'had merge failures',
        'verify': 'had web verification errors',
        'backup_failure': 'had a backup failure',
        'blacklisted': 'were blacklisted',
        'db': 'had database errors',
        'quota': 'had too low quota',
        'permissions': 'had insufficient permissions for upgrade'
    }
    if options.remerge:
        os.unlink(os.path.join(options.log_dir, 'merge.txt'))
    status = (report.make_fresh if options.redo else report.make)(options.log_dir, *human_status.keys())
    runtime = report.make_fresh(options.log_dir, 'success', 'lookup', 'warnings', 'errors')
    # setup rr_cache
    rr_cache = os.path.join(options.log_dir, "rr-cache")
    try:
        os.mkdir(rr_cache)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
    os.chmod(rr_cache, 0o777)
    # setup base arguments
    base_args = calculate_base_args(options)
    base_args.append("--non-interactive")
    base_args.append("--rr-cache=" + rr_cache)
    # loop variables
    errors = {}
    i = 0
    deploys = deploy.parse_install_lines(app, options.versions_path, user=options.user)
    requested_deploys = itertools.islice(deploys, options.limit)
    # clean up /dev/shm/wizard
    if os.path.exists("/dev/shm/wizard"):
        shutil.rmtree("/dev/shm/wizard")
        os.mkdir("/dev/shm/wizard")
        os.chmod("/dev/shm/wizard", 0o777)
    try:
        for i, d in enumerate(requested_deploys, 1):
            runtime.write("lookup", i, d.location)
            if not os.getuid() and not command.security_check_homedir(d.location):
                continue
            if not options.redo:
                found = False
                for r in status.reports.values():
                    if i in r.values:
                        found = True
                        break
                if found:
                    continue
            # XXX: we may be able to punt based on detected versions from d, which
            # would be faster than spinning up a new process. On the other hand,
            # our aggressive caching strategies using reports make this mostly not a problem
            logging.info("[%04d] Processing %s", i, d.location)
            child_args = list(base_args) # copy
            # calculate the log file, if a log dir was specified
            if options.log_dir:
                log_file = command.calculate_log_name(options.log_dir, i)
                child_args.append("--log-file=" + log_file)
            # actual meat
            def make_on_pair(d, i):
                # we need to make another stack frame so that d and i get specific bindings.
                def on_success(stdout, stderr):
                    if stderr:
                        runtime.write("warnings", i, d.location)
                        logging.warning("[%04d] Warnings at [%s]:\n%s", i, d.location, stderr)
                    runtime.write("success", i, d.location)
                    status.write("up_to_date", i, d.location)
                def on_error(e):
                    if e.name == "AlreadyUpgraded":
                        logging.info("[%04d] Skipped already upgraded %s" % (i, d.location))
                        status.write("up_to_date", i, d.location)
                    elif e.name == "MergeFailed":
                        conflicts, _, tmpdir = e.stdout.rstrip().partition(" ")
                        logging.warning("[%04d] Conflicts in %s files: resolve at [%s], source at [%s]",
                                        i, conflicts, tmpdir, d.location)
                        status.write("merge", i, tmpdir, conflicts, d.location)
                    elif e.name == "BlacklistedError":
                        reason = e.stdout.rstrip().replace("\n", " ")
                        logging.warning("[%04d] Blacklisted because of '%s' at %s", i, reason, d.location)
                        status.write("blacklisted", i, d.location, reason)
                    elif e.name == "WebVerificationError":
                        url = d.url.geturl()
                        # This should actually be a warning, but it's a really common error
                        logging.info("[%04d] Could not verify application at %s", i, url)
                        status.write("verify", i, url)
                    elif e.name == "DatabaseVerificationError":
                        logging.info("[%04d] Could not verify database ast %s", i, d.location)
                        status.write("db", i, d.location)
                    elif e.name == "NotMigratedError":
                        logging.info("[%04d] Application not migrated at %s", i, d.location)
                        status.write("not_migrated", i, d.location)
                    elif e.name == "BackupFailure":
                        logging.info("[%04d] Failed backups at %s", i, d.location)
                        status.write("backup_failure", i, d.location)
                    elif e.name == "QuotaTooLow":
                        logging.info("[%04d] Quota too low at %s", i, d.location)
                        status.write("quota", i, d.location)
                    elif e.name == "PermissionsError":
                        logging.info("[%04d] Insufficient permissions to upgrade %s", i, d.location)
                        status.write("permissions", i, d.location)
                    else:
                        errors.setdefault(e.name, []).append(d)
                        logging.error("[%04d] %s in %s", i, e.name, d.location)
                        runtime.write("errors", i, e.name, d.location)
                        # lack of status write means that we'll always retry
                return (on_success, on_error)
            on_success, on_error = make_on_pair(d, i)
            sh.call("wizard", "upgrade", d.location, *child_args,
                          on_success=on_success, on_error=on_error)
        sh.join()
    finally:
        sys.stderr.write("\n")
        for name, deploys in errors.items():
            logging.warning("%s from %d installs", name, len(deploys))
        print
        total = sum(len(x.values) for x in status.reports.values())
        def printPercent(description, number):
            print "% 4d out of % 4d installs (% 5.1f%%) %s" % (number, total, float(number)/total*100, description)
        error_count = sum(len(e) for e in errors.values())
        if error_count:
            printPercent("had unusual errors", error_count)
        for name, description in human_status.items():
            values = status.reports[name].values
            if values:
                printPercent(description, len(values))
        sys.stderr.write("\n")
        print "%d installs were upgraded this run" % len(runtime.reports["success"].values)

def parse_args(argv, baton):
    usage = """usage: %prog mass-upgrade [ARGS] APPLICATION

Mass upgrades an application to the latest version.  Essentially
equivalent to running '%prog upgrade' on all autoinstalls for a
particular application found by parallel-find, but with advanced
reporting.

This command is intended to be run as root on a server with
the scripts AFS patch."""
    parser = command.WizardOptionParser(usage)
    baton.push(parser, "log_dir")
    baton.push(parser, "no_parallelize")
    baton.push(parser, "dry_run")
    baton.push(parser, "max_processes")
    baton.push(parser ,"limit")
    baton.push(parser, "versions_path")
    baton.push(parser, "srv_path")
    baton.push(parser, "user")
    parser.add_option("--force", dest="force", action="store_true",
            default=False, help="Force running upgrade even if it's already at latest version.")
    parser.add_option("--redo", dest="redo", action="store_true",
            default=False, help="Redo all upgrades; use this if you updated Wizard's code.")
    parser.add_option("--remerge", dest="remerge", action="store_true",
            default=False, help="Redo all merges.")
    options, args, = parser.parse_all(argv)
    if len(args) > 1:
        parser.error("too many arguments")
    elif not args:
        parser.error("must specify application to upgrade")
    return options, args

def calculate_base_args(options):
    return command.make_base_args(options, dry_run="--dry-run", srv_path="--srv-path", force="--force")

