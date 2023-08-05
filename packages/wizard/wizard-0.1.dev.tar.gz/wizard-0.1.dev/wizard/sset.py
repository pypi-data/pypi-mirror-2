import os.path

def make(seen_file):
    """
    Return a :class:`SerialisedSet` if given any non-empty string.
    If given an empty string, return a :class:`DummySerialisedSet`.
    """
    if seen_file:
        return SerializedSet(seen_file)
    else:
        return DummySerializedSet()

class ISerializedSet(object):
    """A unique unordered collection of strings."""
    def add(self, name):
        """Adds a value into the set."""
        raise NotImplementedError

class SerializedSet(ISerializedSet):
    """
    This set also records itself to a file, so that it
    is persisted over multiple sessions.
    """
    def __init__(self, file):
        self.set = set()
        if os.path.isfile(file):
            for line in open(file, "r"):
                self.set.add(line.rstrip())
        self.file = open(file, "a")
    def __contains__(self, name):
        return name in self.set
    def add(self, name):
        """Adds a value into the set."""
        self.set.add(name)
        self.file.write(name + "\n")
        self.file.flush()

class DummySerializedSet(ISerializedSet):
    """
    Dummy object that doesn't actually cache anything and
    claims that everything needs to be done.
    """
    def __contains__(self, name):
        return False
    def add(self, name):
        """Doesn't do anything."""
        pass
