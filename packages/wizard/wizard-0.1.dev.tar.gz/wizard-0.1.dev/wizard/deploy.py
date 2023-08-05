"""
Object model for querying information and manipulating deployments
of autoinstalls.  Every :class:`Deployment` has an :class:`app.ApplicationVersion`
which in turn has an :class:`app.Application`.
"""

import os.path
import fileinput
import logging
import decorator
import datetime
import tempfile
import time
import traceback
import shutil
import errno
import pkg_resources
import urlparse

import wizard
from wizard import app, git, old_log, shell, sql, util

## -- Global Functions --

def get_install_lines(versions_store, user=None):
    """
    Low level function that retrieves a list of lines from the
    :term:`versions store` that can be passed to :meth:`Deployment.parse`.
    """
    if os.path.isfile(versions_store):
        return fileinput.input([versions_store])
    if user:
        return fileinput.input([versions_store + "/" + user])
    return fileinput.input([versions_store + "/" + f for f in sorted(os.listdir(versions_store))])

def parse_install_lines(show, versions_store, yield_errors = False, user = None):
    """
    Generator function for iterating through all autoinstalls.
    Each item is an instance of :class:`Deployment`, or possibly
    a :class:`wizard.deploy.Error` if ``yield_errors`` is ``True``.  You can
    filter out applications and versions by specifying ``app``
    or ``app-1.2.3`` in ``show``.  This function may generate
    log output.
    """
    if not show:
        show = app.applications()
    elif isinstance(show, str):
        # otherwise, frozenset will treat string as an iterable
        show = frozenset([show])
    else:
        show = frozenset(show)
    for line in get_install_lines(versions_store, user):
        # construction
        try:
            d = Deployment.parse(line)
            name = d.application.name
        except app.NoSuchApplication as e:
            if not e.location:
                try:
                    e.location = line.split(':')[0]
                except IndexError:
                    e.location = line
            if yield_errors:
                yield e
            continue
        except Error:
            # we consider this a worse error
            logging.warning("Error with '%s'" % line.rstrip())
            continue
        # filter
        if name + "-" + util.truncate(str(d.version)) in show or name in show:
            pass
        else:
            continue
        # yield
        yield d

def web(dir, url=None):
    """
    Attempts to determine the URL a directory would be web-accessible at.
    If ``url`` is specified, automatically use it.  Returns a generator which
    produces a list of candidate urls.

    This function implements a plugin interface named :ref:`wizard.deploy.web`.
    """
    if url:
        if isinstance(url, str):
            url = urlparse.urlparse(url)
        logging.info("wizard.deploy.web: Using default URL %s", url)
        yield url
        return

    for entry in pkg_resources.iter_entry_points("wizard.deploy.web"):
        logging.debug("wizard.deploy.web: Processing %s", entry)
        f = entry.load()
        for r in f(dir):
            if isinstance(r, str):
                r = urlparse.urlparse(r)
            logging.info("wizard.deploy.web: Using plugin-supplied URL %s", r)
            yield r

    # try the environment
    host = os.getenv("WIZARD_WEB_HOST")
    path = os.getenv("WIZARD_WEB_PATH")
    if host is not None and path is not None:
        r = urlparse.ParseResult(
                "http",
                host,
                path.rstrip('/'),
                "", "", "")
        logging.info("wizard.deploy.web: Using environment URL %s", r)
        yield r

    logging.info("wizard.deploy.web: Exhausted URLs")

## -- Model Objects --

@decorator.decorator
def chdir_to_location(f, self, *args, **kwargs):
    """
    Decorator for making a function have working directory
    :attr:`Deployment.location`.
    """
    with util.ChangeDirectory(self.location):
        return f(self, *args, **kwargs)

