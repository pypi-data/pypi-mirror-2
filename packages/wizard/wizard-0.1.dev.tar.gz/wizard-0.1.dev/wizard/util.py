"""
Miscellaneous utility functions and classes.

.. testsetup:: *

    from wizard.util import *
"""

import os.path
import os
import subprocess
import pwd
import sys
import socket
import errno
import itertools
import signal
import httplib
import urllib
import time
import logging
import random
import string

import wizard
from wizard import user

def boolish(val):
    """
    Parse the contents of an environment variable as a boolean.
    This recognizes more values as ``False`` than :func:`bool` would.

        >>> boolish("0")
        False
        >>> boolish("no")
        False
        >>> boolish("1")
        True
    """
    try:
        return bool(int(val))
    except (ValueError, TypeError):
        if val == "No" or val == "no" or val == "false" or val == "False":
            return False
        return bool(val)

class ChangeDirectory(object):
    """
    Context for temporarily changing the working directory.

        >>> with ChangeDirectory("/tmp"):
        ...    print os.getcwd()
        /tmp
    """
    def __init__(self, dir):
        self.dir = dir
        self.olddir = None
    def __enter__(self):
        self.olddir = os.getcwd()
        chdir(self.dir)
    def __exit__(self, *args):
        chdir(self.olddir)

class Counter(object):
    """
    Object for counting different values when you don't know what
    they are a priori.  Supports index access and iteration.

        >>> counter = Counter()
        >>> counter.count("foo")
        >>> print counter["foo"]
        1
    """
    def __init__(self):
        self.dict = {}
    def count(self, value):
        """Increments count for ``value``."""
        self.dict.setdefault(value, 0)
        self.dict[value] += 1
    def __getitem__(self, key):
        return self.dict[key]
    def __iter__(self):
        return self.dict.__iter__()
    def max(self):
        """Returns the max counter value seen."""
        return max(self.dict.values())
    def sum(self):
        """Returns the sum of all counter values."""
        return sum(self.dict.values())
    def keys(self):
        """Returns the keys of counters."""
        return self.dict.keys()

class PipeToLess(object):
    """
    Context for printing output to a pager.  Use this if output
    is expected to be long.
    """
    def __enter__(self):
        self.proc = subprocess.Popen("less", stdin=subprocess.PIPE)
        self.old_stdout = sys.stdout
        sys.stdout = self.proc.stdin
    def __exit__(self, *args):
        if self.proc:
            self.proc.stdin.close()
            self.proc.wait()
            sys.stdout = self.old_stdout

class IgnoreKeyboardInterrupts(object):
    """
    Context for temporarily ignoring keyboard interrupts.  Use this
    if aborting would cause more harm than finishing the job.
    """
    def __enter__(self):
        signal.signal(signal.SIGINT,signal.SIG_IGN)
    def __exit__(self, *args):
        signal.signal(signal.SIGINT, signal.default_int_handler)

class LockDirectory(object):
    """
    Context for locking a directory.
    """
    def __init__(self, lockfile, expiry = 3600):
        self.lockfile = lockfile
        self.expiry = expiry # by default an hour
    def __enter__(self):
        # It's A WAVY
        for i in range(0, 3):
            try:
                os.open(self.lockfile, os.O_CREAT | os.O_EXCL)
                open(self.lockfile, "w").write("%d" % os.getpid())
            except OSError as e:
                if e.errno == errno.EEXIST:
                    # There is a possibility of infinite recursion, but we
                    # expect it to be unlikely, and not harmful if it does happen
                    with LockDirectory(self.lockfile + "_"):
                        # See if we can break the lock
                        try:
                            pid = open(self.lockfile, "r").read().strip()
                            if not os.path.exists("/proc/%s" % pid):
                                # break the lock, try again
                                logging.warning("Breaking orphaned lock at %s", self.lockfile)
                                os.unlink(self.lockfile)
                                continue
                            try:
                                # check if the file is expiry old, if so, break the lock, try again
                                if time.time() - os.stat(self.lockfile).st_mtime > self.expiry:
                                    logging.warning("Breaking stale lock at %s", self.lockfile)
                                    os.unlink(self.lockfile)
                                    continue
                            except OSError as e:
                                if e.errno == errno.ENOENT:
                                    continue
                                raise
                        except IOError:
                            # oh hey, it went away; try again
                            continue
                    raise DirectoryLockedError(os.getcwd())
                elif e.errno == errno.EACCES:
                    raise PermissionsError(os.getcwd())
                raise
            return
        raise DirectoryLockedError(os.getcwd())
    def __exit__(self, *args):
        try:
            os.unlink(self.lockfile)
        except OSError:
            pass

