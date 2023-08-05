from wizard import app, deploy, command

def main(argv, baton):
    options, show = parse_args(argv, baton)
    for e in deploy.parse_install_lines(show, options.versions_path, True, user=options.user):
        if not isinstance(e, deploy.Error) and not isinstance(e, app.Error):
            if isinstance(e, Exception):
                raise e
            continue
        if options.verbose:
            if isinstance(e, app.NoSuchApplication):
                print "Application %s does not exist, at %s" % (e.app, e.location)
            elif isinstance(e, app.DeploymentParseError):
                print "Parse error for line '%s', at %s" % (e.value, e.location)
            else:
                raise e
        else:
            print e.location

def parse_args(argv, baton):
    usage = """usage: %prog errors [ARGS]

Lists all errors that occurred while parsing the versions
directory."""
    parser = command.WizardOptionParser(usage)
    baton.push(parser, "versions_path")
    baton.push(parser, "user")
    options, args = parser.parse_all(argv)
    if len(args) > 1:
        parser.error("too many arguments")
    return options, args

