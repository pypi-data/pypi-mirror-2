"""
Plumbing object model for representing applications we want to
install.  This module does the heavy lifting, but you probably
want to use :class:`wizard.deploy.Deployment` which is more user-friendly.
You'll need to know how to overload the :class:`Application` class
and use some of the functions in this module in order to specify
new applications.

To specify custom applications as plugins,  add the following ``entry_points``
configuration::

    [wizard.app]
    yourappname = your.module:Application
    otherappname = your.other.module:Application

.. note::

    Wizard will complain loudly if ``yourappname`` conflicts with an
    application name defined by someone else.

There are some submodules for programming languages that define common
functions and data that may be used by applications in that language.  See:

* :mod:`wizard.app.php`

.. testsetup:: *

    import re
    import shutil
    import os
    from wizard import deploy, util
    from wizard.app import *
"""

import os.path
import subprocess
import re
import distutils.version
import decorator
import shlex
import logging
import shutil
import sqlalchemy
import sqlalchemy.exc
import string
import urlparse
import tempfile
import pkg_resources

import wizard
from wizard import resolve, shell, sql, util

# SCRIPTS SPECIFIC
_scripts_application_list = [
    "mediawiki", "wordpress", "joomla", "e107", "gallery2",
    "phpBB", "advancedbook", "phpical", "trac", "turbogears", "django",
    "rails",
    # these are technically deprecated
    "advancedpoll", "gallery",
]
def _scripts_make(name):
    """Makes an application, but uses the correct subtype if available."""
    try:
        __import__("wizard.app." + name)
        return getattr(wizard.app, name).Application(name)
    except ImportError as error:
        # XXX ugly hack to check if the import error is from the top level
        # module we care about or a submodule. should be an archetectural change.
        if error.args[0].split()[-1]==name:
            return Application(name)
        else:
            raise

_applications = None
def applications():
    """Hash table for looking up string application name to instance"""
    global _applications
    if not _applications:
        # SCRIPTS SPECIFIC
        _applications = dict([(n,_scripts_make(n)) for n in _scripts_application_list ])
        # setup plugins
        for dist in pkg_resources.working_set:
            for appname, entry in dist.get_entry_map("wizard.app").items():
                if appname in _applications:
                    newname = dist.key + ":" + appname
                    if newname in _applications:
                        raise Exception("Unrecoverable application name conflict for %s from %s", appname, dist.key)
                    logging.warning("Could not overwrite %s, used %s instead", appname, newname)
                    appname = newname
                appclass = entry.load()
                _applications[appname] = appclass(appname)
    return _applications

def getApplication(appname):
    """Retrieves application instance given a name"""
    return applications()[appname]

