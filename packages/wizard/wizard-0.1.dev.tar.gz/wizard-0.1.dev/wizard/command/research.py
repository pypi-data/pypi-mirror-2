import logging
import traceback
import itertools
import random

from wizard import app, command, deploy, shell, util

def main(argv, baton):
    options, show = parse_args(argv, baton)
    appname = show[0]
    application = app.getApplication(appname)
    deploys = deploy.parse_install_lines(show, options.versions_path)
    stats = {}
    iffy = 0
    clean = 0
    total = 0
    deploys = itertools.islice(deploys, options.limit)
    if options.sample:
        deploys = random.sample(list(deploys), options.sample)
    try:
        for d in deploys:
            logging.info("Processing " + d.location)
            try:
                d.verify()
                d.verifyTag(options.srv_path)
                d.verifyGit(options.srv_path)
                d.verifyConfigured()
                with util.ChangeDirectory(d.location):
                    results = []
                    out = shell.safeCall('git', 'diff', '--numstat', d.app_version.wizard_tag, strip=True)
                    total += 1
                    for line in out.split("\n"):
                        added, deleted, filename = line.split(None, 3)
                        if filename.endswith("php.ini"): continue
                        if added == '-': continue
                        if deleted == '-': continue
                        added = int(added)
                        deleted = int(deleted)
                        if not added and not deleted or application.researchFilter(filename, added, deleted):
                            continue
                        results.append((added,deleted,filename))
                    if len(results) > options.filter:
                        print "-       -       " +  d.location
                        iffy += 1
                        continue
                    if not results:
                        clean += 1
                    for added,deleted,filename in results:
                        stats.setdefault(filename, 0)
                        stats[filename] += 1
                        if application.researchVerbose(filename) and not options.verbose:
                            continue
                        print "%-7d %-7d %s/%s" % (added,deleted,d.location,filename)
            except (deploy.NotConfiguredError, deploy.NotMigratedError):
                # XXX: These should error, but for now don't
                pass
            except (deploy.Error, shell.CallError):
                # XXX: Maybe should also do app.Error
                logging.error("%s in %s" % (traceback.format_exc(), d.location))
            except KeyboardInterrupt:
                raise
            except:
                logging.critical("%s in %s" % (traceback.format_exc(), d.location))
    except KeyboardInterrupt:
        print
        print "Caught signal..."
        pass
    print '-' * 50
    for filename in sorted(stats.keys()):
        count = stats[filename]
        if not count: continue
        print "%-7d %s" % (count, filename)
    print '-' * 50
    print "%d out of %d (%.1f%%) had large diffstats" % (iffy, total, float(iffy)/total*100)
    print "%d out of %d (%.1f%%) had clean diffstats" % (clean, total, float(clean)/total*100)

def parse_args(argv, baton):
    usage = """usage: %prog research APP

Tells you how spectacularly an upgrade here will explode."""
    parser = command.WizardOptionParser(usage)
    parser.add_option("--limit", dest="limit", type="int",
            default=None, help="Limit the number of autoinstalls to look at.")
    parser.add_option("--sample", dest="sample", type="int", metavar="N",
            default=None, help="Instead of researching all installs, research a random sample of N size.")
    parser.add_option("--filter", dest="filter", type="int", metavar="N",
            default=4, help="How many files are permitted in a diffstat before treating the install as having a 'large diffstat'")
    baton.push(parser, "srv_path")
    baton.push(parser, "versions_path")
    options, args = parser.parse_all(argv)
    if len(args) > 1:
        parser.error("too many arguments")
    if not args:
        parser.error("must specify application to research")
    return options, args

