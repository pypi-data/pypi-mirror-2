import math
import distutils.version

from wizard import app, command, deploy, shell, util

def main(argv, baton):
    options, args = parse_args(argv, baton)
    appname = args[0]
    # grab all the supported versions
    application = app.getApplication(appname)
    tags = set(shell.eval("git", "--git-dir=" + application.repository(options.srv_path), "tag").strip().split())
    unsupported = set()
    for d in deploy.parse_install_lines(appname, options.versions_path):
        try:
            version = d.detectVersion()
        except IOError:
            continue
        if "wordpress-%s" % version not in tags:
            print version
            unsupported.add(str(version))
    print "SUMMARY:"
    for v in sorted(distutils.version.LooseVersion(x) for x in list(unsupported)):
        print v

def parse_args(argv, baton):
    usage = """usage: %prog summary unsupported [ARGS] APP

Determines what application versions are unsupported in our
repository but are extant in migrated/unmigrated installs.
We have to calculate the real version using our heuristic,
since Git may lie if the user manually upgraded their install."""
    parser = command.WizardOptionParser(usage)
    baton.push(parser, "versions_path")
    baton.push(parser, "srv_path")
    options, args = parser.parse_all(argv)
    if len(args) > 1:
        parser.error("too many arguments")
    if len(args) < 1:
        parser.error("must specify application")
    return options, args