class Application(object):
    """
    Represents an application, i.e. mediawiki or phpbb.

    .. note::
        Many of these methods assume a specific working
        directory; prefer using the corresponding methods
        in :class:`wizard.deploy.Deployment` and its subclasses.
    """
    #: String name of the application
    name = None
    #: Dictionary of version strings to :class:`ApplicationVersion`.
    #: See also :meth:`makeVersion`.
    versions = None
    #: List of files that need to be modified when parametrizing.
    #: This is a class-wide constant, and should not normally be modified.
    parametrized_files = []
    #: Keys that are used in older versions of the application, but
    #: not for the most recent version.
    deprecated_keys = set()
    #: Keys that we can simply generate random strings for if they're missing
    random_keys = set()
    #: Values that are not sufficiently random for a random key.  This can
    #: include default values for a random configuration option,
    random_blacklist = set()
    #: Dictionary of variable names to extractor functions.  These functions
    #: take a :class:`wizard.deploy.Deployment` as an argument and return the value of
    #: the variable, or ``None`` if it could not be found.
    #: See also :func:`filename_regex_extractor`.
    extractors = {}
    #: Dictionary of variable names to substitution functions.  These functions
    #: take a :class:`wizard.deploy.Deployment` as an argument and modify the deployment such
    #: that an explicit instance of the variable is released with the generic
    #: ``WIZARD_*`` constant.  See also :func:`filename_regex_substitution`.
    substitutions = {}
    #: Dictionary of file names to a list of resolutions, which are tuples of
    #: a conflict marker string and a result list.  See :mod:`wizard.resolve`
    #: for more information.
    resolutions = {}
    #: Instance of :class:`wizard.install.ArgSchema` that defines the arguments
    #: this application requires.
    install_schema = None
    #: Name of the database that this application uses, i.e. ``mysql`` or
    #: ``postgres``.  If we end up supporting multiple databases for a single
    #: application, there should also be a value for this in
    #: :class:`wizard.deploy.Deployment`; the value here is merely the preferred
    #: value.
    database = None
    #: Indicates whether or not a web stub is necessary.
    needs_web_stub = False
    def __init__(self, name):
        self.name = name
        self.versions = {}
        # cache variables
        self._extractors = {}
        self._substitutions = {}
    def repository(self, srv_path):
        """
        Returns the Git repository that would contain this application.
        ``srv_path`` corresponds to ``options.srv_path`` from the global baton.
        """
        repo = os.path.join(srv_path, self.name + ".git")
        if not os.path.isdir(repo):
            repo = os.path.join(srv_path, self.name, ".git")
            if not os.path.isdir(repo):
                raise NoRepositoryError(self.name)
        return repo
    def makeVersion(self, version):
        """
        Creates or retrieves the :class:`ApplicationVersion` singleton for the
        specified version.
        """
        if version not in self.versions:
            self.versions[version] = ApplicationVersion(distutils.version.LooseVersion(version), self)
        return self.versions[version]
    def extract(self, deployment):
        """
        Extracts wizard variables from a deployment.  Default implementation
        uses :attr:`extractors`.
        """
        result = {}
        for k,extractor in self.extractors.items():
            result[k] = extractor(deployment)
        # XXX: ugh... we have to do quoting
        for k in self.random_keys:
            if result[k] is None or result[k] in self.random_blacklist:
                result[k] = "'%s'" % util.random_key()
        return result
    def dsn(self, deployment):
        """
        Returns the deployment specific database URL.  Uses the override file
        in :file:`.wizard` if it exists, and otherwise attempt to extract the
        variables from the source files.

        Under some cases, the database URL will contain only the database
        property, and no other values.  This indicates that the actual DSN
        should be determined from the environment.

        This function might return ``None``.

        .. note::

            We are allowed to batch these two together, because the full precedence
            chain for determining the database of an application combines these
            two together.  If this was not the case, we would have to call
            :meth:`databaseUrlFromOverride` and :meth:`databaseUrlFromExtract` manually.
        """
        url = self.dsnFromOverride(deployment)
        if url:
            return url
        return self.dsnFromExtract(deployment)
    def dsnFromOverride(self, deployment):
        """
        Extracts database URL from an explicit dsn override file.
        """
        try:
            return sqlalchemy.engine.url.make_url(open(deployment.dsn_file).read().strip())
        except IOError:
            return None
    def dsnFromExtract(self, deployment):
        """
        Extracts database URL from a deployment, and returns them as
        a :class:`sqlalchemy.engine.url.URL`.  Returns ``None`` if we
        can't figure it out: i.e. the conventional variables are not defined
        for this application.
        """
        if not self.database:
            return None
        vars = self.extract(deployment)
        names = ("WIZARD_DBSERVER", "WIZARD_DBUSER", "WIZARD_DBPASSWORD", "WIZARD_DBNAME")
        host, user, password, database = (shlex.split(vars[x])[0] if vars[x] is not None else None for x in names)
        # XXX: You'd have to put support for an explicit different database
        # type here
        return sqlalchemy.engine.url.URL(self.database, username=user, password=password, host=host, database=database)
    def url(self, deployment):
        """
        Returns the deployment specific web URL.  Uses the override file
        in :file:`.wizard` if it exists, and otherwise attempt to extract
        the variables from the source files.

        This function might return ``None``, which indicates we couldn't figure
        it out.
        """
        url = self.urlFromOverride(deployment)
        if url:
            return url
        return self.urlFromExtract(deployment)
    def urlFromOverride(self, deployment):
        """
        Extracts URL from explicit url override file.
        """
        try:
            return urlparse.urlparse(open(deployment.url_file).read().strip())
        except IOError:
            return None
    def urlFromExtract(self, deployment):
        """
        Extracts URL from a deployment, and returns ``None`` if we can't
        figure it out.  Default implementation is to fail; we might
        do something clever with extractable variables in the future.
        """
        return None
    def parametrize(self, deployment, ref_deployment):
        """
        Takes a generic source checkout and parametrizes it according to the
        values of ``deployment``.  This function operates on the current
        working directory.  ``deployment`` should **not** be the same as the
        current working directory.  See :meth:`parametrizeWithVars` for details
        on the parametrization.
        """
        # deployment is not used in this implementation, but note that
        # we do have the invariant the current directory matches
        # deployment's directory
        variables = ref_deployment.extract()
        self.parametrizeWithVars(variables)
    def parametrizeWithVars(self, variables):
        """
        Takes a generic source checkout and parametrizes it according to
        the values of ``variables``.  Default implementation uses
        :attr:`parametrized_files` and a simple search and replace on
        those files.
        """
        for file in self.parametrized_files:
            logging.debug("Parametrizing file '%s'\n" % (file, ))
            try:
                contents = open(file, "r").read()
            except IOError:
                logging.debug("Failed to open file '%s'\n" % (file, ))
                continue
            for key, value in variables.items():
                if value is None: continue
                contents = contents.replace(key, value)
            f = open(file, "w")
            f.write(contents)
    def resolveConflicts(self, deployment):
        """
        Resolves conflicted files in the current working directory.  Returns
        whether or not all conflicted files were resolved or not.  Fully
        resolved files are added to the index, but no commit is made.  The
        default implementation uses :attr:`resolutions`.
        """
        resolved = True
        files = set()
        files = {}
        for status in shell.eval("git", "ls-files", "--unmerged").splitlines():
            mode, hash, role, name = status.split()
            files.setdefault(name, set()).add(int(role))
        for file, roles in files.items():
            # some automatic resolutions
            if 1 not in roles and 2 not in roles and 3 in roles:
                # upstream added a file, but it conflicted for whatever reason
                shell.call("git", "add", file)
                continue
            elif 1 in roles and 2 not in roles and 3 in roles:
                # user deleted the file, but upstream changed it
                shell.call("git", "rm", file)
                continue
            # manual resolutions
            # XXX: this functionality is mostly subsumed by the rerere
            # tricks we do
            if file in self.resolutions:
                contents = open(file, "r").read()
                for spec, result in self.resolutions[file]:
                    old_contents = contents
                    contents = resolve.resolve(contents, spec, result)
                    if old_contents != contents:
                        logging.info("Did resolution with spec:\n" + spec)
                open(file, "w").write(contents)
                if not resolve.is_conflict(contents):
                    shell.call("git", "add", file)
                else:
                    resolved = False
            else:
                resolved = False
        return resolved
    def prepareMerge(self, deployment):
        """
        Performs various edits to files in the current working directory in
        order to make a merge go more smoothly.  This is usually
        used to fix botched line-endings.  If you add new files,
        you have to 'git add' them; this is not necessary for edits.
        By default this is a no-op; subclasses should replace this
        with useful behavior.
        """
        pass
    def prepareConfig(self, deployment):
        """
        Takes a deployment and replaces any explicit instances
        of a configuration variable with generic ``WIZARD_*`` constants.
        The default implementation uses :attr:`substitutions`, and
        emits warnings when it encounters keys in :attr:`deprecated_keys`.
        """
        for key, subst in self.substitutions.items():
            subs = subst(deployment)
            if not subs and key not in self.deprecated_keys and key not in self.random_keys:
                logging.warning("No substitutions for %s" % key)
    def install(self, version, options):
        """
        Run for 'wizard configure' (and, by proxy, 'wizard install') to
        configure an application.  This assumes that the current working
        directory is a deployment.  (Unlike its kin, this function does not
        take a :class:`wizard.deploy.Deployment` as a parameter.)  Subclasses should
        provide an implementation.
        """
        raise NotImplementedError
    def upgrade(self, deployment, version, options):
        """
        Run for 'wizard upgrade' to upgrade database schemas and other
        non-versioned data in an application after the filesystem has been
        upgraded.  This assumes that the current working directory is the
        deployment.  Subclasses should provide an implementation.
        """
        raise NotImplementedError
    def backup(self, deployment, outdir, options):
        """
        Run for 'wizard backup' and upgrades to backup database schemas
        and other non-versioned data in an application.  ``outdir`` is
        the directory that backup files should be placed.  This assumes
        that the current working directory is the deployment.  Subclasses
        should provide an implementation, even if it is a no-op.

        .. note::
            Static user files may not need to be backed up, since in
            many applications upgrades do not modify static files.
        """
        raise NotImplementedError
    def restore(self, deployment, backup_dir, options):
        """
        Run for 'wizard restore' and failed upgrades to restore database
        and other non-versioned data to a backed up version.  This assumes
        that the current working directory is the deployment.  Subclasses
        should provide an implementation.
        """
        raise NotImplementedError
    def remove(self, deployment, options):
        """
        Run for 'wizard remove' to delete all database and non-local
        file data.  This assumes that the current working directory is
        the deployment.  Subclasses should provide an implementation.
        """
        raise NotImplementedError
    def detectVersion(self, deployment):
        """
        Checks source files to determine the version manually.  This assumes
        that the current working directory is the deployment.  Subclasses
        should provide an implementation.
        """
        raise NotImplementedError
    def detectVersionFromFile(self, filename, regex):
        """
        Helper method that detects a version by using a regular expression
        from a file.  The regexed value is passed through :mod:`shlex`.
        This assumes that the current working directory is the deployment.
        """
        contents = open(filename).read()
        match = regex.search(contents)
        if not match: return None
        return distutils.version.LooseVersion(shlex.split(match.group(2))[0])
    # XXX: This signature doesn't really make too much sense...
    def detectVersionFromGit(self, tagPattern, preStrip = ''):
        """
        Helper method that detects a version by using the most recent tag
        in git that matches the specified pattern.
        This assumes that the current working directory is the deployment.
        """
        sh = wizard.shell.Shell()
        cmd = ['git', 'describe', '--tags', '--match', tagPattern, ]
        tag = sh.call(*cmd, strip=True)
        if tag and len(tag) > len(preStrip) and tag[:len(preStrip)] == preStrip:
            tag = tag[len(preStrip):]
        if not tag: return None
        return distutils.version.LooseVersion(tag)
    def download(self, version):
        """
        Returns a URL that can be used to download a tarball of ``version`` of
        this application.
        """
        raise NotImplementedError
    def checkWeb(self, deployment):
        """
        Checks if the autoinstall is viewable from the web.  Subclasses should
        provide an implementation.

        .. note::
            Finding a reasonable heuristic that works across skinning
            choices can be difficult.  We've had reasonable success
            searching for metadata.  Be sure that the standard error
            page does not contain the features you search for.  Try
            not to depend on pages that are not the main page.
        """
        raise NotImplementedError
    def checkDatabase(self, deployment):
        """
        Checks if the database is accessible.
        """
        try:
            sql.connect(deployment.dsn)
            return True
        except sqlalchemy.exc.DBAPIError:
            return False
    def checkWebPage(self, deployment, page, outputs=[], exclude=[]):
        """
        Checks if a given page of an autoinstall contains a particular string.
        """
        page = deployment.fetch(page)
        for x in exclude:
            if page.find(x) != -1:
                logging.info("checkWebPage (failed due to %s):\n\n%s", x, page)
                return False
        votes = 0
        for output in outputs:
            votes += page.find(output) != -1
        if votes > len(outputs) / 2:
            logging.debug("checkWebPage (passed):\n\n" + page)
            return True
        else:
            logging.info("checkWebPage (failed):\n\n" + page)
            return False
    def checkConfig(self, deployment):
        """
        Checks whether or not an autoinstall has been configured/installed
        for use.  Assumes that the current working directory is the deployment.
        Subclasses should provide an implementation.
        """
        # XXX: Unfortunately, this doesn't quite work because we package
        # bogus config files.  Maybe we should check a hash or
        # something?
        raise NotImplementedError
    def researchFilter(self, filename, added, deleted):
        """
        Allows an application to selectively ignore certain diffstat signatures
        during research; for example, configuration files will have a very
        specific set of changes, so ignore them; certain installation files
        may be removed, etc.  Return ``True`` if a diffstat signature should be
        ignored,
        """
        return False
    def researchVerbose(self, filename):
        """
        Allows an application to exclude certain dirty files from the output
        report; usually this will just be parametrized files, since those are
        guaranteed to have changes.  Return ``True`` if a file should only
        be displayed in verbose mode.
        """
        return filename in self.parametrized_files