class Deployment(object):
    """
    Represents a deployment of an autoinstall, e.g. directory that has a
    ``.wizard`` directory in it.  Supply ``version`` with an
    :class:`ApplicationVersion` only if you were reading from the
    :term:`versions store` and care about speed (data from there can be
    stale).

    The Deployment interface is somewhat neutered, so you may
    want to use :class:`WorkingCopy` or :class:`ProductionCopy` for
    more powerful operations.

    .. note::

        For legacy purposes, deployments can also be marked by a
        ``.scripts`` directory or a ``.scripts-version`` file.
    """
    #: Absolute path to the deployment
    location = None
    def __init__(self, location, version=None):
        self.location = os.path.abspath(location)
        self._app_version = version
        # some cache variables
        self._read_cache = {}
        self._old_log = None
        self._dsn = None
        self._url = None
        self._urlGen = None
        self._wizard_dir = None
    def invalidateCache(self):
        """
        Invalidates all cached variables.  This currently applies to
        :attr:`app_version`, :attr:`old_log` and :meth:`read`.
        """
        self._app_version = None
        self._read_cache = {}
        self._old_log = None
    def read(self, file, force = False):
        """
        Reads a file's contents, possibly from cache unless ``force``
        is ``True``.
        """
        if force or file not in self._read_cache:
            f = open(os.path.join(self.location, file))
            self._read_cache[file] = f.read()
            f.close()
        return self._read_cache[file]
    def extract(self):
        """
        Extracts all the values of all variables from deployment.
        These variables may be used for parametrizing generic parent
        commits and include things such as database access credentials
        and local configuration.
        """
        return self.application.extract(self)

    def verify(self, no_touch=False):
        """
        Checks if this is an autoinstall, throws an exception if there
        are problems.  If ``no_touch`` is ``True``, it will not attempt
        edit the installation.
        """
        with util.ChangeDirectory(self.location):
            has_git = os.path.isdir(".git")
            has_wizard = os.path.isdir(".wizard")
            if not has_wizard and os.path.isdir(".scripts"):
                # LEGACY
                os.symlink(".scripts", ".wizard")
                has_wizard = True
            if not has_git and has_wizard:
                raise CorruptedAutoinstallError(self.location)
            elif has_git and not has_wizard:
                raise AlreadyVersionedError(self.location)
            # LEGACY
            elif not has_git and not has_wizard:
                if os.path.isfile(".scripts-version"):
                    raise NotMigratedError(self.location)
                else:
                    raise NotAutoinstallError(self.location)

    def verifyTag(self, srv_path):
        """
        Checks if the purported version has a corresponding tag
        in the upstream repository.
        """
        repo = self.application.repository(srv_path)
        try:
            shell.eval("git", "--git-dir", repo, "rev-parse", self.app_version.wizard_tag, '--')
        except shell.CallError:
            raise NoTagError(self.app_version.wizard_tag)

    def verifyGit(self, srv_path):
        """
        Checks if the autoinstall's Git repository makes sense,
        checking if the tag is parseable and corresponds to
        a real application, and if the tag in this repository
        corresponds to the one in the remote repository.
        """
        with util.ChangeDirectory(self.location):
            repo = self.application.repository(srv_path)
            def repo_rev_parse(tag):
                return shell.eval("git", "--git-dir", repo, "rev-parse", tag)
            def self_rev_parse(tag):
                try:
                    return shell.safeCall("git", "rev-parse", tag, strip=True)
                except shell.CallError:
                    raise NoLocalTagError(tag)
            def compare_tags(tag):
                return repo_rev_parse(tag) == self_rev_parse(tag)
            if not compare_tags(self.app_version.pristine_tag):
                raise InconsistentPristineTagError(self.app_version.pristine_tag)
            if not compare_tags(self.app_version.wizard_tag):
                raise InconsistentWizardTagError(self.app_version.wizard_tag)
            parent = repo_rev_parse(self.app_version.wizard_tag)
            merge_base = shell.safeCall("git", "merge-base", parent, "HEAD", strip=True)
            if merge_base != parent:
                raise HeadNotDescendantError(self.app_version.wizard_tag)

    def verifyConfigured(self):
        """
        Checks if the autoinstall is configured running.
        """
        if not self.configured:
            raise NotConfiguredError(self.location)

    @chdir_to_location
    def verifyVersion(self):
        """
        Checks if our version and the version number recorded in a file
        are consistent.
        """
        real = self.detectVersion()
        if not str(real) == self.app_version.pristine_tag.partition('-')[2]:
            raise VersionMismatchError(real, self.version)

    @chdir_to_location
    def detectVersion(self):
        """
        Returns the real version, based on filesystem, of install.

        Throws a :class:`VersionDetectionError` if we couldn't figure out
        what the real version was.
        """
        real = self.application.detectVersion(self)
        if not real:
            raise VersionDetectionError
        return real

    @property
    @chdir_to_location
    def configured(self):
        """Whether or not an autoinstall has been configured/installed for use."""
        return self.application.checkConfig(self)
    @property
    def migrated(self):
        """Whether or not the autoinstalls has been migrated."""
        return os.path.isdir(self.wizard_dir)
    @property
    def wizard_dir(self):
        """The absolute path of the Wizard directory."""
        return os.path.join(self.location, ".wizard")
    @property
    def backup_dir(self):
        """The absolute path to ``.wizard/backups``."""
        return os.path.join(self.wizard_dir, "backups")
    # LEGACY
    @property
    def old_version_file(self):
        """
        The absolute path of either ``.scripts-version``.
        """
        return os.path.join(self.location, '.scripts-version')
    @property
    def blacklisted_file(self):
        """The absolute path of the ``.wizard/blacklisted`` file."""
        return os.path.join(self.wizard_dir, 'blacklisted')
    @property
    def pending_file(self):
        """The absolute path of the ``.wizard/pending`` file."""
        return os.path.join(self.wizard_dir, 'pending')
    @property
    def version_file(self):
        """The absolute path of the ``.wizard/version`` file."""
        return os.path.join(self.wizard_dir, 'version')
    @property
    def dsn_file(self):
        """The absolute path of the :file:`.wizard/dsn` override file."""
        return os.path.join(self.wizard_dir, 'dsn')
    @property
    def url_file(self):
        """The absolute path of the :file:`.wizard/url` override file."""
        return os.path.join(self.wizard_dir, 'url')
    @property
    def application(self):
        """The :class:`app.Application` of this deployment."""
        return self.app_version.application
    @property
    def old_log(self):
        """
        The :class:`wizard.old_log.Log` of this deployment.  This
        is only applicable to un-migrated autoinstalls.
        """
        if not self._old_log:
            self._old_log = old_log.DeployLog.load(self)
        return self._old_log
    @property
    def version(self):
        """
        The :class:`distutils.version.LooseVersion` of this
        deployment.
        """
        return self.app_version.version
    @property
    def app_version(self):
        """The :class:`app.ApplicationVersion` of this deployment."""
        if not self._app_version:
            if os.path.isdir(os.path.join(self.location, ".git")):
                try:
                    with util.ChangeDirectory(self.location):
                        appname, _, version = git.describe().partition('-')
                    self._app_version = app.ApplicationVersion.make(appname, version)
                except shell.CallError:
                    pass
        if not self._app_version:
            # LEGACY
            try:
                self._app_version = self.old_log[-1].version
            except old_log.ScriptsVersionNoSuchFile:
                pass
        if not self._app_version:
            appname = shell.eval("git", "config", "remote.origin.url").rpartition("/")[2].partition(".")[0]
            self._app_version = app.ApplicationVersion.make(appname, "unknown")
        return self._app_version
    @property
    def dsn(self):
        """The :class:`sqlalchemy.engine.url.URL` for this deployment."""
        if not self._dsn:
            self._dsn = sql.auth(self.application.dsn(self))
        return self._dsn
    @property
    def url(self):
        """The :class:`urlparse.ParseResult` for this deployment."""
        if not self._url:
            self.nextUrl()
        return self._url
    def nextUrl(self):
        """
        Initializes :attr:`url` with a possible URL the web application may
        be located at.  It may be called again to switch to another possible
        URL, usually in the event of a web access failure.
        """
        if not self._urlGen:
            self._urlGen = web(self.location, self.application.url(self))
        try:
            self._url = self._urlGen.next() # pylint: disable-msg=E1101
            return self._url
        except StopIteration:
            raise UnknownWebPath
    @staticmethod
    def parse(line):
        """
        Parses a line from the :term:`versions store`.

        .. note::

            Use this method only when speed is of the utmost
            importance.  You should prefer to directly create a deployment
            with only a ``location`` when possible.
        """
        line = line.rstrip()
        try:
            location, deploydir = line.split(":")
        except ValueError:
            return ProductionCopy(line) # lazy loaded version
        try:
            return ProductionCopy(location, version=app.ApplicationVersion.parse(deploydir))
        except Error as e:
            e.location = location
            raise e

