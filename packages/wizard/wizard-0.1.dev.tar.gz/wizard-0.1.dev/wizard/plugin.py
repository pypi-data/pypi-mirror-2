"""
Convenience methods for managing plugins.
"""

import pkg_resources

def hook(name, args):
    """
    Runs plugins named ``name`` for this function.  Returns ``None`` if
    all plugins return ``None``, otherwise returns the result of the
    first plugin to result that is not ``None``. Assumes that plugins
    are simple functions that take the arguments ``args``.
    """
    for entry in pkg_resources.iter_entry_points(name):
        func = entry.load()
        r = func(*args)
        if r is not None:
            return r
    return None