class ApplicationVersion(object):
    """Represents an abstract notion of a version for an application, where
    ``version`` is a :class:`distutils.version.LooseVersion` and
    ``application`` is a :class:`Application`."""
    #: The :class:`distutils.version.LooseVersion` of this instance.
    version = None
    #: The :class:`Application` of this instance.
    application = None
    def __init__(self, version, application):
        self.version = version
        self.application = application
    @property
    def tag(self):
        """
        Returns the name of the git describe tag for the commit the user is
        presently on, something like mediawiki-1.2.3-scripts-4-g123abcd
        """
        return "%s-%s" % (self.application, self.version)
    @property
    def wizard_tag(self):
        """
        Returns the name of the Git tag for this version.
        """
        # XXX: Scripts specific
        end = str(self.version).partition('-scripts')[2].partition('-')[0]
        return "%s-scripts%s" % (self.pristine_tag, end)
    @property
    def pristine_tag(self):
        """
        Returns the name of the Git tag for the pristine version corresponding
        to this version.
        """
        return "%s-%s" % (self.application.name, str(self.version).partition('-scripts')[0])
    def __cmp__(self, y):
        return cmp(self.version, y.version)
    @staticmethod
    def parse(value):
        """
        Parses a line from the :term:`versions store` and return
        :class:`ApplicationVersion`.

        Use this only for cases when speed is of primary importance;
        the data in version is unreliable and when possible, you should
        prefer directly instantiating a :class:`wizard.deploy.Deployment` and having it query
        the autoinstall itself for information.

        The `value` to parse will vary.  For old style installs, it
        will look like::

           /afs/athena.mit.edu/contrib/scripts/deploy/APP-x.y.z

        For new style installs, it will look like::

           APP-x.y.z-scripts
        """
        name = value.split("/")[-1]
        try:
            if name.find("-") != -1:
                app, _, version = name.partition("-")
            else:
                # kind of poor, maybe should error.  Generally this
                # will actually result in a not found error
                app = name
                version = "trunk"
        except ValueError:
            raise DeploymentParseError(value)
        return ApplicationVersion.make(app, version)
    @staticmethod
    def make(app, version):
        """
        Makes/retrieves a singleton :class:`ApplicationVersion` from
        a``app`` and ``version`` string.
        """
        try:
            # defer to the application for version creation to enforce
            # singletons
            return applications()[app].makeVersion(version)
        except KeyError:
            raise NoSuchApplication(app)

