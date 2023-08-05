# testAtctType.py

"""
we will do the basic unit test for the new content types based on
ATContentTypes.
"""

import unittest

from Products.ATContentTypes.tests.atcttestcase import ATCTTypeTestCase
from Products.ATContentTypes.tests.test_atfolder import TestSiteATFolder
from Products.ATContentTypes.tests.test_atdocument import TestSiteATDocument

from iscorpio.plonepm.content.PPMProject import PPMProject
from iscorpio.plonepm.content.PPMMetadata import PPMMetadata
from iscorpio.plonepm.content.PPMIteration import PPMIteration

from iscorpio.plonepm.content.PPMArtifact import PPMArtifact
from iscorpio.plonepm.content.PPMResponse import PPMResponse

from iscorpio.plonepm.content.PPMFuncSpec import PPMFuncSpec
from iscorpio.plonepm.content.PPMFuncReq import PPMFuncReq
from iscorpio.plonepm.content.PPMSysReq import PPMSysReq
from iscorpio.plonepm.content.PPMUseCase import PPMUseCase
from iscorpio.plonepm.content.PPMStory import PPMStory

from iscorpio.plonepm.tests.base import PlonepmTestCase

__author__ = "Sean Chen"
__email__ = "sean.chen@leocorn.com"

# test cases list
tests = []

class TestPPMProject(TestSiteATFolder):
    """ Testing basics about the AT Content Types within this product.
    """

    klass = PPMProject
    portal_type = "PPMProject"
    # the title in the types xml file.
    title = 'XP Project'
    meta_type = 'PPMProject'
    icon = 'XPProject_icon.gif'

tests.append(TestPPMProject)

class TestPPMMetadata(ATCTTypeTestCase):

    klass = PPMMetadata
    portal_type = 'PPMMetadata'
    title = 'XP Metadata'
    meta_type = 'PPMMetadata'
    icon = 'xppm_metadata_icon.gif'

tests.append(TestPPMMetadata)

class TestPPMIteration(ATCTTypeTestCase):

    klass = PPMIteration
    portal_type = 'PPMIteration'
    title = 'XP Iteration'
    meta_type = 'PPMIteration'
    icon = 'xppm_iteration_icon.gif'

tests.append(TestPPMIteration)

class TestPPMFuncSpec(TestSiteATFolder):

    klass = PPMFuncSpec
    portal_type = "PPMFuncSpec"
    title = 'XP Function Spec'
    meta_type = "PPMFuncSpec"
    icon = 'xppm_fsd_icon.gif'

tests.append(TestPPMFuncSpec)

class TestPPMFuncReq(ATCTTypeTestCase):

    klass = PPMFuncReq
    portal_type = "PPMFuncReq"
    title = 'XP Function Requirement'
    meta_type = "PPMFuncReq"
    icon = 'xppm_fr_icon.gif'

tests.append(TestPPMFuncReq)

class TestPPMSysReq(ATCTTypeTestCase):

    klass = PPMSysReq
    portal_type = "PPMSysReq"
    title = 'XP System Requirement'
    meta_type = "PPMSysReq"
    icon = 'xppm_sr_icon.gif'

tests.append(TestPPMSysReq)

class TestPPMUseCase(ATCTTypeTestCase):

    klass = PPMUseCase
    portal_type = "PPMUseCase"
    title = 'XP Use Case'
    meta_type = "PPMUseCase"
    icon = 'xppm_usecase_icon.gif'

tests.append(TestPPMUseCase)

class TestPPMStory(TestSiteATFolder):

    klass = PPMStory
    portal_type = "PPMStory"
    title = 'XP Story'
    meta_type = "PPMStory"
    icon = 'xppm_story_icon.gif'

tests.append(TestPPMStory)

class TestPPMArtifact(TestSiteATFolder):

    klass = PPMArtifact
    portal_type = 'PPMArtifact'
    title = 'XP Artifact'
    meta_type = 'PPMArtifact'
    icon = 'xppm_artifact_icon.gif'

    # test create response.
    def testCreateResponse(self):

        response = self._createType(self._ATCT, 'PPMResponse', 'resp')
        #print 'The response: %s' % response

tests.append(TestPPMArtifact)

class TestPPMResponse(ATCTTypeTestCase):

    klass = PPMResponse
    portal_type = 'PPMResponse'
    title = 'XP Response'
    meta_type = 'PPMResponse'
    icon = 'xppm_response_icon.gif'

tests.append(TestPPMResponse)

# making test suite.
def test_suite():
    """This sets up a test suite that actually runs the tests in the class
    above
    """
    suite = unittest.TestSuite()
    for test in tests:
        suite.addTest(unittest.makeSuite(test))

    return suite
