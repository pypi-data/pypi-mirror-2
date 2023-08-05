import distutils.version
import datetime
import dateutil.tz

from wizard import app, deploy

def test_deployment_parse():
    result = deploy.Deployment.parse("/afs/athena.mit.edu/user/e/z/ezyang/web_scripts/test-wiki:/afs/athena.mit.edu/contrib/scripts/deploy/mediawiki-1.11.0\n")
    assert result.location == "/afs/athena.mit.edu/user/e/z/ezyang/web_scripts/test-wiki"
    assert result.version == distutils.version.LooseVersion("1.11.0")
    assert result.application.name == "mediawiki"

def test_deployment_parse_nosuchapplication():
    try:
        deploy.Deployment.parse("a:/foo/obviouslybogus-1.11.0\n")
        assert False
    except app.NoSuchApplication:
        pass

def test_deployment_from_dir():
    pass # XXX

