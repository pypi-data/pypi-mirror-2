import os.path

from wizard import command, deploy, shell, util

def main(argv, baton):
    options, args = parse_args(argv, baton)
    dir = os.path.abspath(args[0]) if args else os.getcwd()
    shell.drop_priviledges(dir, options.log_file)
    util.chdir(dir)
    d = deploy.ProductionCopy(".")
    d.verify()
    d.verifyConfigured()
    print d.backup(options)

def parse_args(argv, baton):
    usage = """usage: %prog backup [ARGS] [DIR]

Takes a configured autoinstall and performs a backup of
its data.  This data is stored by default in
.wizard/backups/x.y.z-yyyy-mm-dd"""
    parser = command.WizardOptionParser(usage)
    options, args = parser.parse_all(argv)
    if len(args) > 1:
        parser.error("too many arguments")
    return options, args

