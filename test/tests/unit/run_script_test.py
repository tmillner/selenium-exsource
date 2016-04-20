#!/usr/bin/python
# This file will also hit other class modules:
#  - logger,
#  - page,
#  - driver
import unittest
import subprocess
import os
from run import Run


class RunTests(unittest.TestCase):

    def __init__(self, args):
        super(RunTests, self).__init__(args)
        self.subprocesses = []

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_help(self):
        res = Run.help()
        self.assertIn("Example usage:", res, "Help isn't helpful")

    def test_run_all(self):
        res = Run.setEnv("PROD").run()
        self.assertIn("run=2 errors=0 failures=0", res, "Failures or erros :(")

    def test_run_groups(self):
        res = Run.setEnv("TEST").groups("example,fast")
        self.assertIn("run=1 errors=0 failures=0", res, "Failures or erros :(")

    def test_run_tests(self):
        res = Run.setEnv("PROD").tests("DoctorTest")
        self.assertIn("run=1 errors=0 failures=0", res, "Failures or erros :(")

    def test_run_invalid_env(self):
        pass

    def test_run_no_env(self):
        pass

