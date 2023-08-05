import traceback

from wizard import tests
from wizard.util import *

lockfile = tests.getTestFile("util_test.lock")

class MyError(Exception):
    def __str__(self):
        return """

ERROR: Foo
"""

class MyErrorWithHTML(Exception):
    def __str__(self):
        return """

ERROR: Bar

<html>
    <title>No good!</title>
</html>
"""

def test_dictmap():
    assert dictmap(lambda x: x + 1, {'a': 0, 'b': 1}) == {'a': 1, 'b': 2}

def test_get_exception_name():
    try:
        raise NotImplementedError
    except NotImplementedError:
        assert get_exception_name(traceback.format_exc()) == "NotImplementedError"

def test_get_exception_name_withstr():
    try:
        raise MyError
    except MyError:
        assert get_exception_name(traceback.format_exc()) == "MyError"

def test_get_exception_name_withhtml():
    try:
        raise MyErrorWithHTML
    except MyErrorWithHTML:
        assert get_exception_name(traceback.format_exc()) == "MyErrorWithHTML"

def test_get_exception_name_withstr2():
    try:
        raise Exception("This is extra info we don't care about");
    except Exception:
        assert get_exception_name(traceback.format_exc()) == "Exception"

def test_lock():
    soft_unlink(lockfile)
    with LockDirectory(lockfile):
        pass

def test_locked():
    soft_unlink(lockfile)
    with LockDirectory(lockfile):
        try:
            with LockDirectory(lockfile):
                assert False
        except DirectoryLockedError:
            pass

def test_break_orphan_lock():
    soft_unlink(lockfile)
    open(lockfile, "w").write("obviouslyboguspid")
    with LockDirectory(lockfile):
        pass

def test_break_stale_lock():
    soft_unlink(lockfile)
    with LockDirectory(lockfile):
        with LockDirectory(lockfile, expiry = 0):
            pass

def test_disk_usage():
    assert disk_usage(tests.getTestFile("disk_usage_test"), "ignore_me") ==  7
