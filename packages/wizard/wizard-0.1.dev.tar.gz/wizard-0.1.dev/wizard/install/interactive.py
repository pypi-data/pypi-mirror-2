import getpass
import sys

def humanize(text):
    return text.replace("_", " ").capitalize()

class Controller(object):
    def __init__(self, dir, schema, input):
        self.dir = dir
        self.schema = schema
        self.input = input
    def ask(self, options):
        """
        Interactively ask the user for information.
        """
        self.schema.fill(options)
        for name, arg in self.schema.args.items():
            if name in self.schema.provides:
                continue
            if getattr(options, name) is not None:
                continue
            if not arg.password:
                val = self.input.inputbox(arg.prompt + "\n\n" + humanize(name) + ":")
            else:
                while 1:
                    val = self.input.passwordbox(arg.prompt + "\n\n" + humanize(name) + " (cursor will not move):")
                    val2 = self.input.passwordbox("Please enter the password again (cursor will not move):")
                    if val != val2:
                        self.input.msgbox("Passwords didn't match.")
                        continue
                    break
            setattr(options, name, val)
        self.schema.load(options)

