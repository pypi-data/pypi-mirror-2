import os.path
from dateutil.tz import tzoffset
from datetime import datetime

from wizard import app, deploy, old_log, tests

def test_deploy_log_load():
    # this also is test_deploy_source_parse() and test_application_version_parse()
    dlog = old_log.DeployLog.load(deploy.Deployment(tests.getTestFile("old_log_test")))

    assert dlog[0].datetime == datetime(2006, 3, 23, 10, 7, 40, tzinfo=tzoffset(None, -5 * 60 * 60))
    assert dlog[0].user == "unknown"
    assert isinstance(dlog[0].source, old_log.TarballInstall)
    assert dlog[0].source.location == "/afs/athena.mit.edu/contrib/scripts/deploy/mediawiki.tar.gz"
    assert dlog[0].source.isDev == False
    assert dlog[0].version == app.applications()["mediawiki"].makeVersion('1.5.6')

    assert dlog[1].datetime == datetime(2007, 10, 17, 3, 38, 2, tzinfo=tzoffset(None, -4 * 60 * 60))
    assert dlog[1].user == "quentin@QUICHE-LORRAINE.MIT.EDU"
    assert isinstance(dlog[1].source, old_log.OldUpdate)
    assert dlog[1].source.isDev == True
    assert dlog[1].version == app.applications()["mediawiki"].makeVersion('1.5.6')

