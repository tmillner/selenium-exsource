#!/usr/bin/python
from classes import Framework
import unittest


class DoctorTest(Framework):
    GROUP = ["simple", "fast"]

    def runTest(self):
        print "o"

    def testTest(self):
        print "eee"

    def testAnother(self):
        print "another"

if __name__ == '__main__':
    unittest.main()
