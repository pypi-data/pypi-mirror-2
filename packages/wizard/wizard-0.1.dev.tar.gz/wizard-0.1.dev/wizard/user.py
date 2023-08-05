"""
Module for querying information about users.  This mostly asks plugins
for the extra information, and falls back to using a default that should
work on most systems (but by no means all systems.)
"""

import pkg_resources
import os
import socket
import logging
import pwd

from wizard import plugin

def quota(dir=None):
    """
    Returns a tuple (quota usage, quota limit).  Returns ``None`` if
    the quota usage is unknown.  If ``dir`` is omitted, the current
    working directory is assumed.  Value returned is in bytes.

    This function implements a plugin interface named
    :ref:`wizard.user.quota`.
    """
    if dir is None:
        dir = os.getcwd()
    return plugin.hook("wizard.user.quota", [dir])

def email(name=None):
    """
    Converts a username into an email address to that user.  If you have
    a UID, you will have to convert it into a username first.  If no
    canonical source of information is found, an heuristic approach
    will be used.  If ``name`` is ``None``, the current user will be
    used unless it is root, in which case :func:`operator` is tried
    first to determine the real current user.

    This function implements a plugin interface named
    :ref:`wizard.user.email`.
    """
    if name is None:
        logging.info("wizard.user.email: Determining email for current user")
        env_email = os.getenv("EMAIL")
        if env_email is not None:
            logging.info("wizard.user.email: Used environment email %s", env_email)
            return env_email
        name = operator()
    # run plugins
    r = plugin.hook("wizard.user.email", [name])
    if r is not None:
        return r
    # guess an email
    try:
        mailname = open("/etc/mailname").read()
    except:
        mailname = socket.getfqdn()
    return name + "@" + mailname

def operator():
    """
    Determines the username of the true person who is running this
    program.  If the process's real uid is nonzero, just do a passwd
    lookup; otherwise attempt to figure out the user behind the root
    prompt some other way.

    This function implements a plugin interface named
    :ref:`wizard.user.operator`.
    """
    uid = os.getuid()
    if uid:
        pwdentry = pwd.getpwuid(uid)
        return pwdentry.pw_name
    # run plugins
    r = plugin.hook("wizard.user.operator", [])
    if r is not None:
        return r
    # use SUDO_USER
    sudo_user = os.getenv("SUDO_USER")
    if not sudo_user:
        return None
    pwdentry = pwd.getpwnam(sudo_user)
    return pwdentry.pw_name

def passwd(path=None, uid=None):
    """
    Returns a passwd-like entry (a :class:`Info` object) corresponding
    to the owner of ``path``.  If ``uid`` is specified, ``path`` is used
    solely to determine the filesystem ``uid`` was determined from.  It
    will fall back to the local passwd database, and return ``None``
    if no information is available.  If ``path`` is omitted, it will
    fall back to the current working directory.

    This function implements a plugin interface named
    :ref:`wizard.user.passwd`.
    """
    if path is None:
        path = os.getcwd()
    path = os.path.realpath(path)
    if not uid:
        uid = os.stat(path).st_uid
    r = plugin.hook("wizard.user.passwd", [path, uid])
    if r is not None:
        return r
    try:
        return Info.pwentry(pwd.getpwuid(uid))
    except KeyError:
        return None

def pwnam(name):
    """
    This user converts a username into a :class:`Info` object using
    *only* the local password database.
    """
    return Info.pwentry(pwd.getpwnam(name))

class Info(object):
    """
    Object containing information describing a user.  It is analogous to
    passwd, but has dropped the password field and dedicated the
    ``gecos`` field for real name information.

    .. note::

        If a platform does not support retrieving information about a
        field, it may have the value ``None``.
    """
    #: Login name
    name = None
    #: User ID
    uid = None
    #: Group ID
    gid = None
    #: Real name
    realname = None
    #: Home directory
    homedir = None
    #: Default command interpreter
    shell = None
    @staticmethod
    def pwentry(pwentry):
        return Info(pwentry.pw_name, pwentry.pw_uid, pwentry.pw_gid,
                pwentry.pw_gecos.split(",")[0], pwentry.pw_dir, pwentry.pw_shell)
    def __init__(self, name, uid, gid, realname, homedir, shell):
        self.name = name
        self.uid = uid
        self.gid = gid
        self.realname = realname
        self.homedir = homedir
        self.shell = shell
        self._email = None
    @property
    def email(self):
        """The email of this user, calculated on the fly."""
        if self._email is None:
            self._email = email(self.name)
        return self._email
