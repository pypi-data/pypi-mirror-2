
# testUtils.py

"""
unit test cases for utils in PlonePM
"""

from unittest import TestCase
from unittest import TestSuite
from unittest import makeSuite

from iscorpio.plonepm.utils import revision2Link

__author__ = "Sean Chen"
__email__ = "sean.chen@leocorn.com"

class TestRevision2Link(TestCase):

    def testRevision2Link(self):

        description = 'this is a test revision r123'
        sf_base_url = 'http://sf.base.url/projectname'

        sf_result = "this is a test revision <a href='%s?view=rev&revision=%s'>%s</a>" % \
                    (sf_base_url, '123', 'r123')

        formatedDesc = revision2Link(description, sf_base_url)
        self.failUnless(formatedDesc == sf_result)

def test_suite():

    suite = TestSuite()
    suite.addTest(makeSuite(TestRevision2Link))

    return suite

    
