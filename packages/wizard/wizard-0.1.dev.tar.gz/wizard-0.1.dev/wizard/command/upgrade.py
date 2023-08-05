import sys
import distutils.version
import os
import os.path
import shutil
import logging.handlers
import tempfile
import itertools
import time
import errno

from wizard import app, command, deploy, merge, shell, user, util

buffer = 1024 * 1024 * 30 # 30 MiB we will always leave available
errno_blacklisted = 64

def main(argv, baton):
    options, args = parse_args(argv, baton)
    dir = os.path.abspath(args[0]) if args else os.getcwd()
    os.chdir(dir)
    shell.drop_priviledges(dir, options.log_file)
    util.set_git_env()
    upgrade = Upgrade(options)
    upgrade.execute(dir)
    if not options.non_interactive:
        print "Upgrade complete"

class Upgrade(object):
    """
    Represents the algorithm for upgrading an application.  This is in
    a class and not a function because it's a multi-step process that
    requires state betweens steps.  Steps are represented as methods
    in this object.
    """

    #: Version of application we are upgrading to, i.e. the latest version.
    version = None # XXX: This is a string... I'm not convinced it should be
    #: String commit ID of the user's latest wc; i.e. "ours"
    user_commit = None
    #: String commit ID of the latest, greatest wizard version; i.e. "theirs"
    next_commit = None
    #: The temporary directory that the system gave us; may stay as ``None``
    #: if we don't ever make ourselves a temporary directory (e.g. ``--continue``).
    #: While we should clean this up if it is set to something, it may
    #: not correspond to anything useful.
    temp_dir = None
    #: The temporary directory containing our working copy for merging
    temp_wc_dir = None
    #: We place the temporary repositories inside a tmpfs while merging;
    #: this makes merges not disk-bound and affords a modest speed increase.
    #: If you are running ``--continue``, this is guaranteed to be ``False``.
    use_shm = None
    #: Upstream repository to use.  This does not need to be saved.
    repo = None

    #: Instance of :class:`wizard.deploy.WorkingCopy` for this upgrade
    wc = None
    #: Instance of :class:`wizard.deploy.ProductionCopy` for this upgrade
    prod = None

    #: Options object that the installer was called with
    options = None

    def __init__(self, options):
        self.version = None
        self.user_commit = None
        self.next_commit = None
        self.temp_dir = None
        self.temp_wc_dir = None
        self.use_shm = False # False until proven otherwise.
        self.wc = None
        self.prod = None
        self.options = options

    def execute(self, dir):
        """
        Executes an upgrade.  This is the entry-point.  This expects
        that it's current working directory is the same as ``dir``.
        """
        assert os.path.abspath(dir) == os.getcwd()
        try:
            if self.options.continue_:
                logging.info("Continuing upgrade...")
                self.resume()
            else:
                logging.info("Upgrading %s" % os.getcwd())
                self.preflight()
                self.merge()
            self.postflight()
            # Till now, all of our operations were in a tmp sandbox.
            if self.options.dry_run:
                logging.info("Dry run, bailing.  See results at %s" % self.temp_wc_dir)
                return
            backup = self.backup()
            self.upgrade(backup)
        finally:
            if self.use_shm and self.temp_dir and os.path.exists(self.temp_dir):
                shutil.rmtree(self.temp_dir)

    def resume(self):
        """
        In the event of a ``--continue`` flag, we have to restore state and
        perform some sanity checks.
        """
        self.resumeChdir()
        self.resumeState()
        self.resumeLogging()
        util.chdir(shell.eval("git", "config", "remote.origin.url"))
        self.resumeProd()
    def resumeChdir(self):
        """
        If we called ``--continue`` inside a production copy,  check if
        :file:`.wizard/pending` exists and change to that directory if so.
        """
        # XXX: Can't use deploy; maybe should stringify constants?
        if os.path.exists(".wizard/pending"):
            newdir = open(".wizard/pending").read().strip()
            logging.warning("Detected production copy; changing directory to %s", newdir)
            os.chdir(newdir)
    def resumeState(self):
        self.temp_wc_dir = os.getcwd()
        self.wc = deploy.WorkingCopy(".")
        try:
            self.user_commit, self.next_commit = open(".git/WIZARD_PARENTS", "r").read().split()
            self.version = open(".git/WIZARD_UPGRADE_VERSION", "r").read()
        except IOError as e:
            if e.errno == errno.ENOENT:
                raise CannotResumeError()
            else:
                raise
    def resumeLogging(self):
        options = self.options
        if not options.log_file and os.path.exists(".git/WIZARD_LOG_FILE"):
            options.log_file = open(".git/WIZARD_LOG_FILE", "r").read()
            command.setup_file_logger(options.log_file, options.debug)
    def resumeProd(self):
        """Restore :attr:`prod` attribute, and check if the production copy has drifted."""
        self.prod = deploy.ProductionCopy(".")
        try:
            # simulate the action of `git status`, based on cmd_status()'s call to
            # refresh_cache() in builtin-commit.c
            shell.call("git", "update-index", "-q", "--unmerged", "--refresh")
            r1 = shell.eval("git", "diff-files", "--name-only").strip()
            r2 = shell.eval("git", "diff-index", "--name-only", "HEAD").strip()
            if r1 or r2:
                raise LocalChangesError()
        except shell.CallError:
            pass
        # Working copy is not anchored anywhere useful for git describe,
        # so we need to give it a hint.
        self.wc.setAppVersion(self.prod.app_version)

    def preflight(self):
        """
        Make sure that a number of pre-upgrade invariants are met before
        attempting anything.
        """
        options = self.options
        for i in range(0,2):
            self.prod = deploy.ProductionCopy(".")
            self.prod.verify()
            self.repo = self.prod.application.repository(options.srv_path)
            # XXX: put this in Application
            self.version = shell.eval("git", "--git-dir="+self.repo, "describe", "--tags", "master")
            self.preflightBlacklist()
            self.prod.verify()
            self.prod.verifyDatabase()
            self.prod.verifyTag(options.srv_path)
            self.prod.verifyGit(options.srv_path)
            self.prod.verifyConfigured()
            try:
                shell.call("git", "fetch", "--tags") # XXX: hack since some installs have stale tags
            except shell.CallError as e:
                if "Disk quota exceeded" in e.stderr:
                    raise QuotaTooLow
                raise
            try:
                self.prod.verifyVersion()
            except deploy.VersionMismatchError as e:
                # XXX: kind of hacky, mainly it does change the Git working copy
                # state (although /very/ non-destructively)
                try:
                    shell.call("git", "merge", "--strategy=ours", self.prod.application.makeVersion(str(e.real_version)).wizard_tag)
                except shell.CallError as e2:
                    if "does not point to a commit" in e2.stderr:
                        raise UnknownVersionError(e.real_version)
                    else:
                        raise
                continue
            break
        else:
            raise VersionRematchFailed
        self.prod.verifyWeb()
        self.preflightAlreadyUpgraded()
        self.preflightQuota()
    def preflightBlacklist(self):
        # XXX: should use deploy info
        if os.path.exists(".wizard/blacklisted"):
            reason = open(".wizard/blacklisted").read()
            # ignore blank blacklisted files
            if reason:
                print reason
                raise BlacklistedError(reason)
            else:
                logging.warning("Application was blacklisted, but no reason was found");
    def preflightAlreadyUpgraded(self):
        if self.version == self.prod.app_version.wizard_tag and not self.options.force:
            # don't log this error; we need to have the traceback line
            # so that the parsing code can catch it
            # XXX: maybe we should build this in as a flag to add
            # to exceptions w/ our exception handler
            sys.stderr.write("Traceback:\n  (n/a)\nAlreadyUpgraded\n")
            sys.exit(2)
    def preflightQuota(self):
        r = user.quota()
        if r is not None:
            usage, limit = r
            if limit is not None and (limit - usage) < buffer:
                logging.info("preflightQuota: limit = %d, usage = %d, buffer = %d", limit, usage, buffer)
                raise QuotaTooLow

    def merge(self):
        if not self.options.dry_run:
            self.mergePreCommit()
        self.mergeClone()
        logging.debug("Temporary WC dir is %s", self.temp_wc_dir)
        with util.ChangeDirectory(self.temp_wc_dir):
            self.wc = deploy.WorkingCopy(".")
            shell.call("git", "remote", "add", "wizard", self.repo)
            shell.call("git", "fetch", "-q", "wizard")
            self.user_commit = shell.eval("git", "rev-parse", "HEAD")
            self.next_commit = shell.eval("git", "rev-parse", self.version)
            self.mergeSaveState()
            self.mergePerform()
    def mergePreCommit(self):
        def get_file_set(rev):
            return set(shell.eval("git", "ls-tree", "-r", "--name-only", rev).split("\n"))
        # add all files that are unversioned but would be replaced by the pull,
        # and generate a new commit
        old_files = get_file_set("HEAD")
        new_files = get_file_set(self.version)
        added_files = new_files - old_files
        for f in added_files:
            if os.path.lexists(f): # broken symbolic links count too!
                shell.call("git", "add", f)
        message = "Pre-commit before autoinstall upgrade.\n\n%s" % util.get_git_footer()
        try:
            message += "\nPre-commit-by: " + util.get_operator_git()
        except util.NoOperatorInfo:
            pass
        try:
            shell.call("git", "commit", "-a", "-m", message)
        except shell.CallError as e:
            if "Permission denied" in e.stderr:
                raise util.PermissionsError
            elif e.stderr:
                raise
            logging.info("No changes detected")
    def mergeClone(self):
        # If /dev/shm exists, it's a tmpfs and we can use it
        # to do a fast git merge. Don't forget to move it to
        # /tmp if it fails.
        if not self.options.dry_run and not self.options.debug:
            self.use_shm = os.path.exists("/dev/shm")
        if self.use_shm:
            dir = "/dev/shm/wizard"
            if not os.path.exists(dir):
                os.mkdir(dir)
                # XXX: race
                os.chmod(dir, 0o777)
        else:
            dir = None
        self.temp_dir = tempfile.mkdtemp(prefix="wizard", dir=dir)
        self.temp_wc_dir = os.path.join(self.temp_dir, "repo")
        logging.info("Using temporary directory: " + self.temp_wc_dir)
        shell.call("git", "clone", "-q", "--shared", ".", self.temp_wc_dir)
    def mergeSaveState(self):
        """Save variables so that ``--continue`` will work."""
        # yeah yeah no trailing newline whatever
        open(".git/WIZARD_UPGRADE_VERSION", "w").write(self.version)
        open(".git/WIZARD_PARENTS", "w").write("%s\n%s" % (self.user_commit, self.next_commit))
        open(".git/WIZARD_SIZE", "w").write(str(util.disk_usage()))
        if self.options.log_file:
            open(".git/WIZARD_LOG_FILE", "w").write(self.options.log_file)
    def mergePerform(self):
        def prepare_config():
            self.wc.prepareConfig()
            shell.call("git", "add", ".")
        def resolve_conflicts():
            return self.wc.resolveConflicts()
        shell.call("git", "config", "merge.conflictstyle", "diff3")
        # setup rerere
        if self.options.rr_cache is None:
            self.options.rr_cache = os.path.join(self.prod.location, ".git", "rr-cache")
        if not os.path.exists(self.options.rr_cache):
            os.mkdir(self.options.rr_cache)
        os.symlink(self.options.rr_cache, os.path.join(self.wc.location, ".git", "rr-cache"))
        shell.call("git", "config", "rerere.enabled", "true")
        try:
            merge.merge(self.wc.app_version.wizard_tag, self.version,
                        prepare_config, resolve_conflicts)
        except merge.MergeError:
            self.mergeFail()
    def mergeFail(self):
        files = set()
        for line in shell.eval("git", "ls-files", "--unmerged").splitlines():
            files.add(line.split(None, 3)[-1])
        conflicts = len(files)
        # XXX: this is kind of fiddly; note that temp_dir still points at the OLD
        # location after this code.
        self.temp_wc_dir = mv_shm_to_tmp(os.getcwd(), self.use_shm)
        self.wc.location = self.temp_wc_dir
        os.chdir(self.temp_wc_dir)
        open(self.prod.pending_file, "w").write(self.temp_wc_dir)
        if self.options.non_interactive:
            print "%d %s" % (conflicts, self.temp_wc_dir)
            raise MergeFailed
        else:
            user_shell = os.getenv("SHELL")
            if not user_shell: user_shell = "/bin/bash"
            # XXX: scripts specific hack, since mbash doesn't respect the current working directory
            # When the revolution comes (i.e. $ATHENA_HOMEDIR/Scripts is your Scripts home
            # directory) this isn't strictly necessary, but we'll probably need to support
            # web_scripts directories ad infinitum.
            if user_shell == "/usr/local/bin/mbash": user_shell = "/bin/bash"
            while 1:
                print
                print "ERROR: The merge failed with %d conflicts in these files:" % conflicts
                print
                for file in sorted(files):
                    print "  * %s" % file
                print
                print "Please resolve these conflicts (edit and then `git add`), and"
                print "then type 'exit'.  You will now be dropped into a shell whose working"
                print "directory is %s" % self.temp_wc_dir
                try:
                    shell.call(user_shell, "-i", interactive=True)
                except shell.CallError as e:
                    logging.warning("Shell returned non-zero exit code %d" % e.code)
                if shell.eval("git", "ls-files", "--unmerged").strip():
                    print
                    print "WARNING: There are still unmerged files."
                    out = raw_input("Continue editing? [y/N]: ")
                    if out == "y" or out == "Y":
                        continue
                    else:
                        print "Aborting.  The conflicted working copy can be found at:"
                        print
                        print "    %s" % self.temp_wc_dir
                        print
                        print "and you can resume the upgrade process by running in that directory:"
                        print
                        print "    wizard upgrade --continue"
                        sys.exit(1)
                break

    def postflight(self):
        with util.ChangeDirectory(self.temp_wc_dir):
            if shell.eval("git", "ls-files", "-u").strip():
                raise UnmergedChangesError
            shell.call("git", "commit", "--allow-empty", "-am", "throw-away commit")
            self.wc.parametrize(self.prod)
            shell.call("git", "add", ".")
            message = self.postflightCommitMessage()
            new_tree = shell.eval("git", "write-tree")
            final_commit = shell.eval("git", "commit-tree", new_tree,
                    "-p", self.user_commit, "-p", self.next_commit, input=message, log=True)
            # a master branch may not necessarily exist if the user
            # was manually installed to an earlier version
            try:
                shell.call("git", "checkout", "-q", "-b", "master", "--")
            except shell.CallError:
                shell.call("git", "checkout", "-q", "master", "--")
            shell.call("git", "reset", "-q", "--hard", final_commit)
            # This is a quick sanity check to make sure we didn't completely
            # mess up the merge
            self.wc.invalidateCache()
            self.wc.verifyVersion()
    def postflightCommitMessage(self):
        message = "Upgraded autoinstall to %s.\n\n%s" % (self.version, util.get_git_footer())
        try:
            message += "\nUpgraded-by: " + util.get_operator_git()
        except util.NoOperatorInfo:
            pass
        return message

    def backup(self):
        # Ok, now we have to do a crazy complicated dance to see if we're
        # going to have enough quota to finish what we need
        pre_size = int(open(os.path.join(self.temp_wc_dir, ".git/WIZARD_SIZE"), "r").read())
        post_size = util.disk_usage(self.temp_wc_dir)
        backup = self.prod.backup(self.options)
        r = user.quota()
        if r is not None:
            usage, limit = r
            if limit is not None and (limit - usage) - (post_size - pre_size) < buffer:
                shutil.rmtree(os.path.join(self.prod.backup_dir, shell.eval("wizard", "restore").splitlines()[0]))
                raise QuotaTooLow
        return backup

    def upgrade(self, backup):
        # XXX: frob .htaccess to make site inaccessible
        # XXX: frob Git to disallow Git operations after the pull
        with util.IgnoreKeyboardInterrupts():
            with util.LockDirectory(".wizard-upgrade-lock"):
                shell.call("git", "fetch", "--tags")
                # git merge (which performs a fast forward)
                shell.call("git", "pull", "-q", self.temp_wc_dir, "master")
                version_obj = distutils.version.LooseVersion(self.version.partition('-')[2])
                try:
                    # run update script
                    self.prod.upgrade(version_obj, self.options)
                    self.prod.verifyWeb()
                except app.UpgradeFailure:
                    logging.warning("Upgrade failed: rolling back")
                    self.upgradeRollback(backup)
                    raise
                except deploy.WebVerificationError as e:
                    logging.warning("Web verification failed: rolling back")
                    self.upgradeRollback(backup)
                    raise app.UpgradeVerificationFailure()
        # XXX: frob .htaccess to make site accessible
        #       to do this, check if .htaccess changed, first.  Upgrade
        #       process might have frobbed it.  Don't be
        #       particularly worried if the segment disappeared
    def upgradeRollback(self, backup):
        # You don't want d.restore() because it doesn't perform
        # the file level backup
        if not self.options.disable_rollback:
            shell.call("wizard", "restore", backup)
            try:
                self.prod.verifyWeb()
            except deploy.WebVerificationError:
                logging.critical("Web verification failed after rollback")
        else:
            logging.warning("Rollback was disabled; you can rollback with `wizard restore %s`", backup)

