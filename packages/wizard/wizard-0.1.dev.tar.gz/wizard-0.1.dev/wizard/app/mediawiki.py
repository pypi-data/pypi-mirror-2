import re
import distutils.version
import os
import lxml.cssselect
import lxml.etree
import StringIO
import logging

from wizard import app, install, resolve, shell, util
from wizard.app import php

def make_filename_regex(var):
    """See :ref:`versioning config <seed>` for more information."""
    return 'LocalSettings.php', php.re_var(var)

seed = util.dictmap(make_filename_regex, {
        'WIZARD_IP': 'IP', # obsolete, remove after we're done
        'WIZARD_SITENAME': 'wgSitename',
        'WIZARD_SCRIPTPATH': 'wgScriptPath',
        'WIZARD_EMERGENCYCONTACT': ('wgEmergencyContact', 'wgPasswordSender'),
        'WIZARD_DBSERVER': 'wgDBserver',
        'WIZARD_DBNAME': 'wgDBname',
        'WIZARD_DBUSER': 'wgDBuser',
        'WIZARD_DBPASSWORD': 'wgDBpassword',
        'WIZARD_SECRETKEY': ('wgSecretKey', 'wgProxyKey'),
        })

class Application(app.Application):
    database = "mysql"
    parametrized_files = ['LocalSettings.php'] + php.parametrized_files
    deprecated_keys = set(['WIZARD_IP']) | php.deprecated_keys
    extractors = app.make_extractors(seed)
    extractors.update(php.extractors)
    substitutions = app.make_substitutions(seed)
    substitutions.update(php.substitutions)
    install_schema = install.ArgSchema("db", "admin", "email", "title")
    def download(self, version):
        series = ".".join(str(version).split(".")[:2])
        return "http://download.wikimedia.org/mediawiki/%s/mediawiki-%s.tar.gz" % (series, version)
    def checkConfig(self, deployment):
        return os.path.isfile("LocalSettings.php")
    def detectVersion(self, deployment):
        return self.detectVersionFromFile("includes/DefaultSettings.php", php.re_var("wgVersion"))
    def checkWeb(self, deployment):
        return self.checkWebPage(deployment, "/index.php?title=Main_Page", outputs=["<!-- Served"])
    def install(self, version, options):
        util.soft_unlink("LocalSettings.php")
        os.chmod("config", 0777) # XXX: vaguely sketchy

        postdata = {
            'Sitename': options.title,
            'EmergencyContact': options.email,
            'LanguageCode': 'en',
            'DBserver': options.dsn.host,
            'DBname': options.dsn.database,
            'DBuser': options.dsn.username,
            'DBpassword': options.dsn.password,
            'DBpassword2': options.dsn.password,
            'defaultEmail': options.email,
            'SysopName': options.admin_name,
            'SysopPass': options.admin_password,
            'SysopPass2': options.admin_password,
            }
        result = install.fetch(options, '/config/index.php', post=postdata)
        result_etree = lxml.etree.parse(StringIO.StringIO(result), lxml.etree.HTMLParser())
        selector = lxml.cssselect.CSSSelector(".error")
        error_messages = [e.text for e in selector(result_etree)]
        logging.debug("Installation output:\n\n" + result)
        if result.find("Installation successful") == -1:
            if not error_messages:
                raise app.InstallFailure()
            else:
                raise app.RecoverableInstallFailure(error_messages)
        os.rename('config/LocalSettings.php', 'LocalSettings.php')
        php.ini_replace_vars()

    def upgrade(self, d, version, options):
        if not os.path.isfile("AdminSettings.php"):
            shell.call("git", "checkout", "-q", "mediawiki-" + str(version), "--", "AdminSettings.php")
        try:
            result = shell.eval("php", "maintenance/update.php", "--quick", log=True)
        except shell.CallError as e:
            raise app.UpgradeFailure("Update script returned non-zero exit code\nSTDOUT: %s\nSTDERR: %s" % (e.stdout, e.stderr))
        results = result.rstrip().split()
        if not results or not results[-1] == "Done.":
            raise app.UpgradeFailure(result)
    def backup(self, deployment, backup_dir, options):
        app.backup_database(backup_dir, deployment)
    def restore(self, deployment, backup_dir, options):
        app.restore_database(backup_dir, deployment)
    def remove(self, deployment, options):
        app.remove_database(deployment)
    def researchFilter(self, filename, added, deleted):
        if filename == "LocalSettings.php":
            return added == deleted == 10 or added == deleted == 9
        elif filename == "AdminSettings.php":
            return added == 0 and deleted == 20
        elif filename == "config/index.php" or filename == "config/index.php5":
            return added == 0
        return False

Application.resolutions = {
'LocalSettings.php': [
    ("""
<<<<<<<
***1***
=======
## The URL base path to the directory containing the wiki;
## defaults for all runtime URL paths are based off of this.
## For more information on customizing the URLs please see:
## http://www.mediawiki.org/wiki/Manual:Short_URL
***2***
$wgScriptExtension  = ".php";

## UPO means: this is also a user preference option
>>>>>>>
""", [-1]),
    ("""
<<<<<<<
***1***
=======

# MySQL specific settings
$wgDBprefix         = "";
>>>>>>>
""", ["\n# MySQL specific settings", 1]),
    ("""
<<<<<<<
## is writable, then uncomment this:
***1***
=======
## is writable, then set this to true:
$wgEnableUploads       = false;
>>>>>>>
""", [-1]),
    ("""
<<<<<<<
***1***
$wgMathPath         = "{$wgUploadPath}/math";
$wgMathDirectory    = "{$wgUploadDirectory}/math";
$wgTmpDirectory     = "{$wgUploadDirectory}/tmp";
=======
$wgUseTeX           = false;
>>>>>>>
""", [1]),
    # order of these rules is important
    ("""
<<<<<<<
$configdate = gmdate( 'YmdHis', @filemtime( __FILE__ ) );
$wgCacheEpoch = max( $wgCacheEpoch, $configdate );
***1***
?>
=======
$wgCacheEpoch = max( $wgCacheEpoch, gmdate( 'YmdHis', @filemtime( __FILE__ ) ) );
>>>>>>>
""", [0, 1]),
    ("""
<<<<<<<
$configdate = gmdate( 'YmdHis', @filemtime( __FILE__ ) );
$wgCacheEpoch = max( $wgCacheEpoch, $configdate );
***1***
=======
$wgCacheEpoch = max( $wgCacheEpoch, gmdate( 'YmdHis', @filemtime( __FILE__ ) ) );
>>>>>>>
""", [0, 1]),
    ("""
<<<<<<<
?>
=======
# When you make changes to this configuration file, this will make
# sure that cached pages are cleared.
$wgCacheEpoch = max( $wgCacheEpoch, gmdate( 'YmdHis', @filemtime( __FILE__ ) ) );
>>>>>>>
""", [0]),
    ("""
<<<<<<<
***1***
?>
=======
# When you make changes to this configuration file, this will make
# sure that cached pages are cleared.
$wgCacheEpoch = max( $wgCacheEpoch, gmdate( 'YmdHis', @filemtime( __FILE__ ) ) );
>>>>>>>
""", [1, 0]),
    ("""
<<<<<<<
***1***
=======
# When you make changes to this configuration file, this will make
# sure that cached pages are cleared.
$wgCacheEpoch = max( $wgCacheEpoch, gmdate( 'YmdHis', @filemtime( __FILE__ ) ) );
>>>>>>>
""", [1, 0]),
    ]
}