def expand_re(val):
    """
    Takes a tree of values (implement using nested lists) and
    transforms them into regular expressions.

        >>> expand_re('*')
        '\\\\*'
        >>> expand_re(['a', 'b'])
        '(?:a|b)'
        >>> expand_re(['*', ['b', 'c']])
        '(?:\\\\*|(?:b|c))'
    """
    if isinstance(val, str):
        return re.escape(val)
    else:
        return '(?:' + '|'.join(map(expand_re, val)) + ')'

def make_extractors(seed):
    """
    Take a dictionary of ``key`` to ``(file, regex)`` tuples and convert them into
    extractor functions (which take a :class:`wizard.deploy.Deployment`
    and return the value of the second subpattern of ``regex`` when matched
    with the contents of ``file``).
    """
    return util.dictmap(lambda a: filename_regex_extractor(*a), seed)

def make_substitutions(seed):
    """
    Take a dictionary of ``key`` to ``(file, regex)`` tuples and convert them into substitution
    functions (which take a :class:`wizard.deploy.Deployment`, replace the second subpattern
    of ``regex`` with ``key`` in ``file``, and returns the number of substitutions made.)
    """
    return util.dictkmap(lambda k, v: filename_regex_substitution(k, *v), seed)

# The following two functions are *highly* functional, and I recommend
# not touching them unless you know what you're doing.