# utility functions

def mv_shm_to_tmp(curdir, use_shm):
    if not use_shm: return curdir
    # Keeping all of our autoinstalls in shared memory is
    # a recipe for disaster, so let's move them to slightly
    # less volatile storage (a temporary directory)
    os.chdir(tempfile.gettempdir())
    newdir = tempfile.mkdtemp(prefix="wizard")
    # shutil, not os; at least on Ubuntu os.move fails
    # with "[Errno 18] Invalid cross-device link"
    shutil.move(curdir, newdir)
    shutil.rmtree(os.path.dirname(curdir))
    curdir = os.path.join(newdir, "repo")
    return curdir

def parse_args(argv, baton):
    usage = """usage: %prog upgrade [ARGS] [DIR]

Upgrades an autoinstall to the latest version.  This involves updating
files the upgrade script associated with this application.  If the merge
fails, this program will write the number of conflicts and the directory
of the conflicted working tree to stdout, separated by a space."""
    parser = command.WizardOptionParser(usage)
    parser.add_option("--dry-run", dest="dry_run", action="store_true",
            default=False, help="Prints would would be run without changing anything")
    # notice trailing underscore
    parser.add_option("--continue", dest="continue_", action="store_true",
            default=False, help="Continues an upgrade that has had its merge manually "
            "resolved using the current working directory as the resolved copy.")
    parser.add_option("--force", dest="force", action="store_true",
            default=False, help="Force running upgrade even if it's already at latest version.")
    parser.add_option("--non-interactive", dest="non_interactive", action="store_true",
            default=False, help="Don't drop to shell in event of conflict.")
    parser.add_option("--rr-cache", dest="rr_cache", metavar="PATH",
            default=None, help="Use this folder to reuse recorded merge resolutions.  Defaults to"
            "your production copy's rr-cache, if it exists.")
    parser.add_option("--disable-rollback", dest="disable_rollback", action="store_true",
            default=util.boolish(os.getenv("WIZARD_DISABLE_ROLLBACK")),
            help="Skips rollback in the event of a failed upgrade. Envvar is WIZARD_DISABLE_ROLLBACK.")
    baton.push(parser, "srv_path")
    options, args = parser.parse_all(argv)
    if len(args) > 1:
        parser.error("too many arguments")
    return options, args

