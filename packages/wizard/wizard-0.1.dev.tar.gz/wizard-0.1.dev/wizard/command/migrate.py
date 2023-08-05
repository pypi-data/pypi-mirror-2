import os
import os.path
import shutil
import logging

from wizard import command, deploy, shell, util

# LEGACY (but still necessary, since we haven't migrated all of scripts
# yet.  Maybe if we plugin-ify the commands interface move this.)

def main(argv, baton):
    options, args = parse_args(argv, baton)
    dir = os.path.abspath(args[0]) if args else os.getcwd()
    shell.drop_priviledges(dir, options.log_file)
    util.chdir(dir)

    sh = shell.Shell(options.dry_run)

    logging.info("Migrating %s" % dir)
    logging.debug("uid is %d" % os.getuid())

    deployment = deploy.ProductionCopy(".")

    os.unsetenv("GIT_DIR") # prevent some perverse errors

    try:
        deployment.verify()
        raise AlreadyMigratedError(deployment.location)
    except deploy.NotMigratedError:
        pass
    except (deploy.CorruptedAutoinstallError, AlreadyMigratedError):
        if not options.force:
            raise

    deployment.verifyTag(options.srv_path)

    if options.force_version:
        version = deployment.application.makeVersion(options.force_version)
    else:
        try:
            deployment.verifyVersion()
            version = deployment.app_version
        except deploy.VersionMismatchError as e:
            # well, we'll use that then
            version = deployment.application.makeVersion(str(e.real_version))
    repo = version.application.repository(options.srv_path)
    tag = version.wizard_tag
    try:
        sh.call("git", "--git-dir=%s" % repo, "rev-parse", tag)
    except shell.CallError:
        raise UnsupportedVersion(version.version)

    with util.LockDirectory(".wizard-migrate-lock"):
        try:
            if options.force:
                perform_force(options)
            make_repository(sh, options, repo, tag)
            check_variables(deployment, options)
        except KeyboardInterrupt:
            # revert it; barring zany race conditions this is safe
            if os.path.exists(".wizard"):
                shutil.rmtree(".wizard")
            if os.path.exists(".git"):
                shutil.rmtree(".git")

def parse_args(argv, baton):
    usage = """usage: %prog migrate [ARGS] DIR

Migrates a directory to our Git-based autoinstall format.
Performs basic sanity checking and intelligently determines
what repository and tag to use.

This command is meant to be run as the owner of the install it is
upgrading .  Do NOT run this command as root."""
    parser = command.WizardOptionParser(usage)
    baton.push(parser, "srv_path")
    parser.add_option("--dry-run", dest="dry_run", action="store_true",
            default=False, help="Prints would would be run without changing anything")
    parser.add_option("--force", "-f", dest="force", action="store_true",
            default=False, help="If .git or .wizard directory already exists,"
            "delete them and migrate")
    parser.add_option("--force-version", dest="force_version",
            default=None, help="If .scripts-version tells lies, explicitly specify"
            "a version to migrate to.")
    options, args = parser.parse_all(argv)
    if len(args) > 1:
        parser.error("too many arguments")
    return (options, args)

def perform_force(options):
    has_git = os.path.isdir(".git")
    has_wizard = os.path.isdir(".wizard")

    if has_git:
        logging.warning("Force removing .git directory")
        if not options.dry_run: backup = util.safe_unlink(".git")
        logging.info(".git backed up to %s" % backup)
    if has_wizard:
        logging.warning("Force removing .wizard directory")
        if not options.dry_run: backup = util.safe_unlink(".wizard")
        logging.info(".wizard backed up to %s" % backup)

def make_repository(sh, options, repo, tag):
    sh.call("git", "init") # create repository
    # configure our alternates (to save space and make this quick)
    data = os.path.join(repo, "objects")
    file = ".git/objects/info/alternates"
    if not options.dry_run:
        alternates = open(file, "w")
        alternates.write(data)
        alternates.close()
        htaccess = open(".git/.htaccess", "w")
        htaccess.write("Deny from all\n")
        htaccess.close()
    else:
        logging.info("# create %s containing \"%s\"" % (file, data))
        logging.info('# create .htaccess containing "Deny from all"')
    # configure our remote (this is merely for convenience; wizard
    # will not rely on this)
    sh.call("git", "remote", "add", "origin", repo)
    # configure what would normally be set up on a 'git clone' for consistency
    sh.call("git", "config", "branch.master.remote", "origin")
    sh.call("git", "config", "branch.master.merge", "refs/heads/master")
    # perform the initial fetch
    sh.call("git", "fetch", "origin")
    # soft reset to our tag
    sh.call("git", "reset", tag, "--")
    # initialize the .wizard directory
    util.init_wizard_dir()
    logging.info("Diffstat:\n" + sh.eval("git", "diff", "--stat"))
    # commit user local changes
    message = "Autoinstall migration.\n\n%s" % util.get_git_footer()
    util.set_git_env()
    try:
        message += "\nMigrated-by: " + util.get_operator_git()
    except util.NoOperatorInfo:
        pass
    sh.call("git", "commit", "--allow-empty", "-a", "-m", message)

def check_variables(d, options):
    """Attempt to extract variables and complain if some are missing."""
    variables = d.extract()
    for k,v in variables.items():
        if v is None and k not in d.application.deprecated_keys:
            logging.warning("Variable %s not found" % k)
        else:
            logging.debug("Variable %s is %s" % (k,v))

class Error(command.Error):
    """Base exception for all exceptions raised by migrate"""
    pass

class AlreadyMigratedError(Error):
    quiet = True
    def __init__(self, dir):
        self.dir = dir
    def __str__(self):
        return """

This autoinstall is already migrated; move along, nothing to
see here.  (If you really want to, you can force a re-migration
with --force, but this will blow away the existing .git and
.scripts directories (i.e. your history and Wizard configuration).)
"""

class UnsupportedVersion(Error):
    def __init__(self, version):
        self.version = version
    def __str__(self):
        return """

ERROR: This autoinstall is presently on %s, which is unsupported by
Wizard.  Please manually upgrade it to one that is supported,
and then retry the migration; usually the latest version is supported.
""" % self.version
