#!/usr/bin/python
from classes import Framework
import unittest


class DoctorTest(Framework):
    GROUP = "a thing"

    def runTest(self):
        print "o"

    def testTest(self):
        print "eee"

if __name__ == '__main__':
    unittest.main()