class Error(command.Error):
    """Base exception for all exceptions raised by upgrade"""
    pass

class QuotaTooLow(Error):
    def __str__(self):
        return """

ERROR: The locker quota was too low to complete the autoinstall
upgrade.
"""

class AlreadyUpgraded(Error):
    quiet = True
    def __str__(self):
        return """

ERROR: This autoinstall is already at the latest version."""

class MergeFailed(Error):
    quiet = True
    def __str__(self):
        return """

ERROR: Merge failed.  Above is the temporary directory that
the conflicted merge is in: resolve the merge by cd'ing to the
temporary directory, finding conflicted files with `git status`,
resolving the files, adding them using `git add` and then
running `wizard upgrade --continue`."""

class LocalChangesError(Error):
    def __str__(self):
        return """

ERROR: Local changes occurred in the install while the merge was
being processed so that a pull would not result in a fast-forward.
The best way to resolve this is probably to attempt an upgrade again,
with git rerere to remember merge resolutions (XXX: not sure if
this actually works)."""

class UnmergedChangesError(Error):
    def __str__(self):
        return """

ERROR: You attempted to continue an upgrade, but there were
still local unmerged changes in your working copy.  Please resolve
them all and try again."""

class BlacklistedError(Error):
    #: Reason why the autoinstall was blacklisted
    reason = None
    exitcode = errno_blacklisted
    def __init__(self, reason):
        self.reason = reason
    def __str__(self):
        return """

ERROR: This autoinstall was manually blacklisted against errors;
if the user has not been notified of this, please send them
mail.

The reason was: %s""" % self.reason

class CannotResumeError(Error):
    def __str__(self):
        return """

ERROR: We cannot resume the upgrade process; either this working
copy is missing essential metadata, or you've attempt to continue
from a production copy that does not have any pending upgrades.
"""

class VersionRematchFailed(Error):
    def __str__(self):
        return """

ERROR: Your Git version information was not consistent with your
files on the system, and we were unable to create a fake merge
to make the two consistent."""

class UnknownVersionError(Error):
    #: Version that we didn't have
    version = None
    def __init__(self, version):
        self.version = version
    def __str__(self):
        return """

ERROR: The version you are attempting to upgrade from (%s)
is unknown to the repository Wizard is using.""" % str(self.version)
