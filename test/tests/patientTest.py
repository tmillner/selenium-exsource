#!/usr/bin/python
from classes import Framework
from classes import Page
import unittest


# This class would also go in it's own file. For brevity, it's here.
class PatientPage(Page):

    def __init__(self):
        super(PatientPage, self).__init__()
        self.pageInfo["path"] = "test/resources/patients.html"

    def get_first_patient_id(self):
        return self.driver.find_element_by_id("first_id").text

    def get_first_patient_fname(self):
        return self.driver.find_element_by_id("first_first-name").text


class PatientTest(Framework):
    GROUP = ["simple"]

    def test_patient(self):
        Page().jump_to(self.contextmap.get("startPage"))
        pp = PatientPage()
        patient_id = pp.get_first_patient_id()
        self.assertEqual(patient_id, self.contextmap.get("firstPatientId"),
                         "patiend id's don't match")
        patient_fname = pp.get_first_patient_fname()
        self.assertEqual(patient_fname,
                         self.contextmap.get("firstPatientName"),
                         "patiend id's don't match")

if __name__ == '__main__':
    unittest.main()
