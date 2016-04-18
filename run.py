#!/usr/bin/python
import sys
import os
import unittest
import importlib
from test.tests.classes import Framework

env = next((arg for arg in sys.argv if arg == "-e"), None)
group = next((arg for arg in sys.argv if arg == "-g"), None)
tests = next((arg for arg in sys.argv if arg == "-t"), None)
helpme = next((arg for arg in sys.argv if arg == "-h"), None)
loader = unittest.TestLoader()
TEST_ROOT = "test/tests/"

if helpme is not None:
    print """
Run the test suite (tests or groups) under an environment (context).
-h              |   print this (help) info
-e={ENV}        |   set the environment ({ENV} = Valid context, from Framework)
-t={T1,T2,...}  |   run the target test classes ({T1} = TestClass (DoctorTest))
-g={G1,G2,...}  |   run the target test groups ({G1} = Test group in TestClass)


For -t and -g options use only 1 or the other.
    """
    exit()

if env is not None:
    os.environ[Framework.TEST_CONTEXT_K] = env

if group is not None and tests is not None:
    exit("Sorry, I don't do magic. Specify either a test or group only.")

#  Run everything if no options are provided
if group is None and tests is None:
    tests = loader.discover("test/tests", "*Test.py")
    result = unittest.TextTestResult(sys.stderr, True, 1)
    tests.run(result)
    print result
    exit()


#  Find files in test root, that adhere to Test protocol
def get_tests(arg, dirname, names):
    for name in names:
        if "Test.py" in name and "Test.pyc" not in name:
            test = {}
            testpath = dirname + name
            test['path'] = testpath
            test['module_file'] = testpath.split(".")[0].replace("/", ".")
            for attr in dir(importlib.import_module(test['module_file'])):
                if "Test" in attr:
                    test['class'] = attr
                    break
            test['module_class'] = test['module_file'] + "." + test['class']
            arg += [test]


tests = []
os.path.walk(TEST_ROOT, get_tests, tests)
print tests
suite = unittest.TestSuite()
for test in tests:
    testmethods = loader.loadTestsFromName(test['module_file'])
    suite.addTest(testmethods)

result = unittest.TextTestResult(sys.stderr, True, 1)
suite.run(result)
print (result)
