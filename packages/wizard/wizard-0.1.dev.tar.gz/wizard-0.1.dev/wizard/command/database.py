import os.path

from wizard import deploy, command, shell

def main(argv, baton):
    options, args = parse_args(argv, baton)
    dir = os.path.abspath(args[0]) if args else os.getcwd()
    shell.drop_priviledges(dir, options.log_file)
    deployment = deploy.ProductionCopy(dir)
    deployment.verify()
    deployment.verifyConfigured()
    print deployment.dsn.database

def parse_args(argv, baton):
    usage = """usage: %prog database [DIR]

Prints the name of the database an application is using.
Maybe in the future this will print more information."""
    parser = command.WizardOptionParser(usage)
    options, args = parser.parse_all(argv)
    if len(args) > 1:
        parser.error("too many arguments")
    if len(args) == 0:
        parser.error("must specify directory")
    return options, args
