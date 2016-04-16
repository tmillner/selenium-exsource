#!/usr/bin/python
from classes import Framework
import unittest


class DoctorTest(Framework):

    def test_patient(self):
        print self.context

if __name__ == '__main__':
    unittest.main()