class ProductionCopy(Deployment):
    """
    Represents the production copy of a deployment.  This copy
    is canonical, and is the only one guaranteed to be accessible
    via web, have a database, etc.
    """
    @chdir_to_location
    def upgrade(self, version, options):
        """
        Performs an upgrade of database schemas and other non-versioned data.
        """
        return self.application.upgrade(self, version, options)
    @chdir_to_location
    def backup(self, options):
        """
        Performs a backup of database schemas and other non-versioned data.
        """
        # There are retarded amounts of race-safety in this function,
        # because we do NOT want to claim to have made a backup, when
        # actually something weird happened to it.
        if not os.path.exists(self.backup_dir):
            try:
                os.mkdir(self.backup_dir)
            except OSError as e:
                if e.errno == errno.EEXIST:
                    pass
                else:
                    raise
        tmpdir = tempfile.mkdtemp() # actually will be kept around
        try:
            self.application.backup(self, tmpdir, options)
        except app.BackupFailure:
            # the backup is bogus, don't let it show up
            shutil.rmtree(tmpdir)
            raise
        backup = None
        with util.LockDirectory(os.path.join(self.backup_dir, "lock")):
            while 1:
                backup = str(self.version) + "-" + datetime.datetime.today().strftime("%Y-%m-%dT%H%M%S")
                outdir = os.path.join(self.backup_dir, backup)
                if os.path.exists(outdir):
                    logging.warning("Backup: A backup occurred in the last second. Trying again in a second...")
                    time.sleep(1)
                    continue
                try:
                    shutil.move(tmpdir, outdir)
                except:
                    # don't leave half-baked stuff lying around
                    try:
                        shutil.rmtree(outdir)
                    except OSError:
                        pass
                    raise
                break
        return backup
    @chdir_to_location
    def restore(self, backup, options):
        """
        Restores a backup. Destroys state, so be careful! Also, this does
        NOT restore the file-level backup, which is what 'wizard restore'
        does, so you probably do NOT want to call this elsewhere unless
        you know what you're doing (call 'wizard restore' instead).
        """
        return self.application.restore(self, os.path.join(self.backup_dir, backup), options)
    @chdir_to_location
    def remove(self, options):
        """
        Deletes all non-local or non-filesystem data (such as databases) that
        this application uses.
        """
        self.application.remove(self, options)
    def verifyDatabase(self):
        """
        Checks if the autoinstall has a properly configured database.
        """
        if not self.application.checkDatabase(self):
            raise DatabaseVerificationError
    def verifyWeb(self):
        """
        Checks if the autoinstall is viewable from the web.  If you do not run
        this, there is no guarantee that the url returned by this application
        is the correct one.
        """
        while True:
            if not self.application.checkWeb(self):
                try:
                    self.nextUrl()
                except UnknownWebPath:
                    raise WebVerificationError
            else:
                break
    def fetch(self, path, post=None):
        """
        Performs a HTTP request on the website.
        """
        return util.fetch(self.url.netloc, self.url.path, path, post) # pylint: disable-msg=E1103

