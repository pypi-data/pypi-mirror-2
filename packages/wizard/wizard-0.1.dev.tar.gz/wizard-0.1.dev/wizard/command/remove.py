import shutil

from wizard import command, deploy, shell

def main(argv, baton):
    options, args = parse_args(argv, baton)
    dir = args[0]
    shell.drop_priviledges(dir, options.log_file)
    deployment = deploy.ProductionCopy(dir)
    deployment.verify()
    deployment.remove(options)
    shutil.rmtree(dir)

def parse_args(argv, baton):
    usage = """usage: %prog remove DIR

Removes an autoinstall directory, deleting any databases along
with it.  Will refuse to remove a non-autoinstall directory.  Be
careful: this will also destroy all backups!"""
    parser = command.WizardOptionParser(usage)
    options, args = parser.parse_all(argv)
    if len(args) > 1:
        parser.error("too many arguments")
    if len(args) == 0:
        parser.error("must specify directory")
    return options, args

