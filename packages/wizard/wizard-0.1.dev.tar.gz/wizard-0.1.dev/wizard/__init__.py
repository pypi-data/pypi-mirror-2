class Error(Exception):
    """Base exception for all Wizard exceptions"""
    #: Code to exit the application with.
    exitcode = 1
    #: Whether or not to suppress the backtrace (unless in debug mode)
    quiet = False