class WorkingCopy(Deployment):
    """
    Represents a temporary clone of a deployment that we can make
    modifications to without fear of interfering with a production
    deployment.  More operations are permitted on these copies.
    """
    def setAppVersion(self, app_version):
        """
        Manually resets the application version; useful if the working
        copy is off in space (i.e. not anchored to something we can
        git describe off of.)
        """
        self._app_version = app_version
    @chdir_to_location
    def parametrize(self, deployment):
        """
        Edits files in ``dir`` to replace WIZARD_* variables with literal
        instances based on ``deployment``.  This is used for constructing
        virtual merge bases, and as such ``deployment`` will generally not
        equal ``self``.
        """
        return self.application.parametrize(self, deployment)
    @chdir_to_location
    def prepareConfig(self):
        """
        Edits files in the deployment such that any user-specific configuration
        is replaced with generic WIZARD_* variables.
        """
        return self.application.prepareConfig(self)
    @chdir_to_location
    def resolveConflicts(self):
        """
        Resolves conflicted files in this working copy.  Returns whether or
        not all conflicted files were resolved or not.  Fully resolved
        files are added to the index, but no commit is made.
        """
        return self.application.resolveConflicts(self)
    @chdir_to_location
    def prepareMerge(self):
        """
        Performs various edits to files in the current working directory in
        order to make a merge go more smoothly.  This is usually
        used to fix botched line-endings.
        """
        return self.application.prepareMerge(self)

## -- Exceptions --

class Error(wizard.Error):
    """Base error class for this module"""
    pass

# LEGACY
class NotMigratedError(Error):
    """
    The deployment contains a .scripts-version file, but no .git
    or .wizard directory.
    """
    #: Directory of deployment
    dir = None
    def __init__(self, dir):
        self.dir = dir
    def __str__(self):
        return """This installation was not migrated"""