def filename_regex_extractor(file, regex):
    """
    .. highlight:: haskell

    Given a relative file name ``file``, a regular expression ``regex``, and a
    :class:`wizard.deploy.Deployment` extracts a value out of the file in that
    deployment.  This function is curried, so you pass just ``file`` and
    ``regex``, and then pass ``deployment`` to the resulting function.

    Its Haskell-style type signature would be::

        Filename -> Regex -> (Deployment -> String)

    The regular expression requires a very specific form, essentially ``()()()``
    (with the second subgroup being the value to extract).  These enables
    the regular expression to be used equivalently with filename

    .. highlight:: python

    For convenience purposes, we also accept ``[Filename]``, in which case
    we use the first entry (index 0).  Passing an empty list is invalid.

        >>> open("test-settings.extractor.ini", "w").write("config_var = 3\\n")
        >>> f = filename_regex_extractor('test-settings.extractor.ini', re.compile('^(config_var\s*=\s*)(.*)()$'))
        >>> f(deploy.Deployment("."))
        '3'
        >>> os.unlink("test-settings.extractor.ini")

    .. note::
        The first application of ``regex`` and ``file`` is normally performed
        at compile-time inside a submodule; the second application is
        performed at runtime.
    """
    if not isinstance(file, str):
        file = file[0]
    def h(deployment):
        try:
            contents = deployment.read(file) # cached
        except IOError:
            return None
        match = regex.search(contents)
        if not match: return None
        # assumes that the second match is the one we want.
        return match.group(2)
    return h

