"""
Interface compatible with :class:`PromptInterface` for doing
non-ncurses interaction.

By convention, the last line of a text parameter should be
a short value with a trailing colon so that we can prompt a user
for a value immediately after it.

.. testsetup:: *

    from wizard.prompt import *
"""

import sys
import readline
import decorator
import textwrap
import getpass
import os

import wizard

try:
    import dialog
    has_dialog = True
except ImportError:
    has_dialog = False

def fill(text, width=60, **kwargs):
    """
    Convenience wrapper for :func:`textwrap.fill` that preserves
    paragraphs.
    """
    return "\n\n".join(textwrap.fill(p, width=width, **kwargs) for p in text.split("\n\n"))

def guess_dimensions(text, width=60):
    """
    Guesses the dimensions that any given piece of text will
    need to display on terminal, given some width.
    """
    # +1 for the fact that there's no trailing newline from fill
    # +2 for the borders
    # +1 as a buffer in case we underestimate
    print fill(text)
    return width, fill(text, width-2).count("\n") + 1 + 2 + 1

def make(prompt, non_interactive):
    """
    Makes a :class:`dialog.Dialog` compatible class based on
    configuration.
    """
    if non_interactive:
        return FailPrompt()
    if prompt or os.getenv('TERM') == 'dumb' or not has_dialog:
        return Prompt()
    try:
        return Dialog()
    except (dialog.ExecutableNotFound, UnsupportedTerminal):
        return Prompt()

def join_or(items):
    """
    Joins a list of disjunctions into a human readable sentence.

    >>> join_or(['foo'])
    'foo'
    >>> join_or(['foo', 'bar', 'baz'])
    'foo, bar or baz'
    """
    if len(items) == 0:
        raise ValueError
    elif len(items) == 1:
        return items[0]
    return ', '.join(items[:-1]) + ' or ' + items[-1]

class PromptInterface(object):
    def inputbox(self, text, init='', **kwargs):
        """
        Request a free-form, single line of text from the user.
        Prompt the user using ``text``; and ``init`` is the
        initial value filling the field; not all implementations
        support editing ``init``.  Returns the typed string.
        """
        raise NotImplementedError
    def menu(self, text, choices=[], **kwargs):
        """
        Request a selection from a number of choices from the user.
        Prompt the user using ``text``; ``choices`` is a list
        of tuples of form ``(value to return, description)``, where
        ``value to return`` is the value that this function will
        return.
        """
        raise NotImplementedError
    def passwordbox(self, text, **kwargs):
        """
        Securely requests a password from the user.  Prompts the user
        using ``text``; return value is the password.
        """
        raise NotImplementedError
    def msgbox(self, text, **kwargs):
        """
        Gives the user a message that they must dismiss before proceeding.
        """
        raise NotImplementedError
    def infobox(self, text, **kwargs):
        """
        Gives the user a non-blocking message; useful if you are about
        to do an operation that will take some time.
        """
        raise NotImplementedError

@decorator.decorator
def dialog_wrap(f, self, text, *args, **kwargs):
    """
    Convenience decorator that automatically:

        1. Removes already handled keyword arguments,
        2. Configures the dimensions of the dialog box, and
        3. Handles the different ext possibilities of dialog.
    """
    if 'cmdopt' in kwargs: del kwargs['cmdopt']
    if 'width' not in kwargs and 'height' not in kwargs:
        kwargs["width"], kwargs["height"] = guess_dimensions(text)
    elif 'width' in kwargs and 'height' not in kwargs:
        kwargs["width"], kwargs["height"] = guess_dimensions(text, width=kwargs["width"])
    result = f(self, text, *args, **kwargs)
    if not isinstance(result, tuple):
        exit = result
        value = None
    else:
        exit, value = result
    if exit == self.dialog.DIALOG_CANCEL or exit == self.dialog.DIALOG_ESC:
        raise UserCancel
    elif exit != self.dialog.DIALOG_OK:
        # XXX: We don't support stuff like DIALOG_EXTRA or DIALOG_HELP
        raise DialogError(exit)
    return value

