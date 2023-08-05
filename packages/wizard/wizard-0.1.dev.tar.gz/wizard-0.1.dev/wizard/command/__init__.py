import logging
import traceback
import os
import sys
import optparse
import errno
import pwd
import shutil
import cStringIO

import wizard
from wizard import util

logging_setup = False
debug = True # This will get overwritten with the real value early on

def setup_logger(options, numeric_args):
    global logging_setup
    if logging_setup: return logging.getLogger()
    logger = logging.getLogger()
    logger.handlers = [] # under certain cases, a spurious stream handler is set. We don't know why
    logger.setLevel(logging.INFO)
    stderr = logging.StreamHandler(sys.stderr)
    stderr.setFormatter(logging.Formatter('%(levelname)s: %(message)s'))
    if not options.quiet:
        logger.addHandler(stderr)
    else:
        logger.addHandler(NullLogHandler()) # prevent default
    if options.log_file:
        setup_file_logger(options.log_file, options.debug)
    if options.debug:
        logger.setLevel(logging.DEBUG)
    else:
        stderr.setLevel(logging.WARNING)
        if options.verbose:
            stderr.setLevel(logging.INFO)
    logging_setup = True
    return logger

def setup_file_logger(log_file, debug):
    logger = logging.getLogger()
    file = logging.FileHandler(log_file)
    logformatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s", "%Y-%m-%d %H:%M")
    file.setFormatter(logformatter)
    logger.addHandler(file)
    if not debug:
        file.setLevel(logging.INFO)
    return file

def make_base_args(options, **grab):
    """Takes parsed options, and breaks them back into a command
    line string that we can pass into a subcommand"""
    args = []
    grab["debug"]   = "--debug"
    grab["verbose"] = "--verbose"
    grab["quiet"]   = "--quiet"
    #grab["log_db"] = "--log-db"
    for k,flag in grab.items():
        value = getattr(options, k)
        if not value: continue
        args.append(flag)
        if type(value) is not bool:
            args.append(str(value))
    return args

def security_check_homedir(location):
    """
    Performs a check against a directory to determine if current
    directory's owner has a home directory that is a parent directory.
    This protects against malicious mountpoints, and is roughly equivalent
    to the suexec checks.
    """
    # XXX: this is a smidge unfriendly to systems who haven't setup
    # nswitch.
    try:
        uid = util.get_dir_uid(location)
        real = os.path.realpath(location)
        if not real.startswith(pwd.getpwuid(uid).pw_dir + "/"):
            logging.error("Security check failed, owner of deployment and "
                    "owner of home directory mismatch for %s" % location)
            return False
    except KeyError:
        logging.error("Security check failed, could not look up "
                "owner of %s (uid %d)" % (location, uid))
        return False
    except OSError as e:
        logging.error("OSError: %s" % str(e))
        return False
    return True

def calculate_log_name(log_dir, i):
    """
    Calculates a log entry given a numeric identifier, and
    directory under operation.
    """
    return os.path.join(log_dir, "%04d.log" % i)

def create_logdir(log_dir):
    """
    Creates a log directory and chmods it 777 to enable de-priviledged
    processes to create files.
    """
    try:
        os.mkdir(log_dir)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
        #if create_subdirs:
        #    log_dir = os.path.join(log_dir, str(int(time.time())))
        #    os.mkdir(log_dir) # if fails, be fatal
        #    # XXX: update last symlink
    os.chmod(log_dir, 0o777)

class NullLogHandler(logging.Handler):
    """Log handler that doesn't do anything"""
    def emit(self, record):
        pass

class WizardOptionParser(optparse.OptionParser):
    """Configures some default user-level options"""
    store_help = False
    def __init__(self, *args, **kwargs):
        kwargs["add_help_option"] = False
        if "store_help" in kwargs:
            self.store_help = kwargs["store_help"]
            del kwargs["store_help"]
        optparse.OptionParser.__init__(self, *args, **kwargs)
    def parse_all(self, *args, **kwargs):
        if self.store_help:
            self.add_option("-h", "--help", action="store_true", default=False, dest="help", help=optparse.SUPPRESS_HELP)
        else:
            self.add_option("-h", "--help", action="help", help=optparse.SUPPRESS_HELP)
        group = optparse.OptionGroup(self, "Common Options")
        group.add_option("-v", "--verbose", dest="verbose", action="store_true",
                default=util.boolish(os.getenv("WIZARD_VERBOSE")), help="Turns on verbose output.  Envvar is WIZARD_VERBOSE")
        group.add_option("--debug", dest="debug", action="store_true",
                default=util.boolish(os.getenv("WIZARD_DEBUG")), help="Turns on debugging output.  Envvar is WIZARD_DEBUG")
        group.add_option("-q", "--quiet", dest="quiet", action="store_true",
                default=util.boolish(os.getenv("WIZARD_QUIET")), help="Turns off output to stdout. Envvar is WIZARD_QUIET")
        group.add_option("--log-file", dest="log_file", metavar="FILE",
                default=os.getenv("WIZARD_LOGFILE"), help="Logs verbose output to file")
        group.add_option("--directory", dest="directory", metavar="PATH",
                default=os.getenv("WIZARD_DIRECTORY", ".wizard"), help="Initialize this folder to store metadata.")
        self.add_option_group(group)
        options, numeric_args = self.parse_args(*args, **kwargs)
        setup_logger(options, numeric_args)
        debug = options.debug
        # we're going to process the global --log-dir/--seen dependency here
        if hasattr(options, "seen") and hasattr(options, "log_dir"):
            if not options.seen and options.log_dir:
                options.seen = os.path.join(options.log_dir, "seen.txt")
        return options, numeric_args

class OptionBaton(object):
    """Command classes may define options that they sub-commands may
    use.  Since wizard --global-command subcommand is not a supported
    mode of operation, these options have to be passed down the command
    chain until a option parser is ready to take it; this baton is
    what is passed down."""
    def __init__(self):
        self.store = {}
    def add(self, *args, **kwargs):
        key = kwargs["dest"] # require this to be set
        self.store[key] = optparse.make_option(*args, **kwargs)
    def push(self, option_parser, *args):
        """Hands off parameters to option parser"""
        for key in args:
            option_parser.add_option(self.store[key])

class Error(wizard.Error):
    """Base error class for all command errors"""
    pass