class AlreadyVersionedError(Error):
    """The deployment contained a .git directory but no .wizard directory."""
    #: Directory of deployment
    dir = None
    def __init__(self, dir):
        self.dir = dir
    def __str__(self):
        return """

ERROR: Directory contains a .git directory, but not
a .wizard directory.  If this is not a corrupt
migration, this means that the user was versioning their
install using Git."""

class NotConfiguredError(Error):
    """The install was missing essential configuration."""
    #: Directory of unconfigured install
    dir = None
    def __init__(self, dir):
        self.dir = dir
    def __str__(self):
        return """

ERROR: The install was well-formed, but not configured
(essential configuration files were not found.)"""

class CorruptedAutoinstallError(Error):
    """The install was missing a .git directory, but had a .wizard directory."""
    #: Directory of the corrupted install
    dir = None
    def __init__(self, dir):
        self.dir = dir
    def __str__(self):
        return """

ERROR: Directory contains a .wizard directory,
but not a .git directory."""

class NotAutoinstallError(Error):
    """Application is not an autoinstall."""
    #: Directory of the not autoinstall
    dir = None
    def __init__(self, dir):
        self.dir = dir
    def __str__(self):
        return """

ERROR: The directory

    %s

does not appear to be an autoinstall.  If you are in a
subdirectory of an autoinstall, you need to use the root
directory for the autoinstall.""" % self.dir

class NoTagError(Error):
    """Deployment has a tag that does not have an equivalent in upstream repository."""
    #: Missing tag
    tag = None
    def __init__(self, tag):
        self.tag = tag
    def __str__(self):
        return """

ERROR: Could not find tag %s in repository.""" % self.tag

class NoLocalTagError(Error):
    """Could not find tag in local repository."""
    #: Missing tag
    tag = None
    def __init__(self, tag):
        self.tag = tag
    def __str__(self):
        return """

ERROR: Could not find tag %s in local repository.""" % self.tag

class InconsistentPristineTagError(Error):
    """Pristine tag commit ID does not match upstream pristine tag commit ID."""
    #: Inconsistent tag
    tag = None
    def __init__(self, tag):
        self.tag = tag
    def __str__(self):
        return """

ERROR: Local pristine tag %s did not match repository's.  This
probably means an upstream rebase occured.""" % self.tag

class InconsistentWizardTagError(Error):
    """Wizard tag commit ID does not match upstream wizard tag commit ID."""
    #: Inconsistent tag
    tag = None
    def __init__(self, tag):
        self.tag = tag
    def __str__(self):
        return """

ERROR: Local wizard tag %s did not match repository's.  This
probably means an upstream rebase occurred.""" % self.tag

class HeadNotDescendantError(Error):
    """HEAD is not connected to tag."""
    #: Tag that HEAD should have been descendant of.
    tag = None
    def __init__(self, tag):
        self.tag = tag
    def __str__(self):
        return """

ERROR: HEAD is not a descendant of %s.  This probably
means that an upstream rebase occurred, and new tags were
pulled, but local user commits were never rebased.""" % self.tag

class VersionDetectionError(Error):
    """Could not detect real version of application."""
    def __str__(self):
        return """

ERROR: Could not detect the real version of the application."""

class VersionMismatchError(Error):
    """Git version of application does not match detected version."""
    #: Detected version
    real_version = None
    #: Version from Git
    git_version = None
    def __init__(self, real_version, git_version):
        self.real_version = real_version
        self.git_version = git_version
    def __str__(self):
        return """

ERROR: The detected version %s did not match the Git
version %s.""" % (self.real_version, self.git_version)

class WebVerificationError(Error):
    """Could not access the application on the web"""
    def __str__(self):
        return """

ERROR: We were not able to access the application on the
web.  This may indicate that the website is behind
authentication on the htaccess level.  You can find
the contents of the page from the debug backtraces."""

class DatabaseVerificationError(Error):
    """Could not access the database"""
    def __str__(self):
        return """

ERROR: We were not able to access the database for
this application; this probably means that your database
configuration is misconfigured."""

class UnknownWebPath(Error):
    """Could not determine application's web path."""
    def __str__(self):
        return """

ERROR: We were not able to determine what the application's
host and path were in order to perform a web request
on the application.  You can specify this manually using
the WIZARD_WEB_HOST and WIZARD_WEB_PATH environment
variables."""
