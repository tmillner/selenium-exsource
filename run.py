#!/usr/bin/python
#  If running this in virtualenv use the python in it's dir e.g.
#  python run.py
import sys
import os
import unittest
import importlib
from test.tests.classes import Framework


def get_optionarg(opt):
    try:
        arg = None
        for i in range(len(sys.argv)):
            if opt == sys.argv[i]:
                arg = sys.argv[i+1]
                break
        return arg
    except IndexError as err:
        exit(str.format("Specify an arg after option.\n{}", err.message))

env = get_optionarg("-e")
groups = get_optionarg("-g")
tests = get_optionarg("-t")
helpme = next((arg for arg in sys.argv if arg == "-h"), None)
loader = unittest.TestLoader()
TEST_ROOT = "test/tests/"

if helpme is not None:
    print """
Run the test suite (tests or groups) under an environment (context).
-h            |   print this (help) info
-e ENV        |   set the environment ({ENV} = Valid context, from Framework)
-t T1,T2,...  |   run the target test classes ({T1} = TestClass (DoctorTest))
-g G1,G2,...  |   run the target test groups ({G1} = Test group in TestClass)

For -t and -g options, use only 1 or the other.

Example usage:
-- Run all tests, in Production:
  $ ./run.py -e PROD
-- Run "SimpleTest" test, in Test:
  $ ./run.py -e TEST -t SimpleTest
-- Run tests marked with "perf" and "security" groups, in TEST:
  $ ./run.py -e TEST -g perf,security
    """
    exit()

if groups is not None and tests is not None:
    exit("Sorry, I don't do magic. Specify either a test or group only.")

if env is not None:
    os.environ[Framework.TEST_CONTEXT_K] = env

if groups is None and tests is None:
    tests = loader.discover("test/tests", "*Test.py")
    result = unittest.TextTestResult(sys.stderr, True, 1)
    tests.run(result)
    print result
    exit()


def _get_tests(arg, dirname, names):
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


def _match_groups(alltests, in_groups):
    out_groups = []
    for test in alltests:
        module = importlib.import_module(test['module_file'])
        testgroup = getattr(getattr(module, test['class']), "GROUP", None)
        if testgroup is not None:
            for g in [(ig, tg) for ig in in_groups for tg in testgroup]:
                if g[0] == g[1]:
                    out_groups += [test]
                    break
    return out_groups


def _match_tests(alltests, in_tests):
    out_tests = []
    for in_test in in_tests:
        for test in alltests:
            if in_test == test['class']:
                out_tests += [test]
                break
    return out_tests


def get_testmatches():
    try:
        if tests is not None:
            by = tests
            process = _match_tests
        elif groups is not None:
            by = groups
            process = _match_groups
        in_list = by.split(",")
        alltests = []
        os.path.walk(TEST_ROOT, _get_tests, alltests)
        return process(alltests, in_list)
    except Exception as err:
        exit(str.format("Uh oh...\n{}", err.message))


tests = get_testmatches()
suite = unittest.TestSuite()
for test in tests:
    testmethods = loader.loadTestsFromName(test['module_class'])
    suite.addTest(testmethods)

result = unittest.TextTestResult(sys.stderr, True, 1)
suite.run(result)
print result
