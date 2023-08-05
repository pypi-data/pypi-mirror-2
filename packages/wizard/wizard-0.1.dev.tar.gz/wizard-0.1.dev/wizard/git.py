"""
Helper functions for dealing with Git.
"""

from wizard import shell, util

def describe():
    """Finds the output of git describe --tags of the current directory."""
    return shell.safeCall("git", "describe", "--tags", strip=True)

def commit_configure():
    """
    Performs a commit of changes performed during configuration of an install
    with an appropriate logfile message.
    """
    message = "Autoinstall configuration.\n\n%s" % util.get_git_footer()
    util.set_git_env()
    try:
        message += "\nConfigured-by: " + util.get_operator_git()
    except util.NoOperatorInfo:
        pass
    shell.call("git", "commit", "--allow-empty", "-a", "-m", message)
