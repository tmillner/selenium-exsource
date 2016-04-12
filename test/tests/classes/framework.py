#!/usr/bin/python
from unittest import TestCase
import logging
import json
import os

class Framework(TestCase):
  """Framework
  context - targetd environment
  contextmap - targeted environments test data
  """

  TEST_CONTEXT_K = "PYTHON_TEST_CONTEXT"
  TEST_CONTEXT_V = ["TEST", "PROD"]

  def __init__(self, arg):
    super(Framework, self).__init__()
    self.arg = arg
    self.context = self._get_context()
    self.contextmap = self._setup_context(self.context)
    print self.__class__.__name__

  def _get_context():
    """Get the no-nonsense test context (env var)"""
    context = os.getenv(TEST_CONTEXT_K)
    if (context in TEST_CONTEXT_V):
      return context
    else:
      logging.info("Did't find valid env var '%s'. Continuing", TEST_CONTEXT_K)
      return None

  def _setup_context(context):
    """Establish contextmap with the target context data"""
    if (context):
      derivedClass = self.__class__.__name__ + ".json"
      print derivedClass
      with open(os.path.dirname(__file__) + "../" + derivedClass) as f:
        contextmap = json.load(f)
      logging.info("contextmap is %s", contextmap[context])
      return contextmap[context]