def filename_regex_substitution(key, files, regex):
    """
    .. highlight:: haskell

    Given a Wizard ``key`` (``WIZARD_*``), a list of ``files``, a
    regular expression ``regex``, and a :class:`wizard.deploy.Deployment`
    performs a substitution of the second subpattern of ``regex``
    with ``key``.  Returns the number of replacements made.  This function
    is curried, so you pass just ``key``, ``files`` and ``regex``, and
    then pass ``deployment`` to the resulting function.

    Its Haskell-style type signature would be::

        Key -> ([File], Regex) -> (Deployment -> IO Int)

    .. highlight:: python

    For convenience purposes, we also accept ``Filename``, in which case it is treated
    as a single item list.

        >>> open("test-settings.substitution.ini", "w").write("config_var = 3")
        >>> f = filename_regex_substitution('WIZARD_KEY', 'test-settings.substitution.ini', re.compile('^(config_var\s*=\s*)(.*)()$'))
        >>> f(deploy.Deployment("."))
        1
        >>> print open("test-settings.substitution.ini", "r").read()
        config_var = WIZARD_KEY
        >>> os.unlink("test-settings.substitution.ini")
    """
    if isinstance(files, str):
        files = (files,)
    def h(deployment):
        base = deployment.location
        subs = 0
        for file in files:
            file = os.path.join(base, file)
            try:
                contents = open(file, "r").read()
                contents, n = regex.subn("\\1" + key + "\\3", contents)
                subs += n
                open(file, "w").write(contents)
            except IOError:
                pass
        return subs
    return h

def backup_database(outdir, deployment):
    """
    Generic database backup function for MySQL.
    """
    # XXX: Change this once deployments support multiple dbs
    if deployment.application.database == "mysql":
        return backup_mysql_database(outdir, deployment)
    else:
        raise NotImplementedError

def backup_mysql_database(outdir, deployment):
    """
    Database backups for MySQL using the :command:`mysqldump` utility.
    """
    outfile = os.path.join(outdir, "db.sql")
    try:
        shell.call("mysqldump", "--compress", "-r", outfile, *get_mysql_args(deployment.dsn))
        shell.call("gzip", "--best", outfile)
    except shell.CallError as e:
        raise BackupFailure(e.stderr)

def restore_database(backup_dir, deployment):
    """
    Generic database restoration function for MySQL.
    """
    # XXX: see backup_database
    if deployment.application.database == "mysql":
        return restore_mysql_database(backup_dir, deployment)
    else:
        raise NotImplementedError

def restore_mysql_database(backup_dir, deployment):
    """
    Database restoration for MySQL by piping SQL commands into :command:`mysql`.
    """
    if not os.path.exists(backup_dir):
        raise RestoreFailure("Backup %s doesn't exist", backup_dir.rpartition("/")[2])
    sql = open(os.path.join(backup_dir, "db.sql"), 'w+')
    shell.call("gunzip", "-c", os.path.join(backup_dir, "db.sql.gz"), stdout=sql)
    sql.seek(0)
    shell.call("mysql", *get_mysql_args(deployment.dsn), stdin=sql)
    sql.close()

