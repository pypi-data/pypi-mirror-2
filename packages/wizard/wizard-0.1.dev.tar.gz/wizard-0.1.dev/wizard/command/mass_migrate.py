import logging
import os
import os.path
import itertools

from wizard import deploy, report, shell, sset, command

def main(argv, baton):
    options, args = parse_args(argv, baton)
    app = args[0]
    base_args = calculate_base_args(options)
    sh = shell.ParallelShell.make(options.no_parallelize, options.max_processes)
    command.create_logdir(options.log_dir)
    seen = sset.make(options.seen)
    is_root = not os.getuid()
    runtime = report.make_fresh(options.log_dir, "success", "warnings", "errors")
    # loop stuff
    errors = {}
    i = 0
    deploys = deploy.parse_install_lines(app, options.versions_path, user=options.user)
    requested_deploys = itertools.islice(deploys, options.limit)
    for i, d in enumerate(requested_deploys, 1):
        # check if we want to punt due to --limit
        if d.location in seen:
            continue
        if is_root and not command.security_check_homedir(d.location):
            continue
        logging.info("Processing %s" % d.location)
        child_args = list(base_args)
        # calculate the log file, if a log dir was specified
        if options.log_dir:
            log_file = command.calculate_log_name(options.log_dir, i)
            child_args.append("--log-file=" + log_file)
        # actual meat
        def make_on_pair(d, i):
            # we need to make another stack frame so that d and i get specific bindings.
            def on_success(stdout, stderr):
                if stderr:
                    logging.warning("Warnings [%04d] %s:\n%s" % (i, d.location, stderr))
                    runtime.write("warnings", i, d.location)
                runtime.write("success", i, d.location)
            def on_error(e):
                if e.name == "wizard.command.migrate.AlreadyMigratedError" or \
                   e.name == "AlreadyMigratedError":
                    logging.info("Skipped already migrated %s" % d.location)
                else:
                    errors.setdefault(e.name, []).append(d)
                    logging.error("%s in [%04d] %s", e.name, i, d.location)
                    runtime.write("errors", i, d.location)
            return (on_success, on_error)
        on_success, on_error = make_on_pair(d, i)
        sh.call("wizard", "migrate", d.location, *child_args,
                      on_success=on_success, on_error=on_error)
    sh.join()
    for name, deploys in errors.items():
        logging.warning("%s from %d installs" % (name, len(deploys)))

def parse_args(argv, baton):
    usage = """usage: %prog mass-migrate [ARGS] APPLICATION

Mass migrates an application to the new repository format.
Essentially equivalent to running '%prog migrate' on all
autoinstalls for a particular application found by parallel-find,
but with advanced reporting.

This command is intended to be run as root on a server with
the scripts AFS patch."""
    parser = command.WizardOptionParser(usage)
    baton.push(parser, "log_dir")
    baton.push(parser, "seen")
    baton.push(parser, "no_parallelize")
    baton.push(parser, "dry_run")
    baton.push(parser, "max_processes")
    parser.add_option("--force", dest="force", action="store_true",
            default=False, help="Force migrations to occur even if .wizard or .git exists.")
    baton.push(parser ,"limit")
    baton.push(parser, "versions_path")
    baton.push(parser, "srv_path")
    baton.push(parser, "user")
    options, args, = parser.parse_all(argv)
    if len(args) > 1:
        parser.error("too many arguments")
    elif not args:
        parser.error("must specify application to migrate")
    return options, args

def calculate_base_args(options):
    return command.make_base_args(options, dry_run="--dry-run", srv_path="--srv-path",
            force="--force")

