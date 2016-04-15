#!/usr/bin/python
from classes import Framework
import unittest

# Desired outsourced data
class PatientTest(Framework):

  def runTest(self):
    print self.context
    
if __name__ == '__main__':
  unittest.main()