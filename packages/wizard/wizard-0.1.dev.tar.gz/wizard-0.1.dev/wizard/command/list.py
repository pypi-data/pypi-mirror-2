import logging
import os.path

from wizard import command, deploy

def main(argv, baton):
    options, show = parse_args(argv, baton)
    errors = 0
    for d in deploy.parse_install_lines(show, options.versions_path, True, user=options.user):
        if isinstance(d, Exception):
            errors += 1
            continue
        if options.exists and not os.path.exists(os.path.join(d.location, options.exists)):
            continue
        if options.url:
            print d.url.geturl()
        else:
            print d.location
    if errors:
        logging.warning("%d errors, see 'wizard errors --verbose' for details" % errors)

def parse_args(argv, baton):
    usage = """usage: %prog list [ARGS] [APP[-VERSION]]

Lists the locations of all autoinstalls, optionally
filtered on parameters such as application name and version.

Examples:
    %prog list
        List all autoinstalls
    %prog list --exists php.ini
        List all autoinstalls with php.ini
    %prog list mediawiki
        List only MediaWiki autoinstalls
    %prog list mediawiki-1.11.0
        List only Mediawiki 1.11.0 autoinstalls"""
    parser = command.WizardOptionParser(usage)
    parser.add_option("-e", "--exists", dest="exists",
            help="only print deployment if FILE exists", metavar="FILE")
    parser.add_option("--url", dest="url", action="store_true",
            default=False, help="prints URLs of deployment instead of path")
    baton.push(parser, "versions_path")
    baton.push(parser, "user")
    options, args = parser.parse_all(argv)
    if len(args) > 1:
        parser.error("too many arguments")
    return options, args

