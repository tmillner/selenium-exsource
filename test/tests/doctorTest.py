#!/usr/bin/python
from classes import Framework
import unittest


class DoctorTest(Framework):
    GROUP = ["simple", "fast", "example"]

    def testExample(self):
        self.assertEqual(True, True, "I'll never see the light of day")

if __name__ == '__main__':
    unittest.main()
