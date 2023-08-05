
# testStoryPortlets.py

"""
testing the portlets for PPMStory
"""

import unittest

from iscorpio.plonepm.portlets import storyFacts

from base import PlonepmPortletTestCase

__author__ = "Sean Chen"
__email__ = "sean.chen@leocorn.com"

class TestStoryPortlets(PlonepmPortletTestCase):

    def testRenderer(self):

        renderer = self.renderer(context=self.folder,
                                 assignment=storyFacts.Assignment())
        self.failIf(renderer.available)
        self.failUnless(isinstance(renderer, storyFacts.Renderer))

class TestStoryFactsRenderer(PlonepmPortletTestCase):

    def testAvailable(self):

        # renderer in root should not available
        renderer = self.renderer(assignment=storyFacts.Assignment())
        self.failIf(renderer.available)

        # renderer in a project
        self.portal.invokeFactory('PPMProject', 'project1')
        project = getattr(self.portal, 'project1')
        renderer = self.renderer(context=project,
                                 assignment=storyFacts.Assignment())
        self.failIf(renderer.available)

        # renderer in a metadata
        project.invokeFactory('PPMMetadata', 'meta1')
        metadata = getattr(project, 'meta1')
        renderer = self.renderer(context=metadata,
                                 assignment=storyFacts.Assignment())
        self.failIf(renderer.available)

        # renderer in a story
        project.invokeFactory('PPMStory', 'story1')
        story1 = getattr(project, 'story1')
        renderer = self.renderer(context=story1,
                                 assignment=storyFacts.Assignment())
        self.failUnless(renderer.available)

        # renderer in a story response

    def testStoryInfo(self):

        self.portal.invokeFactory('PPMProject', 'project1')
        project1 = getattr(self.portal, 'project1')

        project1.invokeFactory('PPMIteration', 'iter1', title='Iteration Title')
        iter1 = getattr(project1, 'iter1')

        project1.invokeFactory('PPMStory', 'story1', title="Story Title")
        story1 = getattr(project1, 'story1')
        story1.xppm_iteration = 'iter1'
        renderer = self.renderer(context=story1,
                                 assignment=storyFacts.Assignment())
        info = renderer.storyInfo()
        self.assertEquals(info['url'], story1.absolute_url())
        self.assertEquals(info['title'], 'Story Title')
        self.assertEquals(info['iterationTitle'], 'Iteration Title')
        self.assertEquals(info['iterationUrl'], iter1.absolute_url())
        self.assertEquals(info['iterationIcon'], iter1.getIcon())

    def testColleagueStories(self):

        # we don't need this, the profile will be imported when we install
        # the product.
        #setup_tool = getattr(self.portal, 'portal_setup')
        #setup_tool.runAllImportStepsFromProfile('profile-%s' % \
        #                                        'iscorpio.plonepm:default')

        self.portal.invokeFactory('PPMProject', 'project1')
        project1 = getattr(self.portal, 'project1')

        project1.invokeFactory('PPMIteration', 'iter1', title='Iteration Title')
        iter1 = getattr(project1, 'iter1')

        project1.invokeFactory('PPMStory', 'story1')
        story1 = getattr(project1, 'story1')
        story1.xppm_iteration = 'iter1'
        # re-index the object is required! since this is not a default index
        # field.
        self.portal.portal_catalog.indexObject(story1)

        project1.invokeFactory('PPMStory', 'story2')
        story2 = getattr(project1, 'story2')
        story2.xppm_iteration = 'iter1'
        self.portal.portal_catalog.indexObject(story2)

        project1.invokeFactory('PPMStory', 'story3')
        story3 = getattr(project1, 'story3')
        story3.xppm_iteration = 'iter1'
        self.portal.portal_catalog.indexObject(story3)

        renderer = self.renderer(context=story2,
                                 assignment=storyFacts.Assignment())
        stories = renderer.colleagueStories()
        self.assertEquals(len(stories), 3)
        self.assertEquals(stories[0]['url'], story1.absolute_url())
        self.assertEquals(stories[1]['title'], story2.id)
        self.assertEquals(stories[2]['url'], story3.absolute_url())

def test_suite():

    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestStoryPortlets))
    suite.addTest(unittest.makeSuite(TestStoryFactsRenderer))

    return suite
