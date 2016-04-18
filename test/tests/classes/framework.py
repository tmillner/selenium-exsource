from unittest import TestCase
import unittest
from logger import log
import inspect
import json
import os


class Framework(TestCase):
    """Framework
    context - targeted environment
    contextmap - targeted environments test data
    """

    TEST_CONTEXT_K = "PYTHON_TEST_CONTEXT"
    TEST_CONTEXT_V = [
            {"name": "TEST", "domain": "localhost"},
            {"name": "PROD", "domain": "localhost"}
        ]
    GROUPS = []  # Derived classes have their own

    def __init__(self, args):
        super(Framework, self).__init__(args)
        self.args = args
        self.context = self._get_context()
        if self.context:
            self.contextmap = self._setup_context(self.context.get("name"))
        else:
            self.contextmap = {}

    def setUp(self):
        pass

    def tearDown(self):
        self.context = None
        self.contextmap = None

    def _get_context(self):
        """Get the no-nonsense test context (env var)"""
        context = os.getenv(Framework.TEST_CONTEXT_K)
        match = next((c for c in self.TEST_CONTEXT_V
                     if c.get("name") == context), {})
        if match:
            return match
        else:
            log.info("Didn't find valid env var '%s'. Continuing",
                     Framework.TEST_CONTEXT_K)

    def _setup_context(self, context):
        """Establish contextmap with the target context data"""
        if context:
            derivedfilepath = inspect.getfile(self.__class__)
            derivedfile = os.path.basename(derivedfilepath)
            derivedfilejson = derivedfile.split(".")[0] + ".json"
            print derivedfilejson
            try:
                with open(os.path.dirname(
                  derivedfilepath) + "/" + derivedfilejson) as f:
                    contextmap = json.load(f)
                return self._find_target_context(contextmap)
            except IOError as err:
                msg = str.format("\n{}\n'{}'", err.strerror, err.filename)
                exit("Attempt to find the external data file failed: " + msg)
            except ValueError as err:
                msg = str.format("\n{}", err.message)
                exit("Invalid json format in input file: " + msg)

    def _find_target_context(self, contextmap):
        """Pick the target context data the test will run with"""
        log.debug("Loading context map with " + self.context)
        try:
            return [o for o in contextmap.get("contexts") if
                    self.context in o][0]
        except (AttributeError, IndexError) as err:
            msg = str.format("{}\n{}", "Using context " + self.context,
                             err.message)
            exit("Didn't find the target context in the json: " + msg)


if __name__ == "__main__":
    unittest.main()