from unittest import TestCase
from logger import log
from driver import Driver
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
            {"name": "TEST", "domain": "localhost", "port": "8080"},
            {"name": "PROD", "domain": "localhost", "port": "8080"}
        ]
    GROUPS = []  # Derived classes have their own

    def __init__(self, args):
        super(Framework, self).__init__(args)
        log.info("running test " + self.id())
        self.args = args
        self.context = self._get_context()
        if self.context:
            context_name = self.context.get("name")
            contextmap = self._setup_context(context_name)
            self.contextmap = contextmap.get(context_name)
        else:
            self.contextmap = {}
        Driver.CONTEXT = self.context

    def setUp(self):
        self._driver = Driver()

    def tearDown(self):
        self._driver.close()
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
            try:
                with open(os.path.dirname(
                  derivedfilepath) + "/" + derivedfilejson) as f:
                    contextmap = json.load(f)
                return self._find_target_context(contextmap)
            except IOError as err:
                self.tearDown()
                msg = str.format("\n{}\n'{}'", err.strerror, err.filename)
                exit("Attempt to find the external data file failed: " + msg)
            except ValueError as err:
                self.tearDown()
                msg = str.format("\n{}", err.message)
                exit("Invalid json format in input file: " + msg)

    def _find_target_context(self, contextmap):
        """Pick the target context data the test will run with"""
        log.debug("Loading context map with " + str(self.context))
        try:
            target_context = [o for o in contextmap.get("contexts") if
                              self.context.get("name") in o][0]
            return target_context
        except (AttributeError, IndexError) as err:
            self.tearDown()
            msg = str.format("{}\n{}", "Using context " +
                             self.context.get("name") + err.message)
            exit("Didn't find the target context in the json: " + msg)
