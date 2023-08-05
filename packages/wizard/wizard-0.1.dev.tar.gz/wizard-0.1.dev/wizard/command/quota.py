import logging
import os.path
import sys

from wizard import command, user

def main(argv, baton):
    options, args = parse_args(argv, baton)
    dir = os.path.abspath(args[0]) if args else os.getcwd()
    r = user.quota(dir)
    if r is None:
        sys.exit(1)
    print "%d %d" % r

def parse_args(argv, baton):
    usage = """usage: %prog quota [DIR]

Lists the used quota in bytes for a directory.  If
a directory is not specified, uses the current working
directory.

Output format is:

    USED AVAIL

in bytes.  Returns an exit code of 1 if quota could
not be determined."""
    parser = command.WizardOptionParser(usage)
    options, args = parser.parse_all(argv)
    if len(args) > 1:
        parser.error("too many arguments")
    return options, args

