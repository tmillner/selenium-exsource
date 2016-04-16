#!/usr/bin/python
from classes import Framework
from classes import Page
import unittest


# This class would also go in it's own file. For brevity, it's here.
class PatientPage(Page):

    def __init__(self):
        super(PatientPage, self).__init__()
        self.pageInfo["path"] = "patients"


class PatientTest(Framework):

    def runTest(self):
        """Only this method will run if the file is run without unittest"""
        print self.context

    def thisWontRun(self):
        """This will never run"""
        print("BOO!")

    def test_patient(self):
        """Only this method will run if ran via TestLoader (discover)"""
        print self.context

if __name__ == '__main__':
    unittest.main()
