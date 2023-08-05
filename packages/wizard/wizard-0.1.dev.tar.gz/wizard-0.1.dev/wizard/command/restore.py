import logging
import os
import sys

from wizard import command, deploy, shell

def main(argv, baton):
    options, args = parse_args(argv, baton)
    d = deploy.ProductionCopy(".")
    d.verify()
    backups = d.backup_dir
    if not args:
        if not os.path.exists(backups):
            print "No restore points available"
            return
        sys.stderr.write("Available backups:\n")
        count = 0
        for d in reversed(sorted(os.listdir(backups))):
            if ".bak" in d:
                continue
            if d.startswith("."):
                continue
            if os.listdir(os.path.join(backups, d)):
                print d
            else:
                count += 1
        if count:
            logging.warning("Pruned %d empty backups" % count)
        return
    backup = args[0]
    if backup == "top":
        try:
            backup = sorted(os.listdir(backups))[-1]
            logging.warning("Using backup %s" % backup)
        except IndexError:
            raise Exception("No restore points available")
    bits = backup.split('-')
    date = '-'.join(bits[-3:])
    version = '-'.join(bits[0:-3])
    shell.drop_priviledges(".", options.log_file)
    d = deploy.ProductionCopy(".")
    d.verify()
    d.verifyConfigured()
    tag = "%s-%s" % (d.application.name, version)
    try:
        shell.call("git", "rev-parse", tag)
    except shell.CallError:
        raise Exception("Tag %s doesn't exist in repository" % tag)
    shell.call("git", "reset", "-q", "--hard", tag)
    d.restore(backup, options)

def parse_args(argv, baton):
    usage = """usage: %prog restore [ARGS] ID

Takes a backup from the backups/ directory and does
a full restore back to it.  CURRENT DATA IS DESTROYED,
so you may want to do a backup before you do a restore.

You can specify 'top' as the ID in order to restore from
the latest backup."""
    parser = command.WizardOptionParser(usage)
    options, args = parser.parse_all(argv)
    if len(args) > 1:
        parser.error("too many arguments")
    return options, args

