"""
.. highlight:: diff

This module contains algorithms for performing conflict
resolution after Git performs its recursive merge.  It
defines a simple domain specific language (that, at
its simplest form, merely involves copying conflict markers
and writing in the form that they should be resolved as) for
specifying how to resolve conflicts.  These are mostly relevant
for resolving conflicts in configuration files.

The conflict resolution DSL is described here:

Resolutions are specified as input-output pairs.  An input
is a string with the conflict resolution markers ``("<" * 7,
"=" * 7 and ">" * 7)``, with the HEAD content above the equals
divider, and the upstream content below the equals divider.
Lines can also be marked as ``***N***`` where N is a natural
number greater than 0 (i.e. 1 or more), which means that
an arbitrary number of lines may be matched and available for output.

Output is a list of integers and strings.  Integers expand
to lines that were specified earlier; -1 and 0 are special integers
that correspond to the entire HEAD text, and the entire upstream
text, respectively.  Strings can be used to insert custom lines.

The DSL does not currently claim to support character level granularity.
It also does not claim to support contiguous conflicts.
Our hope is that this simple syntax will be sufficient to cover
most common merge failures.

Here are some examples::

    <<<<<<<
    downstream
    |||||||
    common
    =======
    upstream
    >>>>>>>

With ``[-1]`` would discard all upstream changes, whereas with ``[0]``
would discard downstream changes (you would probably want to be
careful about wildcarding in the upstream string).

Pattern matching in action::

    <<<<<<<
    ***1***
    old upstream
    ***2***
    old upstream
    ***3***
    =======
    new upstream
    >>>>>>>

With ``[0, 1, 2, 3]`` would resolve with the new upstream text, and
then the user matched globs.
"""

import re
import itertools
import logging

re_var = re.compile("^\*\*\*(\d+)\*\*\*\\\n", re.MULTILINE)

def spec_to_regex(spec):
    """
    Translates a specification string into a regular expression tuple.
    Note that pattern matches are out of order, so the second element
    of the tuple is a dict specified strings to subpattern numbers.
    Requires re.DOTALL for correct operation.
    """
    ours, _, theirs = "".join(spec.strip().splitlines(True)[1:-1]).partition("=======\n")
    def regexify(text, fullmatch, matchno):
        text_split = re.split(re_var, text)
        ret = ""
        mappings = {fullmatch: matchno}
        for is_var, line in zip(itertools.cycle([False, True]), text_split):
            if is_var:
                ret += "(.*\\\n)"
                matchno += 1
                mappings[int(line)] = matchno
            else:
                ret += re.escape(line)
        return ("(" + ret + ")", mappings)
    ours, split, common = ours.partition("|||||||\n")
    if not split:
        common = "***9999***\n" # force wildcard behavior
    ours_regex, ours_mappings     = regexify(ours,   -1, 1)
    common_regex, common_mappings = regexify(common, -2, 1 + len(ours_mappings))
    theirs_regex, theirs_mappings = regexify(theirs,  0, 1 + len(ours_mappings) + len(common_mappings))
    # unify the mappings
    ours_mappings.update(theirs_mappings)
    ours_mappings.update(common_mappings)
    return ("<<<<<<<[^\n]*\\\n" + ours_regex + "\|\|\|\|\|\|\|\\\n" + common_regex + "=======\\\n" + theirs_regex + ">>>>>>>[^\n]*(\\\n|$)", ours_mappings)

def result_to_repl(result, mappings):
    """
    Converts a list of replacement strings and or references
    into a replacement string appropriate for a regular expression.
    """
    def ritem_to_string(r):
        if type(r) is int:
            return "\\%d" % mappings[r]
        else:
            return r + "\n"
    return "".join(map(ritem_to_string, result))

def resolve(contents, spec, result):
    """
    Given a conflicted file, whose contents are ``contents``, attempt
    to resolve all conflicts that match ``spec`` with ``result``.
    """
    rstring, mappings = spec_to_regex(spec)
    regex = re.compile(rstring, re.DOTALL)
    repl = result_to_repl(result, mappings)
    ret = ""
    conflict = ""
    status = 0
    for line in contents.splitlines(True):
        if status == 0 and line.startswith("<<<<<<<"):
            status = 1
        elif status == 1 and line.startswith("|||||||"):
            status = 2
        elif status == 1 or status == 2 and line.startswith("======="):
            status = 3
        # ok, now process
        if status == 3 and line.startswith(">>>>>>>"):
            status = 0
            conflict += line
            ret += regex.sub(repl, conflict)
            conflict = ""
        elif status:
            conflict += line
        else:
            ret += line
    return ret

def is_conflict(contents):
    """
    Given ``contents``, return ``True`` if there are any conflicts in it.
    """
    # Really really simple heuristic
    return "<<<<<<<" in contents

