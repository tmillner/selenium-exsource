import sys
from unittest import TestLoader
import unittest

group = next((arg for arg in sys.argv if arg == "-g"), None)
tests = next((arg for arg in sys.argv if arg == "-t"), None)

loader = TestLoader()
tests = loader.discover("test/tests", "*Test.py", "./")
suite = unittest.TestSuite().addTest(tests)
result = unittest.TestResult()
unittest.TestSuite(tests=tests).run(result)
print (result)
