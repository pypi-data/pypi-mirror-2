import math
import distutils.version

from wizard import app, command, deploy, util

def main(argv, baton):
    options, str_show = parse_args(argv, baton)
    HISTOGRAM_WIDTH = 30
    if str_show:
        apps = app.applications()
        show = set(apps[x] for x in str_show)
        accumulate = False
    else:
        str_show = []
        show = set()
        accumulate = True
    c_application = {}
    for d in deploy.parse_install_lines(str_show, options.versions_path):
        c_application.setdefault(d.application, util.Counter())
        version = util.truncate(d.app_version.version)
        c_application[d.application].count(version)
        if accumulate:
            show.add(d.application)
    if not show:
        print "No applications found"
    for application in show:
        counter = c_application[application]
        total = counter.sum()
        print "%-20s %3d installs" % (application.name, total)
        vmax = counter.max()
        for version in sorted(counter.keys(), key=distutils.version.LooseVersion):
            v = counter[version]
            graph = '+' * int(math.ceil(float(v)/vmax * HISTOGRAM_WIDTH))
            print "    %-16s %3d  %s" % (version, v, graph)
        print

def parse_args(argv, baton):
    usage = """usage: %prog summary version [ARGS] [APP]

Prints graphs of version usage in autoinstallers

Examples:
    %prog summary
        Show graphs for all autoinstall versions
    %prog summary version mediawiki
        Show graph for MediaWiki autoinstall versions"""
    parser = command.WizardOptionParser(usage)
    baton.push(parser, "versions_path")
    options, args = parser.parse_all(argv)
    if len(args) > 1:
        parser.error("too many arguments")
    return options, args

