import os
import re
import logging
import distutils
import distutils.version
import urlparse
import hashlib
import sqlalchemy.exc

from wizard import app, install, resolve, sql, util
from wizard.app import php

def make_filename_regex_define(var):
    """See :ref:`versioning config <seed>` for more information."""
    return 'wp-config.php', php.re_define(var)

seed = util.dictmap(make_filename_regex_define, {
    # these funny names are due to convention set by MediaWiki
    'WIZARD_DBSERVER': 'DB_HOST',
    'WIZARD_DBNAME': 'DB_NAME',
    'WIZARD_DBUSER': 'DB_USER',
    'WIZARD_DBPASSWORD': 'DB_PASSWORD',
    'WIZARD_SECRETKEY': 'SECRET_KEY',
    'WIZARD_AUTH_KEY': 'AUTH_KEY',
    'WIZARD_SECURE_AUTH_KEY': 'SECURE_AUTH_KEY',
    'WIZARD_LOGGED_IN_KEY': 'LOGGED_IN_KEY',
    'WIZARD_NONCE_KEY': 'NONCE_KEY',
    'WIZARD_AUTH_SALT': 'AUTH_SALT',
    'WIZARD_SECURE_AUTH_SALT': 'SECURE_AUTH_SALT',
    'WIZARD_LOGGED_IN_SALT': 'LOGGED_IN_SALT',
    'WIZARD_NONCE_SALT': 'NONCE_SALT',
    })

class Application(app.Application):
    database = "mysql"
    parametrized_files = ['wp-config.php'] + php.parametrized_files
    extractors = app.make_extractors(seed)
    extractors.update(php.extractors)
    substitutions = app.make_substitutions(seed)
    substitutions.update(php.substitutions)
    install_schema = install.ArgSchema("db", "admin", "email", "title")
    deprecated_keys = set(['WIZARD_SECRETKEY'])
    random_keys = set([
        'WIZARD_SECRETKEY',
        'WIZARD_AUTH_KEY',
        'WIZARD_SECURE_AUTH_KEY',
        'WIZARD_LOGGED_IN_KEY',
        'WIZARD_NONCE_KEY',
        'WIZARD_AUTH_SALT',
        'WIZARD_SECURE_AUTH_SALT',
        'WIZARD_LOGGED_IN_SALT',
        'WIZARD_NONCE_SALT',
        ])
    random_blacklist = set(['put your unique phrase here'])
    def urlFromExtract(self, deployment):
        try:
            meta = sql.connect(deployment.dsn)
            try:
                wp_options = meta.tables["wp_options"]
            except KeyError:
                return None
            query = wp_options.select(wp_options.c.option_name == 'home')
            return query.execute().fetchone()['option_value']
        except sqlalchemy.exc.OperationalError:
            return None
    def download(self, version):
        return "http://wordpress.org/wordpress-%s.tar.gz" % version
    def checkConfig(self, deployment):
        return os.path.isfile("wp-config.php")
    def checkWeb(self, deployment):
        return self.checkWebPage(deployment, "",
                outputs=["<html", "WordPress", "feed"],
                exclude=["Error establishing a database connection", "Account unknown"])
    def detectVersion(self, deployment):
        return self.detectVersionFromFile("wp-includes/version.php", php.re_var("wp_version"))
    def install(self, version, options):
        util.soft_unlink("wp-config.php")

        post_setup_config = {
                'dbhost': options.dsn.host,
                'uname': options.dsn.username,
                'dbname': options.dsn.database,
                'pwd': options.dsn.password,
                'prefix': '',
                'submit': 'Submit',
                'step': '2',
                }
        post_install = {
                'weblog_title': options.title,
                'admin_email': options.email,
                'submit': 'Continue',
                'step': '2',
                # Version >= 3.0
                'user_name': options.admin_name,
                'admin_password': options.admin_password,
                'admin_password2': options.admin_password,
                }
        old_mode = os.stat(".").st_mode
        os.chmod(".", 0777) # XXX: squick squick

        # we need to disable the wp_mail function in wp-includes/pluggable[-functions].php
        pluggable_path = os.path.exists('wp-includes/pluggable.php') and 'wp-includes/pluggable.php' or 'wp-includes/pluggable-functions.php'
        pluggable = open(pluggable_path, 'r').read()
        wp_mail_noop = "<?php function wp_mail( $to, $subject, $message, $headers = '', $attachments = array() ) { /*noop*/ } ?> \n\n"
        pluggable_file = open(pluggable_path,'w')
        pluggable_file.write(wp_mail_noop)
        pluggable_file.write(pluggable)
        pluggable_file.close()

        result = install.fetch(options, "wp-admin/setup-config.php?step=2", post_setup_config)
        logging.debug("setup-config.php output\n\n" + result)
        result = install.fetch(options, "wp-admin/install.php?step=2", post_install)
        logging.debug("install.php output\n\n" + result)
        os.chmod(".", old_mode)
        if "Finished" not in result and "Success" not in result:
            raise app.InstallFailure()

        # not sure what to do about this
        meta = sql.connect(options.dsn)
        wp_options = meta.tables["wp_options"]
        wp_options.update().where(wp_options.c.option_name == 'siteurl').values(option_value=options.web_path).execute()
        wp_options.update().where(wp_options.c.option_name == 'home').values(option_value="http://%s%s" % (options.web_host, options.web_path)).execute() # XXX: what if missing leading slash; this should be put in a function

        if version < distutils.version.LooseVersion("3.0"):
            wp_users = meta.tables["wp_users"]
            hashed_pass = hashlib.md5(options.admin_password).hexdigest()
            wp_users.update().where(wp_users.c.ID == 1).values(user_login=options.admin_name,user_nicename=options.admin_name,display_name=options.admin_name,user_pass=hashed_pass).execute()
            wp_usermeta = meta.tables["wp_usermeta"]
            wp_usermeta.delete().where(wp_usermeta.c.user_id==1 and wp_usermeta.c.meta_key == "default_password_nag").execute()

        # now we can restore the wp_mail function in wp-includes/pluggable[-functions].php
        pluggable_file = open(pluggable_path,'w')
        pluggable_file.write(pluggable)
        pluggable_file.close()

        # replace random variable stubs with real values
        old_config = open('wp-config.php').read()
        def replace_with_random(s):
            return s.replace('put your unique phrase here', util.random_key(), 1)
        config = replace_with_random(old_config)
        while config != old_config:
            old_config = config
            config = replace_with_random(config)
        open('wp-config.php', 'w').write(config)

        php.ini_replace_vars()
    def upgrade(self, d, version, options):
        result = d.fetch("wp-admin/upgrade.php?step=1")
        if "Upgrade Complete" not in result and "No Upgrade Required" not in result:
            raise app.UpgradeFailure(result)
    def backup(self, deployment, backup_dir, options):
        app.backup_database(backup_dir, deployment)
    def restore(self, deployment, backup_dir, options):
        app.restore_database(backup_dir, deployment)
    def remove(self, deployment, options):
        app.remove_database(deployment)

Application.resolutions = {
'wp-config.php': [
    ("""
<<<<<<<

/** WordPress absolute path to the Wordpress directory. */
|||||||
/** WordPress absolute path to the Wordpress directory. */
=======
/** Absolute path to the WordPress directory. */
>>>>>>>
""", [0])
],
}
