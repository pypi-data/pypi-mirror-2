import os.path

def getTestFile(file):
    """
    Returns the path to a testfile in this test directory.
    """
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), file)

