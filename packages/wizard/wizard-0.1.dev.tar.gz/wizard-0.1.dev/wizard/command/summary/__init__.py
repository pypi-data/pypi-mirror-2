import optparse
import os
import logging

import wizard
from wizard import command, deploy

def main(argv, baton):
    usage = """usage: %prog summary [ARGS] APPS

Scans all of the collected data from parallel-find.pl, and
calculates interesting information about them.

Its subcommands are:
    unsupported     List unsupported versions in the wild
    version         Breakdown of autoinstalls by version (default)

Use %prog summary SUBCOMMAND --help for more information."""
    parser = command.WizardOptionParser(usage)
    parser.disable_interspersed_args()
    baton.push(parser, "versions_path")
    _, args = parser.parse_all(argv)
    rest_argv = args[1:]
    try:
        command_name = args[0]
    except IndexError:
        command_name = "version"
    def get_command(name):
        member = name.replace("-", "_")
        module = "wizard.command.summary." + member
        __import__(module)
        return getattr(wizard.command.summary, member)
    if command == "help":
        try:
            get_command(rest_argv[0]).main(['--help'], baton)
        except ImportError:
            parser.error("invalid action")
        except IndexError:
            parser.print_help()
            raise SystemExit(1)
    try:
        command_module = get_command(command_name)
    except ImportError:
        parser.error("invalid action")
    command_module.main(rest_argv, baton)