class Dialog(PromptInterface):
    """Ncurses interface using dialog."""
    interactive = True
    def __init__(self):
        self.dialog = dialog.Dialog()
        exit = self.dialog.infobox("Setting up...")
        if exit != 0:
            raise UnsupportedTerminal
    @dialog_wrap
    def inputbox(self, *args, **kwargs):
        kwargs.setdefault('initerror', "You cannot edit initial value; please type characters after it.")
        initerror = kwargs['initerror']
        del kwargs['initerror']
        kwargs['height'] += 5 # for the text box
        exit, result = self.dialog.inputbox(*args, **kwargs)
        if exit == self.dialog.DIALOG_OK: # pylint: disable-msg=E1101
            # do some funny munging
            kwargs.setdefault('init', '')
            if result[0:len(kwargs['init'])] != kwargs['init']:
                self.msgbox(initerror, height=10, width=50)
                exit = self.dialog.DIALOG_OK # pylint: disable-msg=E1101
                result = self.inputbox(*args, initerror=initerror, **kwargs)
            else:
                result = result[len(kwargs['init']):]
        return (exit, result)
    @dialog_wrap
    def menu(self, *args, **kwargs):
        kwargs['height'] += 6 + len(kwargs['choices']) # for the border and menu entries
        return self.dialog.menu(*args, **kwargs)
    @dialog_wrap
    def msgbox(self, *args, **kwargs):
        kwargs['height'] += 3
        return self.dialog.msgbox(*args, **kwargs)
    @dialog_wrap
    def passwordbox(self, *args, **kwargs):
        kwargs['height'] += 6
        return self.dialog.passwordbox(*args, **kwargs)
    @dialog_wrap
    def infobox(self, text, **kwargs):
        return self.dialog.infobox(text, **kwargs)

@decorator.decorator
def prompt_wrap(f, self, *args, **kwargs):
    """Convenience decorator that handles end-of-document and interrupts."""
    try:
        return f(self, *args, **kwargs)
    except (EOFError, KeyboardInterrupt):
        raise UserCancel

class Prompt(PromptInterface):
    """Simple stdin/stdout prompt object."""
    interactive = True
    @prompt_wrap
    def inputbox(self, text, init='', **kwargs):
        print ""
        return raw_input(fill(text.strip()) + " " + init)
    @prompt_wrap
    def menu(self, text, choices=[], **kwargs):
        print ""
        print fill(text.strip())
        values = list(choice[0] for choice in choices)
        for choice in choices:
            print "% 4s  %s" % (choice[0], choice[1])
        while 1:
            out = raw_input("Please enter %s: " % join_or(values))
            if out not in values:
                print "'%s' is not a valid value" % out
                continue
            return out
    @prompt_wrap
    def passwordbox(self, text, **kwargs):
        print ""
        return getpass.getpass(text + " ")
    @prompt_wrap
    def msgbox(self, text, **kwargs):
        print ""
        print fill(text.strip())
        print "Press <Enter> to continue..."
    @prompt_wrap
    def infobox(self, text, **kwargs):
        print ""
        print fill(text.strip())

class FailPrompt(PromptInterface):
    """
    Prompt that doesn't actually ask the user; just fails with
    an error message.
    """
    interactive = False
    def inputbox(self, *args, **kwargs):
        kwargs.setdefault('cmdopt', '(unknown)')
        raise MissingRequiredParam(kwargs['cmdopt'])
    def passwordbox(self, *args, **kwargs):
        kwargs.setdefault('cmdopt', '(unknown)')
        raise MissingRequiredParam(kwargs['cmdopt'])
    def menu(self, *args, **kwargs):
        kwargs.setdefault('cmdopt', '(unknown)')
        raise MissingRequiredParam(kwargs['cmdopt'])
    def msgbox(self, text, **kwargs):
        print ""
        print fill(text.strip(), break_long_words=False)
    def infobox(self, text, **kwargs):
        print ""
        print fill(text.strip(), break_long_words=False)

class Error(wizard.Error):
    """Base error class."""
    pass

class MissingRequiredParam(Error):
    """Non-interactive, but we needed more info."""
    def __init__(self, cmdopt):
        """``cmdopt`` is the command line option that should be specified."""
        self.cmdopt = cmdopt
    def __str__(self):
        return """

ERROR: Missing required parameter, try specifying %s""" % self.cmdopt

class UserCancel(Error):
    """User canceled the input process."""
    def __str__(self):
        return "\nAborting installation process; no changes were made"

class DialogError(Error):
    """Dialog returned a mysterious error."""
    def __init__(self, exit):
        """``exit`` is the mysterious exit code."""
        self.exitcode = exit
    def __str__(self):
        return """

ERROR:  Dialog returned a mysterious exit code %d.""" % self.exitcode

class UnsupportedTerminal(Error):
    """It doesn't look like we support this terminal.  Internal error."""
    pass
