
import os
from xmlrunner import XMLTestRunner

import unittest

_main = unittest.main

# Patch needed to invoke setuptools `test` command
def main(*args, **kwds):
  if 'runner' in kwds :
    kwds['testRunner'] = kwds.pop('runner')
  return _main(*args, **kwds)

main.__doc__ = unittest.main.__doc__
unittest.main = main

def junitrunner():
  return XMLTestRunner(output=os.environ.get('BUILD_REPORT', '.') + '/xunit')

