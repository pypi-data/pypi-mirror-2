import optparse

def attr_to_option(variable):
    """
    Converts Python attribute names to command line options.

    >>> attr_to_option("foo_bar")
    '--foo-bar'
    """
    return '--' + variable.replace('_', '-')

class Controller(object):
    """
    Simple controller that actually delegates to :class:`optparse.OptionParser`.
    """
    def __init__(self, dir, schema):
        self.dir = dir
        self.schema = schema
    def push(self, parser):
        """Pushes arg schema to :class:`optparse.OptionParser`."""
        required = optparse.OptionGroup(parser, "Required Arguments (SETUPARGS)")
        optional = optparse.OptionGroup(parser, "Optional Arguments (SETUPARGS)")
        for arg in self.schema.args.values():
            group = arg.name in self.schema.provides and optional or required
            group.add_option(attr_to_option(arg.name), dest=arg.name, metavar=arg.type,
                    default=None, help=arg.help)
        parser.add_option_group(required)
        parser.add_option_group(optional)
    def handle(self, options):
        """
        Performs post-processing for the options, including throwing
        errors if not all arguments are specified.
        """
        self.schema.load(options)
