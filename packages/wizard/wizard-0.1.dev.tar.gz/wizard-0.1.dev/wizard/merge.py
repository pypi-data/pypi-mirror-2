"""
Advanced merge tools for git rerere, sloppy commits and parametrization.

Wizard requires infrastructure for reusing merge resolutions across
many repositories, due to the number of user installs and highly
repetitive conflict resolution process.  This environment results
in a number of unique challenges:

    1. Users are commonly very sloppy with their text editors and
       will frequently change the line-ending style of their file.
       Because Git respects newline choice when core.autocrlf is
       off, a file that flips newline style will result in a full
       merge conflict.

    2. We version user configuration files, which means that there
       will always be a set of changes between upstream and ours.
       Since Git refuses to automatically merge changes that are
       too close to each other, these frequently result in spurious
       merge commits.

Furthermore, both of these make it difficult to reuse rerere resolutions
across installations.  Thus, an advanced Wizard merge has the following
properties:

    1. Wizard will perform a full scan of all files that were
       different between common and ours, filter out those that
       are binary (using as close to the Git heuristic as possible)
       and then check among common, ours and theirs if the newlines
       match.  The newline style of theirs always takes precedence.

    2. Wizard will genericize the ours copy so that it matches
       common and theirs, and reparametrize it once the merge
       is finished.  Consumers of this function should be careful
       to appropriately reparametrize if there are conflicts
       (we can't do it any earlier, because we want clean rerere
       postimages).

Usage of this functionality is primarily through the :func:`merge` function;
see that function more usage information.  While the ``git`` and ``newline``
functions published by this module are public, use of these functions outside
of this module is discouraged.
"""

import logging
import itertools
import tempfile
import os

import wizard
from wizard import shell

def git_commit_tree(tree, *parents):
    """
    Convenience wrapper for ``git commit-tree``.  Writes an empty log.
    """
    parent_args = itertools.chain(*(["-p", p] for p in parents))
    commit = shell.eval("git", "commit-tree", tree,
            *parent_args, input="", log=True)
    return commit

def git_diff_text(a, b):
    """
    Returns a list of files that are text and are different between
    commits ``a`` and ``b``.
    """
    lines = shell.eval("git", "diff", "--numstat", a, b).strip().split("\n")
    files = []
    for line in lines:
        added, deleted, name = line.split()
        if added != "-" and deleted != "-":
            files.append(name)
    return files

def git_newline_style(rev, name):
    """
    Returns the newline style for a blob, identified by Git revision
    ``rev`` and filename ``name``.
    """
    f = tempfile.NamedTemporaryFile(prefix="wizardResolve", delete=False)
    shell.call("git", "cat-file", "blob", "%s:%s" % (rev, name), stdout=f, log=False)
    f.close()
    nl = get_newline(f.name)
    os.unlink(f.name)
    return nl

# only works on Unix
def get_newline(filename):
    """
    Determines the newline style of ``filename``.  This will be a
    string if only one newline style was find, or a tuple of newline
    types found.
    """
    f = open(filename, 'U')
    f.read()
    return f.newlines

def convert_newline(filename, dest_nl):
    """
    Replaces the detected newline style of ``filename`` with
    ``dest_nl`` type newlines.
    """
    contents = open(filename, "U").read().replace("\n", dest_nl)
    open(filename, "wb").write(contents)