def chdir(dir):
    """
    Changes a directory, but has special exceptions for certain
    classes of errors.
    """
    try:
        os.chdir(dir)
    except OSError as e:
        if e.errno == errno.EACCES:
            raise PermissionsError()
        elif e.errno == errno.ENOENT:
            raise NoSuchDirectoryError()
        else: raise e

def dictmap(f, d):
    """
    A map function for dictionaries.  Only changes values.

        >>> dictmap(lambda x: x + 2, {'a': 1, 'b': 2})
        {'a': 3, 'b': 4}
    """
    return dict((k,f(v)) for k,v in d.items())

def dictkmap(f, d):
    """
    A map function for dictionaries that passes key and value.

        >>> dictkmap(lambda x, y: x + y, {1: 4, 3: 4})
        {1: 5, 3: 7}
    """
    return dict((k,f(k,v)) for k,v in d.items())

def get_exception_name(output):
    """
    Reads the traceback from a Python program and grabs the
    fully qualified exception name.
    """
    lines = output.split("\n")
    cue = False
    result = "(unknown)"
    for line in lines[1:]:
        line = line.rstrip()
        if not line: continue
        if line[0] == ' ':
            cue = True
            continue
        if cue:
            cue = False
            return line.partition(':')[0]
    return result

def get_dir_uid(dir):
    """Finds the uid of the person who owns this directory."""
    return os.stat(dir).st_uid

def get_revision():
    """Returns the commit ID of the current Wizard install."""
    # If you decide to convert this to use wizard.shell, be warned
    # that there is a circular dependency, so this function would
    # probably have to live somewhere else, probably wizard.git
    wizard_git = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".git")
    return subprocess.Popen(["git", "--git-dir=" + wizard_git, "rev-parse", "HEAD"], stdout=subprocess.PIPE).communicate()[0].rstrip()

def get_operator_git():
    """
    Returns ``Real Name <username@mit.edu>`` suitable for use in
    Git ``Something-by:`` string.  Throws :exc:`NoOperatorInfo` if
    no operator information is available.
    """
    op = user.operator()
    if op is None:
        raise NoOperatorInfo
    info = user.pwnam(op)
    return "%s <%s>" % (info.realname, info.email)

def set_operator_env():
    """
    Sets :envvar:`GIT_COMMITTER_NAME` and :envvar:`GIT_COMMITTER_EMAIL`
    environment variables if applicable.  Does nothing if no information
    is available
    """
    op = user.operator()
    if op is None:
        return
    info = user.pwnam(op)
    os.putenv("GIT_COMMITTER_NAME", info.realname)
    os.putenv("GIT_COMMITTER_EMAIL", info.email)

def set_author_env():
    """
    Sets :envvar:`GIT_AUTHOR_NAME` and :envvar:`GIT_AUTHOR_EMAIL`
    environment variables if applicable. Does nothing if
    :func:`wizard.user.passwd` fails.
    """
    info = user.passwd()
    if info is None:
        return
    os.putenv("GIT_AUTHOR_NAME", "%s" % info.realname)
    os.putenv("GIT_AUTHOR_EMAIL", "%s" % info.email)

def set_git_env():
    """Sets all appropriate environment variables for Git commits."""
    set_operator_env()
    set_author_env()

def get_git_footer():
    """Returns strings for placing in Git log info about Wizard."""
    return "\n".join(["Wizard-revision: %s" % get_revision()
        ,"Wizard-args: %s" % " ".join(sys.argv)
        ])

