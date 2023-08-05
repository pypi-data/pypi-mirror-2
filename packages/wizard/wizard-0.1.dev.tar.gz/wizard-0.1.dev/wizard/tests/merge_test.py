import unittest

from wizard import tests
from wizard.merge import *

sampleFile = tests.getTestFile("merge_test.sample")

class NewlineTest(unittest.TestCase):
    def testGetNewlineUnix(self):
        open(sampleFile, "wb").write("\n\n\n")
        self.assertEqual(get_newline(sampleFile), "\n")
        os.unlink(sampleFile)
    def testGetNewlineMixed(self):
        open(sampleFile, "wb").write("\n\n\n\n\n\n\r\n")
        self.assertEqual(get_newline(sampleFile), ("\n", "\r\n"))
        os.unlink(sampleFile)
    def testConvertNewline(self):
        open(sampleFile, "wb").write("\r\n\r\n\n")
        convert_newline(sampleFile, "\r")
        self.assertEqual(open(sampleFile, "rb").read(), "\r\r\r")
        os.unlink(sampleFile)

