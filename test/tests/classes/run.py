import sys
import os
import unittest
import importlib
from test.tests.classes import Framework

TEST_ROOT = "test/tests"


class Run:
    @staticmethod
    def _get_tests(arg, dirname, names):
        for name in names:
            if "Test.py" in name and "Test.pyc" not in name:
                test = {}
                testpath = dirname + "/" + name
                print testpath
                test['path'] = testpath
                test['module_file'] = testpath.split(".")[0].replace("/", ".")
                for attr in dir(importlib.import_module(test['module_file'])):
                    if "Test" in attr:
                        test['class'] = attr
                        break
                test['module_class'] = test['module_file'] + "." + test['class']
                arg += [test]

    @staticmethod
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

    @staticmethod
    def _match_tests(alltests, in_tests):
        out_tests = []
        for in_test in in_tests:
            for test in alltests:
                if in_test == test['class']:
                    out_tests += [test]
                    break
        return out_tests

    @staticmethod
    def get_testmatches(tests=None, groups=None):
        if tests is not None:
            by = tests
            process = Run._match_tests
        elif groups is not None:
            by = groups
            process = Run._match_groups
        in_list = by.split(",")
        alltests = []
        os.path.walk(TEST_ROOT, Run._get_tests, alltests)
        return process(alltests, in_list)

    @staticmethod
    def setEnv(env):
        os.environ[Framework.TEST_CONTEXT_K] = env
        return Run

    @staticmethod
    def help():
        return """
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

    @staticmethod
    def run(tests=None):
        loader = unittest.TestLoader()
        if tests is None:
            tests = loader.discover("test/tests", "*Test.py")
            result = unittest.TextTestResult(sys.stderr, True, 1)
            tests.run(result)
        else:
            suite = unittest.TestSuite()
            for test in tests:
                testmethods = loader.loadTestsFromName(test['module_class'])
                suite.addTest(testmethods)
            result = unittest.TextTestResult(sys.stderr, True, 1)
            suite.run(result)
        return str(result)

    @staticmethod
    def tests(tests):
        return Run.run(Run.get_testmatches(tests=tests))

    @staticmethod
    def groups(groups):
        return Run.run(Run.get_testmatches(groups=groups))
