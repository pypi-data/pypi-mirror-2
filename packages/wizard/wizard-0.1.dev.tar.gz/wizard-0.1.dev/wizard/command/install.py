import os
import sys
import distutils
import logging

import wizard
from wizard import app, command, git, prompt, shell, util
from wizard.install import installopt, interactive

def main(argv, baton):
    old_options, args = parse_args(argv, baton)

    appstr = args[0]
    dir = os.path.abspath(args[1])
    web_stub_path = old_options.web_stub_path

    if not old_options.retry and not old_options.help and os.path.exists(dir) and os.listdir(dir):
        raise DirectoryExistsError(dir)

    appname, _, version = appstr.partition('-')
    application = app.getApplication(appname)

    if application.needs_web_stub and web_stub_path is None:
        raise NeedsWebStubError

    # get configuration
    schema = application.install_schema
    schema.commit(application, dir, web_stub_path)
    options = None
    opthandler = installopt.Controller(dir, schema)
    parser = command.WizardOptionParser("""usage: %%prog install %s DIR [ -- SETUPARGS ]

Autoinstalls the application %s in the directory DIR.""" % (appname, appname))
    configure_parser(parser, baton)
    opthandler.push(parser)
    if old_options.help:
        parser.print_help()
        sys.exit(1)
    input = prompt.make(old_options.prompt, old_options.non_interactive)
    ihandler = interactive.Controller(dir, schema, input)
    options, _ = parser.parse_all(args[2:] + command.make_base_args(old_options))
    if old_options.non_interactive:
        opthandler.handle(options)
    else:
        ihandler.ask(options)

    if not os.path.exists(dir) or not os.listdir(dir):
        input.infobox("Copying files (this may take a while)...")
        shell.call("git", "clone", "-q", "--shared", application.repository(old_options.srv_path), dir)
    else:
        logging.info("Skipped clone")
    wizard_dir = ".wizard"
    with util.ChangeDirectory(dir):
        util.init_wizard_dir()
        if not old_options.retry and version:
            shell.call("git", "reset", "-q", "--hard", appstr)
        input.infobox("Installing...")
        if not version: # figure out what version we're installing
            v = application.detectVersionFromGit(appname + "-*", appname + "-")
            logging.info("Installing latest version: %s", version)
        else:
            v = distutils.version.LooseVersion(version)
        if application.needs_web_stub:
            application.install(v, options, web_stub_path)
        else:
            application.install(v, options)
        if not old_options.no_commit:
            git.commit_configure()
    # This should be on a per-application basis
    #if not hasattr(options, "web_inferred"):
    #    open(os.path.join(dir, os.path.join(wizard_dir, "url")), "w") \
    #        .write("http://%s%s" % (options.web_host, options.web_path)) # XXX: no support for https yet!

    input.infobox("Congratulations, your new install is now accessible at:\n\nhttp://%s%s" \
            % (options.web_host, options.web_path), width=80)

def configure_parser(parser, baton):
    parser.add_option("--prompt", dest="prompt", action="store_true",
            default=False, help="Force to use non-ncurses interactive interface")
    parser.add_option("--non-interactive", dest="non_interactive", action="store_true",
            default=False, help="Force program to be non-interactive and use SETUPARGS.  Use --help with APP to find argument names.")
    parser.add_option("--no-commit", dest="no_commit", action="store_true",
            default=util.boolish(os.getenv("WIZARD_NO_COMMIT")), help="Do not generate an 'installation commit' after configuring the application. Envvar is WIZARD_NO_COMMIT")
    parser.add_option("--retry", dest="retry", action="store_true",
            default=False, help="Do not complain if directory already exists and reinstall application.")
    baton.push(parser, "srv_path")

def parse_args(argv, baton):
    usage = """usage: %prog install APP DIR [ -- SETUPARGS ]

Autoinstalls the application APP in the directory DIR.
This command will interactively ask for information to
complete the autoinstall.

You can also use --help with APP and DIR to find out what
are required SETUPARGS if you want to run this non-interactively
(the distribution of required and optional arguments may change
depending on what directory you are installing to.)"""
    parser = command.WizardOptionParser(usage, store_help=True)
    configure_parser(parser, baton)
    parser.add_option("--web-stub-path", dest="web_stub_path",
            default=None, help="Used on certain installations for indicating"
            "where to place stub files for a web path.")
    options, args = parser.parse_all(argv)
    if options.help:
        if len(args) == 0:
            parser.print_help()
            sys.exit(1)
        elif len(args) == 1:
            args.append(os.getcwd())
    else:
        if len(args) < 2:
            parser.error("not enough arguments")
    return options, args

class DirectoryExistsError(wizard.Error):
    def __init__(self, dir=None, ):
        self.dir = dir
    def __str__(self):
        return "Directory (%s) already exists and is not empty" % self.dir

class NeedsWebStubError(wizard.Error):
    def __str__(self):
        return "You need to specify a web stub directory for this application"
