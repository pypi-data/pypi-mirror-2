import os

from wizard import command, deploy, shell, util

def main(argv, baton):
    options, args = parse_args(argv, baton)
    reason = args[0]
    # Directory information not transferred via command line, so this
    # will not error due to the changed directory.
    shell.drop_priviledges(".", options.log_file)
    # XXX: this should be abstracted away!
    if os.path.exists(".git/WIZARD_REPO"):
        util.chdir(shell.eval('git', 'config', 'remote.origin.url'))
    production = deploy.ProductionCopy(".")
    production.verify()
    open(production.blacklisted_file, 'w').write(reason + "\n")

def parse_args(argv, baton):
    usage = """usage: %prog blacklist [ARGS] REASON

Adds the file .wizard/blacklisted so that future upgrades
are not attempted without manual intervention."""
    parser = command.WizardOptionParser(usage)
    options, args = parser.parse_all(argv)
    if len(args) > 2:
        parser.error("too many arguments")
    if len(args) < 1:
        parser.error("must specify reason")
    return options, args

