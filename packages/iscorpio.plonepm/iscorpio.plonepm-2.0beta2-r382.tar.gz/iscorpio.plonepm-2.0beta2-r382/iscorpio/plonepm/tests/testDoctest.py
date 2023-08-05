
# testDoctest.py

"""
The first step to use doctest for unit testing.
"""

import unittest
import doctest

from Testing import ZopeTestCase

from base import PlonepmFunctionalTestCase

__author__ = "Sean Chen"
__email__ = "sean.chen@leocorn.com"

def test_suite():

    return unittest.TestSuite([

        ZopeTestCase.ZopeDocFileSuite('README.txt',
                                      package='iscorpio.plonepm',
                                      test_class=PlonepmFunctionalTestCase),
                           
        ZopeTestCase.ZopeDocFileSuite('tests/README.txt',
                                      package='iscorpio.plonepm'),

        # other text files.
        ])