def safe_unlink(file):
    """Moves a file/dir to a backup location."""
    if not os.path.lexists(file):
        return None
    prefix = "%s.bak" % file
    name = None
    for i in itertools.count():
        name = "%s.%d" % (prefix, i)
        if not os.path.lexists(name):
            break
    os.rename(file, name)
    return name

def soft_unlink(file):
    """Unlink a file, but don't complain if it doesn't exist."""
    try:
        os.unlink(file)
    except OSError:
        pass

def makedirs(path):
    """
    Create a directory path (a la ``mkdir -p`` or ``os.makedirs``),
    but don't complain if it already exists.
    """
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST:
            pass
        else:
            raise

def fetch(host, path, subpath, post=None):
    try:
        # XXX: Should use urllib instead
        h = httplib.HTTPConnection(host)
        fullpath = path.rstrip("/") + "/" + subpath.lstrip("/") # to be lenient about input we accept
        if post:
            headers = {"Content-type": "application/x-www-form-urlencoded"}
            logging.info("POST request to http://%s%s", host, fullpath)
            logging.debug("POST contents:\n" + urllib.urlencode(post))
            h.request("POST", fullpath, urllib.urlencode(post), headers)
        else:
            logging.info("GET request to http://%s%s", host, fullpath)
            h.request("GET", fullpath)
        r = h.getresponse()
        data = r.read()
        h.close()
        return data
    except socket.gaierror as e:
        if e.errno == socket.EAI_NONAME:
            raise DNSError(host)
        else:
            raise

def mixed_newlines(filename):
    """Returns ``True`` if ``filename`` has mixed newlines."""
    f = open(filename, "U") # requires universal newline support
    f.read()
    ret = isinstance(f.newlines, tuple)
    f.close() # just to be safe
    return ret

def disk_usage(dir=None, excluded_dir=".git"):
    """
    Recursively determines the disk usage of a directory, excluding
    .git directories.  Value is in bytes.  If ``dir`` is omitted, the
    current working directory is assumed.
    """
    if dir is None: dir = os.getcwd()
    sum_sizes = 0
    for root, _, files in os.walk(dir):
        for name in files:
            if not os.path.join(root, name).startswith(os.path.join(dir, excluded_dir)):
                file = os.path.join(root, name)
                try:
                    if os.path.islink(file): continue
                    sum_sizes += os.path.getsize(file)
                except OSError as e:
                    if e.errno == errno.ENOENT:
                        logging.warning("%s disappeared before we could stat", file)
                    else:
                        raise
    return sum_sizes

def random_key(length=30):
    """Generates a random alphanumeric key of ``length`` size."""
    return ''.join(random.choice(string.letters + string.digits) for i in xrange(length))

def truncate(version):
    """Truncates the Scripts specific version number."""
    return str(version).partition('-scripts')[0]

def init_wizard_dir():
    """
    Generates a .wizard directory and initializes it with some common
    files.  This operation is idempotent.
    """
    # no harm in doing this repeatedly
    wizard_dir = ".wizard"
    if not os.path.isdir(wizard_dir):
        os.mkdir(wizard_dir)
    open(os.path.join(wizard_dir, ".htaccess"), "w").write("Deny from all\n")
    open(os.path.join(wizard_dir, ".gitignore"), "w").write("*\n")

class NoOperatorInfo(wizard.Error):
    """No information could be found about the operator from Kerberos."""
    pass

class PermissionsError(IOError):
    errno = errno.EACCES

class NoSuchDirectoryError(IOError):
    errno = errno.ENOENT

class DirectoryLockedError(wizard.Error):
    def __init__(self, dir):
        self.dir = dir
    def __str__(self):
        return """

ERROR: Could not acquire lock on directory.  Maybe there is
another migration process running?
"""

class DNSError(socket.gaierror):
    errno = socket.EAI_NONAME
    #: Hostname that could not resolve name
    host = None
    def __init__(self, host):
        self.host = host
    def __str__(self):
        return """

ERROR: Could not resolve hostname %s.
""" % self.host
