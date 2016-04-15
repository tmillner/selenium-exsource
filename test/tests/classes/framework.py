#!/usr/bin/python
from unittest import TestCase
import inspect
import logging
import json
import os

class Framework(TestCase):
  """Framework
  context - targeted environment
  contextmap - targeted environments test data
  """

  TEST_CONTEXT_K, TEST_CONTEXT_V  = "PYTHON_TEST_CONTEXT", ["TEST", "PROD"]

  def __init__(self, arg):
    super(Framework, self).__init__()
    self.arg = arg
    self.context = self._get_context()
    self.contextmap = self._setup_context(self.context)
    print self.contextmap

  def _get_context(self):
    """Get the no-nonsense test context (env var)"""
    context = os.getenv(Framework.TEST_CONTEXT_K)
    if (context in Framework.TEST_CONTEXT_V):
      return context
    else:
      logging.info("Didn't find valid env var '%s'. Continuing", 
        Framework.TEST_CONTEXT_K)

  def _setup_context(self, context):
    """Establish contextmap with the target context data"""
    if (context):
      derivedfilepath = inspect.getfile(self.__class__)
      derivedfile = os.path.basename(derivedfilepath)
      derivedfile_json = derivedfile.split(".")[0] + ".json"
      print derivedfile_json
      try:
        with open(
          os.path.dirname(derivedfilepath) + "/" + derivedfile_json) as f:
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
    logging.debug("Loading context map with " + self.context)
    try:
      return [o for o in contextmap.get("contexts") if 
      o.has_key(self.context)][0]
    except (AttributeError, IndexError) as err:
      msg = str.format("{}\n{}", "Using context " + self.context, err.message)
      exit("Didn't find the target context in the json: " + msg)
