import shutil
import logging
import os.path
import distutils.version

from wizard import app, install, resolve, util
from wizard.app import php

#phpBB                104 installs
#    2.0.19            87  ++++++++++++++++++++++++++++++
#    3.0.4             17  ++++++

CONFIG = 'config.php'
def make_filename_regex(var):
    """See :ref:`versioning config <seed>` for more information."""
    return CONFIG, php.re_var(var)

seed = util.dictmap(make_filename_regex, {
        'WIZARD_DBSERVER' : 'dbhost',
        'WIZARD_DBNAME' : 'dbname',
        'WIZARD_DBUSER' : 'dbuser',
        'WIZARD_DBPASSWORD' : 'dbpasswd' })

class Application(app.Application):
    install_schema = install.ArgSchema('db', 'admin', 'email', 'title')
    database = 'mysql'
    parametrized_files = [ CONFIG ] + php.parametrized_files
    extractors = app.make_extractors(seed)
    extractors.update(php.extractors)
    substitutions = app.make_substitutions(seed)
    substitutions.update(php.substitutions)

    def checkConfig(self, deployment):
        return os.path.getsize('config.php')

    def detectVersion(self, deployment):
        version = str(self.detectVersionFromFile('install/update_to_latest.php', php.re_var('updates_to_version')))
        if version.startswith('.'): # blehh, but phpBB2 uses '.0.19'...
            version = '2' + version
        return distutils.version.LooseVersion(version)

    def remove(self, deployment, options):
        app.remove_database(deployment)

    def install(self, version, options):
        old_mode = os.stat(".").st_mode
        os.chmod("config.php", 0777)
        self.install_2(options)
        os.chmod("config.php", old_mode)
        php.ini_replace_vars()

    def install_2(self, options):
        database_dict = {
                'lang' : 'english',
                'dbms' : 'mysql',
                'upgrade' : '0',
                'dbhost' : options.dsn.host,
                'dbname' : options.dsn.database,
                'dbuser' : options.dsn.username,
                'dbpasswd' : options.dsn.password,
                'prefix' : '',
                'board_email' : options.email,
                'server_name' : options.web_host,
                'server_port' : '80',
                'script_path' : options.web_path,
                'admin_name' : options.admin_name,
                'admin_pass1' : options.admin_password,
                'admin_pass2' : options.admin_password,
                'install_step' : '1',
                'cur_lang' : 'english' }

        result = install.fetch(options, 'install/install.php', database_dict)
        logging.debug('install.php output:\n\n' + result)
        if 'Thank you' not in result:
            raise app.InstallFailure()
        #shutil.rmtree('install')
        #shutil.rmtree('contrib')

    def install_3(self, options):
        def install_helper(sub, post):
            uri = 'install/index.php?mode=install&language=en'
            if sub:
                uri += '&sub=%s' % sub
            result = install.fetch(options, uri, post)
            logging.debug('%s (%s) output:\n\n' % (uri, sub) + result)
            return result

        # *deep breath*
        install_helper('', {})
        install_helper('requirements', {})

        database_dict = { 'img_imagick' : '/usr/bin/' }
        install_helper('database', database_dict)

        database_dict.update({
                'dbms' : 'mysql',
                'dbhost' : options.mysql_host,
                'dbname' : options.mysql_db,
                'dbuser' : options.mysql_user,
                'dbpasswd' : options.mysql_password,
                'table_prefix' : '',
                'img_imagick' : '/usr/bin/',
                'language' : 'en',
                'testdb' : 'true' })
        install_helper('database', database_dict)

        database_dict['dbport'] = ''
        del database_dict['testdb']
        install_helper('administrator', database_dict)

        database_dict.update({
                'default_lang' : 'en',
                'admin_name' : options.admin_name,
                'admin_pass1' : options.admin_password,
                'admin_pass2' : options.admin_password,
                'board_email1' : options.email,
                'board_email2' : options.email,
                'check' : 'true' })
        install_helper('administrator', database_dict)

        del database_dict['check']
        install_helper('config_file', database_dict)
        install_helper('advanced', database_dict)

        database_dict.update({
                'email_enable' : '1',
                'smtp_delivery' : '0',
                'smtp_auth' : 'PLAIN',
                'cookie_secure' : '0',
                'force_server_vars' : '0',
                'server_protocol' : 'http://',
                'server_name' : options.web_host,
                'server_port' : '80',
                'script_path' : options.web_path })
        install_helper('create_table', database_dict)

        database_dict.update({
                'ftp_path' : '',
                'ftp_user' : '',
                'ftp_pass' : '',
                'smtp_host' : '',
                'smtp_user' : '',
                'smtp_pass' : '' })
        install_helper('final', database_dict)
