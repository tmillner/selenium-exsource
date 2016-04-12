#!/usr/bin/python
from classes import Framework
import unittest

# Desired outsourced data
class PatientTest(Framework):

  def __init__(self):
    super(PatientTest, self).__init__()

  def test_patient_page():
    print "done"
    
if __name__ == '__main__':
  unittest.main()