def merge(common_id, theirs_id,
          prepare_config=None,
          resolve_conflicts=None):
    """
    Performs a merge.  Throws a :class:`MergeError` if the merge fails
    (and leaves the current working directory in a state amenable
    to manual conflict resolution), or returns a tree id of the successful
    merge (the directory state is undefined and should not be relied upon).
    This function is not responsible for actually coming
    up with the real merge commit, because it can fail.

    If ``prepare_config`` is used, you are expected to reverse the effects
    of this on whatever the final tree is; otherwise you will lose
    those changes.

    Arguments:

        * ``common_id``: base commit to calculate merge off of
        * ``theirs_id``: changes to merge in from commit
        * ``prepare_config``: function that removes any user-specific
          values from files.  This function is expected to ``git add``
          any files it changes.
        * ``resolve_conflicts``: this function attempts to resolve
          conflicts automatically.  Returns ``True`` if all conflicts
          are resolved, and ``False`` otherwise.  It is permitted
          to resolve some but not all conflicts.

    .. note::

        Wizard has a strange idea of repository topology (due to lack of
        rebases, see documentation about doctoring retroactive commits),
        so we require the common and theirs commits, instead of
        using the normal Git algorithm.
    """
    if prepare_config is None:
        prepare_config = lambda: None
    if resolve_conflicts is None:
        resolve_conflicts = lambda: False
    ours_id = shell.eval("git", "rev-parse", "HEAD")
    theirs_newline_cache = {}
    def get_theirs_newline(file):
        if file not in theirs_newline_cache:
            nl = git_newline_style(theirs_id, file)
            if not isinstance(nl, str):
                if nl is not None:
                    # A case of incompetent upstream, unfortunately
                    logging.warning("Canonical version (theirs) of %s has mixed newline style, forced to \\n", file)
                else:
                    logging.debug("Canonical version (theirs) of %s had no newline style, using \\n", file)
                nl = "\n"
            theirs_newline_cache[file] = nl
        return theirs_newline_cache[file]
    theirs_tree = shell.eval("git", "rev-parse", "%s^{tree}" % theirs_id)
    # operations on the ours tree
    for file in git_diff_text(ours_id, theirs_id):
        try:
            theirs_nl = get_theirs_newline(file)
            ours_nl = get_newline(file) # current checkout is ours_id
        except (IOError, shell.CallError): # hack
            continue
        if theirs_nl != ours_nl:
            if ours_nl is None:
                logging.debug("File had no newlines, ignoring newline style")
            else:
                logging.info("Converting our file (3) from %s to %s newlines", repr(ours_nl), repr(theirs_nl))
                convert_newline(file, theirs_nl)
                shell.eval("git", "add", file)
    prepare_config() # for Wizard, this usually genericizes config files
    ours_tree = shell.eval("git", "write-tree")
    logging.info("Merge wrote virtual tree for ours: %s", ours_tree)
    # operations on the common tree (pretty duplicate with the above)
    shell.call("git", "reset", "--hard", common_id)
    for file in git_diff_text(common_id, theirs_id):
        try:
            theirs_nl = get_theirs_newline(file)
            common_nl = get_newline(file) # current checkout is common_id
        except (IOError, shell.CallError): # hack
            continue
        if theirs_nl != common_nl:
            if common_nl is None:
                logging.debug("File had no newlines, ignoring newline style")
            else:
                logging.info("Converting common file (1) from %s to %s newlines", repr(common_nl), repr(theirs_nl))
                convert_newline(file, theirs_nl)
                shell.eval("git", "add", file)
    common_tree = shell.eval("git", "write-tree")
    logging.info("Merge wrote virtual tree for common: %s", common_tree)
    # construct merge commit graph
    common_virtual_id = git_commit_tree(common_tree)
    ours_virtual_id   = git_commit_tree(ours_tree, common_virtual_id)
    theirs_virtual_id = git_commit_tree(theirs_tree, common_virtual_id)
    # perform merge
    shell.call("git", "reset", "--hard", ours_virtual_id)
    try:
        shell.call("git", "merge", theirs_virtual_id)
    except shell.CallError as e:
        logging.info("Merge failed with these message:\n\n" + e.stderr)
        if resolve_conflicts():
            logging.info("Resolved conflicts automatically")
            shell.call("git", "commit", "-a", "-m", "merge")
        else:
            raise MergeError
    # post-merge operations
    result_tree = shell.eval("git", "write-tree")
    logging.info("Resolution tree is %s", result_tree)
    return result_tree

class Error(wizard.Error):
    """Base error class for merge"""
    pass

class MergeError(Error):
    """Merge terminated with a conflict, oh no!"""
    pass
