import os.path
import sys
import dateutil.parser

import wizard
from wizard import app
import wizard.deploy # to break circular loop

# This code operates off of the assumption of .scripts-version, which
# is not true.

class DeployLog(list):
    # As per #python; if you decide to start overloading magic methods,
    # we should remove this subclass
    """Equivalent to .scripts-version: a series of DeployRevisions."""
    def __init__(self, revs = []):
        """`revs`  List of DeployRevision objects"""
        list.__init__(self, revs) # pass to list
    def __repr__(self):
        return '<DeployLog %s>' % list.__repr__(self)
    @staticmethod
    def load(deployment):
        """Loads a scripts version file and parses it into
        DeployLog and DeployRevision objects"""
        # XXX: DIRTY DIRTY HACK
        # What we should actually do is parse the git logs
        file = deployment.old_version_file
        i = 0
        rev = DeployRevision()
        revs = []
        def append(rev):
            if i:
                if i != 4:
                    raise ScriptsVersionNotEnoughFieldsError(file)
                revs.append(rev)
        try:
            fh = open(file)
        except IOError:
            raise ScriptsVersionNoSuchFile(file)
        for line in fh:
            line = line.rstrip()
            if not line:
                append(rev)
                i = 0
                rev = DeployRevision()
                continue
            if i == 0:
                # we need the dateutil parser in order to
                # be able to parse time offsets
                rev.datetime = dateutil.parser.parse(line)
            elif i == 1:
                rev.user = line
            elif i == 2:
                rev.source = DeploySource.parse(line)
            elif i == 3:
                try:
                    rev.version = app.ApplicationVersion.parse(line)
                except (wizard.deploy.Error, app.Error) as e:
                    e.location = deployment.location
                    raise e, None, sys.exc_info()[2]
            else:
                # ruh oh
                raise ScriptsVersionTooManyFieldsError(file)
            i += 1
        append(rev)
        return DeployLog(revs)

class DeployRevision(object):
    """A single entry in the .scripts-version file. Contains who deployed
    this revision, what application version this is, etc."""
    def __init__(self, datetime=None, user=None, source=None, version=None):
        """ `datetime`  Time this revision was deployed
            `user`      Person who deployed this revision, in ``user@host`` format.
            `source`    Instance of :class:`DeploySource`
            `version`   Instance of :class:`app.ApplicationVersion`
        Note: This object is typically built incrementally."""
        self.datetime = datetime
        self.user = user
        self.source = source
        self.version = version

class DeploySource(object):
    """Source of the deployment; see subclasses for examples"""
    def __init__(self):
        raise NotImplementedError # abstract class
    @staticmethod
    def parse(line):
        # munge out common prefix
        rel = os.path.relpath(line, "/afs/athena.mit.edu/contrib/scripts/")
        parts = rel.split("/")
        if parts[0] == "wizard":
            return WizardUpdate()
        elif parts[0] == "deploy" or parts[0] == "deploydev":
            isDev = ( parts[0] == "deploydev" )
            try:
                if parts[1] == "updates":
                    return OldUpdate(isDev)
                else:
                    return TarballInstall(line, isDev)
            except IndexError:
                pass
        return UnknownDeploySource(line)

class TarballInstall(DeploySource):
    """Original installation from tarball, characterized by
    /afs/athena.mit.edu/contrib/scripts/deploy/APP-x.y.z.tar.gz
    """
    def __init__(self, location, isDev):
        self.location = location
        self.isDev = isDev

class OldUpdate(DeploySource):
    """Upgrade using old upgrade infrastructure, characterized by
    /afs/athena.mit.edu/contrib/scripts/deploydev/updates/update-scripts-version.pl
    """
    def __init__(self, isDev):
        self.isDev = isDev

class WizardUpdate(DeploySource):
    """Upgrade using wizard infrastructure, characterized by
    /afs/athena.mit.edu/contrib/scripts/wizard/bin/wizard HASHGOBBLEDYGOOK
    """
    def __init__(self):
        pass

class UnknownDeploySource(DeploySource):
    """Deployment that we don't know the meaning of. Wot!"""
    def __init__(self, line):
        self.line = line

## -- Exceptions --

class Error(wizard.Error):
    """Base error class for log errors."""
    pass

class ScriptsVersionError(Error):
    """Errors specific to the parsing of a full .scripts-version file
    (errors that could also be triggered while parsing a parallel-find
    output should not be this subclass.)"""
    pass

class ScriptsVersionTooManyFieldsError(ScriptsVersionError):
    def __str__(self):
        return """

ERROR: Could not parse .scripts-version file.  It
contained too many fields.
"""

class ScriptsVersionNotEnoughFieldsError(ScriptsVersionError):
    def __str__(self):
        return """

ERROR: Could not parse .scripts-version file. It
didn't contain enough fields.
"""

class ScriptsVersionNoSuchFile(ScriptsVersionError):
    def __init__(self, file):
        self.file = file
    def __str__(self):
        return """

ERROR: File %s didn't exist.
""" % self.file

