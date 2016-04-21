#!/usr/bin/python
# This file will also hit other class modules:
#  - logger,
#  - page,
#  - driver
import unittest
import subprocess
from test.tests.classes import Run


class RunTests(unittest.TestCase):

    def __init__(self, args):
        super(RunTests, self).__init__(args)
        self.subprocesses = []

    def setUp(self):
        sp = subprocess.Popen(["python", "-m", "SimpleHTTPServer", "8080"])
        self.subprocesses += [sp]

    def tearDown(self):
        [sp.terminate() for sp in self.subprocesses]

    def test_0_help(self):
        res = Run.help()
        self.assertIn("Example usage:", res)

    def test_1_run_all(self):
        res = Run.setEnv("PROD").run()
        self.assertIn("run=2 errors=0 failures=0", res)

    def test_2_run_groups(self):
        res = Run.setEnv("TEST").groups("example,fast")
        self.assertIn("run=1 errors=0 failures=0", res)

    def test_3_run_tests(self):
        res = Run.setEnv("PROD").tests("DoctorTest")
        self.assertIn("run=1 errors=0 failures=0", res)

    def test_4_run_invalid_test(self):
        res = Run.setEnv("TEST").tests("abc,,,[]")
        self.assertIn("run=0 errors=0 failures=0", res)

    def test_5_run_invalid_group(self):
        res = Run.setEnv("PROD").groups("[],{},(),[],,#")
        self.assertIn("run=0 errors=0 failures=0", res)

    def test_6_run_invalid_env(self):
        # Same flow as run on no environment
        res = Run.setEnv("nana").tests("DoctorTest,PatientTest")
        self.assertIn("run=2 errors=1 failures=0", res)

    def test_7_run_no_env(self):
        res = Run().setEnv("").run()
        # Blows up in trying to run everything in the tests
        self.assertIn("run=2 errors=3 failures=0", res)
