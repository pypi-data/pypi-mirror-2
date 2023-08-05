import unittest

from wizard import resolve

class TestResolve(unittest.TestCase):

    def test_resolve_simple(self):
        contents = """
foo
bar
<<<<<<< HEAD
baz
|||||||
bal
=======
boo
>>>>>>> upstream
bing
"""
        spec = """
<<<<<<<
baz
=======
boo
>>>>>>>
"""
        result = [0]
        self.assertEqual(resolve.resolve(contents, spec, result), """
foo
bar
boo
bing
""")

    def test_resolve_simple_constrained(self):
        contents = """
1
<<<<<<< HEAD
2.1
|||||||
2
=======
2.a
>>>>>>> upstream
3
"""
        spec = """
<<<<<<< HEAD
2.1
|||||||
2
=======
2.a
>>>>>>> upstream
"""
        result = [0]
        self.assertEqual(resolve.resolve(contents, spec, result), """
1
2.a
3
""")

    def test_resolve_wildcard(self):
        contents = """
foo
bar
<<<<<<< HEAD
common
uncommon
still uncommon

|||||||
something else
=======
transformed common
>>>>>>> 456ef127bf8531bb363b1195172c71bce3747ae7
baz
"""

        spec = """
<<<<<<<
common
***1***
=======
transformed common
>>>>>>>
"""

        result = [0, 1]
        self.assertEqual(resolve.resolve(contents, spec, result), """
foo
bar
transformed common
uncommon
still uncommon

baz
""")

    def test_resolve_user(self):
        contents = """
top
<<<<<<<
bar
the user is right
baz
|||||||
something wonderful
=======
blah blah
>>>>>>>
bottom
<<<<<<<
Unrelated conflict
|||||||
something conflicty
=======
Unrelated conflicts
>>>>>>>"""
        spec = """
<<<<<<<
***1***
the user is right
***2***
=======
blah blah
>>>>>>>
"""
        result = [-1]
        self.assertEqual(resolve.resolve(contents, spec, result), """
top
bar
the user is right
baz
bottom
<<<<<<<
Unrelated conflict
|||||||
something conflicty
=======
Unrelated conflicts
>>>>>>>""")

    def test_resolve_multi_var(self):
        contents = """
top
<<<<<<<
the user is right
this is ours
more user stuff
this is ours
|||||||
Something special?
=======
this is kept, but variable
this is not kept
>>>>>>>
bottom
<<<<<<<
unrelated conflict
|||||||
original text of unrelated conflict
=======
unrelated conflicts
>>>>>>>
"""
        spec = """
<<<<<<<
***1***
this is ours
***2***
this is ours
=======
***3***
this is not kept
>>>>>>>
"""
        result = [3, 1, 2]
        self.assertEqual(resolve.resolve(contents, spec, result), """
top
this is kept, but variable
the user is right
more user stuff
bottom
<<<<<<<
unrelated conflict
|||||||
original text of unrelated conflict
=======
unrelated conflicts
>>>>>>>
""")

    def test_resolve_multi_simple(self):
        contents = """
bar
<<<<<<< HEAD
baz
|||||||
bollocks
=======
boo
>>>>>>> upstream
bing
<<<<<<< HEAD
oh?
|||||||
puntful
=======
bad match
>>>>>>> upstream
"""
        spec = """
<<<<<<<
***1***
=======
bad match
>>>>>>>
"""
        result = [-1]
        self.assertEqual(resolve.resolve(contents, spec, result), """
bar
<<<<<<< HEAD
baz
|||||||
bollocks
=======
boo
>>>>>>> upstream
bing
oh?
""")

def test_is_conflict():
    assert not resolve.is_conflict("foobar\nbar")
    assert resolve.is_conflict("bar\n<<<<<<< HEAD\n=======\n>>>>>>> abcd\nbar")