# XXX: SCRIPTS
def remove_database(deployment):
    """
    Generic database removal function.  Actually, not so generic because we
    go and check if we're on scripts and if we are run a different command.
    """
    if deployment.dsn.host == "sql.mit.edu":
        try:
            shell.call("/mit/scripts/sql/bin/drop-database", deployment.dsn.database)
            return
        except shell.CallError:
            pass
    engine = sqlalchemy.create_engine(deployment.dsn)
    engine.execute("DROP DATABASE `%s`" % deployment.dsn.database)

def get_mysql_args(dsn):
    """
    Extracts arguments that would be passed to the command line mysql utility
    from a deployment.
    """
    args = []
    if dsn.host:
        args += ["-h", dsn.host]
    if dsn.username:
        args += ["-u", dsn.username]
    if dsn.password:
        args += ["-p" + dsn.password]
    args += [dsn.database]
    return args

class Error(wizard.Error):
    """Generic error class for this module."""
    pass

class NoRepositoryError(Error):
    """
    :class:`Application` does not appear to have a Git repository
    in the normal location.
    """
    #: The name of the application that does not have a Git repository.
    app = None
    def __init__(self, app):
        self.app = app
    def __str__(self):
        return """Could not find Git repository for '%s'.  If you would like to use a local version, try specifying --srv-path or WIZARD_SRV_PATH.""" % self.app

class DeploymentParseError(Error):
    """
    Could not parse ``value`` from :term:`versions store`.
    """
    #: The value that failed to parse.
    value = None
    #: The location of the autoinstall that threw this variable.
    #: This should be set by error handling code when it is available.
    location = None
    def __init__(self, value):
        self.value = value

class NoSuchApplication(Error):
    """
    You attempted to reference a :class:`Application` named
    ``app``, which is not recognized by Wizard.
    """
    #: The name of the application that does not exist.
    app = None
    #: The location of the autoinstall that threw this variable.
    #: This should be set by error handling code when it is availble.
    location = None
    def __init__(self, app):
        self.app = app

class Failure(Error):
    """
    Represents a failure when performing some double-dispatched operation
    such as an installation or an upgrade.  Failure classes are postfixed
    with Failure, not Error.
    """
    pass

class InstallFailure(Error):
    """Installation failed for unknown reason."""
    def __str__(self):
        return """

ERROR: Installation failed for unknown reason.  You can
retry the installation by appending --retry to the installation
command."""

class RecoverableInstallFailure(InstallFailure):
    """
    Installation failed, but we were able to determine what the
    error was, and should give the user a second chance if we were
    running interactively.
    """
    #: List of the errors that were found.
    errors = None
    def __init__(self, errors):
        self.errors = errors
    def __str__(self):
        return """

ERROR: Installation failed due to the following errors:  %s

You can retry the installation by appending --retry to the
installation command.""" % ", ".join(self.errors)

class UpgradeFailure(Failure):
    """Upgrade script failed."""
    #: String details of failure (possibly stdout or stderr output)
    details = None
    def __init__(self, details):
        self.details = details
    def __str__(self):
        return """

ERROR: Upgrade script failed, details:

%s""" % self.details

class UpgradeVerificationFailure(Failure):
    """Upgrade script passed, but website wasn't accessible afterwards"""
    def __str__(self):
        return """

ERROR: Upgrade script passed, but website wasn't accessible afterwards.  Check
the debug logs for the contents of the page."""

class BackupFailure(Failure):
    """Backup script failed."""
    #: String details of failure
    details = None
    def __init__(self, details):
        self.details = details
    def __str__(self):
        return """

ERROR: Backup script failed, details:

%s""" % self.details

class RestoreFailure(Failure):
    """Restore script failed."""
    #: String details of failure
    details = None
    def __init__(self, details):
        self.details = details
    def __str__(self):
        return """

ERROR: Restore script failed, details:

%s""" % self.details

class RemoveFailure(Failure):
    """Remove script failed."""
    #: String details of failure
    details = None
    def __init__(self, details):
        self.details = details
    def __str__(self):
        return """

ERROR: Remove script failed, details:

%s""" % self.details
