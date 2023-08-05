"""
Common data and functions for use in PHP applications.

.. testsetup:: *

    from wizard.app.php import *
"""

import re
import os

from wizard import app, util

def re_var(var):
    """
    Generates a regexp for assignment to ``var`` in PHP; the quoted
    value is the second subpattern.

    >>> re_var('key').search("$key = 'val';").group(2)
    "'val'"
    """
    return re.compile('^(\$' + app.expand_re(var) + r'''\s*=\s*)(.*)(;)''', re.M)

def re_define(var):
    """
    Generates a regexp for the definition of a constant in PHP; the
    quoted value is the second subpattern.

    >>> re_define('FOO').search("define('FOO', 'bar');").group(2)
    "'bar'"
    """
    return re.compile('^(define\([\'"]' + app.expand_re(var) + r'''['"]\s*,\s*)(.*)(\);)''', re.M)

def _make_filename_regex(var):
    return 'php.ini', re.compile('^(' + app.expand_re(var) + r'\s*=\s*)(.*)()$', re.M)

def ini_replace_vars():
    """
    Replace ``WIZARD_TMPDIR`` and ``WIZARD_SESSIONNAME`` with with user-specific values.
    """
    text = open('php.ini', "r").read()
    text = text.replace('WIZARD_TMPDIR', '/mit/%s/web_scripts_tmp' % os.environ['USER'])
    text = text.replace('WIZARD_SESSIONNAME', '%s_SID' % os.environ['USER'])
    open('php.ini', "w").write(text)

seed = util.dictmap(_make_filename_regex, {
        'WIZARD_SESSIONNAME': 'session.name',
        'WIZARD_TMPDIR': ('upload_tmp_dir', 'session.save_path'),
        })

#: Common extractors for parameters in :file:`php.ini`.
extractors = app.make_extractors(seed)
#: Common substitutions for parameters in :file:`php.ini`.
substitutions = app.make_substitutions(seed)
#: A list containing :file:`php.ini`.
parametrized_files = ["php.ini"]
#: Nop for consistency.
deprecated_keys = set([])

