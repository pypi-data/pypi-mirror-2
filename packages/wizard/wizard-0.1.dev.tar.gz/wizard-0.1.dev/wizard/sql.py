import sqlalchemy
import os
import pkg_resources
import copy

from wizard import shell

# We're going to use sqlalchemy.engine.url.URL as our database
# info intermediate object

def connect(url):
    """Convenience method for connecting to a MySQL database."""
    engine = sqlalchemy.create_engine(url)
    meta = sqlalchemy.MetaData()
    meta.bind = engine
    meta.reflect()
    return meta

def auth(url):
    """
    If the URL has a database name but no other values, it will
    use the global configuration, and then try the database name.

    This function implements a plugin interface named
    :ref:`wizard.sql.auth`.
    """
    if not url:
        return None
    if not url.database:
        # it's hopeless
        return url
    # omitted port and query
    if any((url.host, url.username, url.password)):
        # don't try for defaults if a few of these were set
        return url
    for entry in pkg_resources.iter_entry_points("wizard.sql.auth"):
        func = entry.load()
        r = func(copy.copy(url))
        if r is not None:
            return r
    env_dsn = os.getenv("WIZARD_DSN")
    if env_dsn:
        old_url = url
        url = sqlalchemy.engine.url.make_url(env_dsn)
        url.database = old_url.database
    return url
