
# testProjectPortlets.py

"""
Unit testing the portlets binding to PPMProject.
"""

import unittest

from iscorpio.plonepm.portlets import projectOverview
from iscorpio.plonepm.portlets import projectSimpleNav
from iscorpio.plonepm.portlets import recentArtifacts

from base import PlonepmPortletTestCase

__author__ = "Sean Chen"
__email__ = "sean.chen@leocorn.com"

class TestProjectPortlets(PlonepmPortletTestCase):

    def testRenderer(self):

        renderer = self.renderer(context=self.folder,
                                 assignment=projectSimpleNav.Assignment())
        self.failIf(renderer.available)
        self.failUnless(isinstance(renderer, projectSimpleNav.Renderer))

        renderer = self.renderer(context=self.folder,
                                 assignment=recentArtifacts.Assignment())
        self.failIf(renderer.available)
        self.failUnless(isinstance(renderer, recentArtifacts.Renderer))

        renderer = self.renderer(context=self.folder,
                                 assignment=projectOverview.Assignment())
        self.failIf(renderer.available)
        self.failUnless(isinstance(renderer, projectOverview.Renderer))

class TestProjectOverviewRenderer(PlonepmPortletTestCase):

    def testAvailable(self):

        # renderer in root should not available
        renderer = self.renderer(assignment=projectOverview.Assignment())
        self.failIf(renderer.available)

        # renderer in a project
        self.portal.invokeFactory('PPMProject', 'project1')
        project = getattr(self.portal, 'project1')
        renderer = self.renderer(context=project,
                                 assignment=projectOverview.Assignment())
        self.failUnless(renderer.available)

        # renderer in a metadata
        project.invokeFactory('PPMMetadata', 'meta1')
        metadata = getattr(project, 'meta1')
        renderer = self.renderer(context=metadata,
                                 assignment=projectOverview.Assignment())
        self.failUnless(renderer.available)

    def testProjectInfo(self):

        repoUrl = 'http://svn.example.com'
        browseUrl = "http://trac.example.com"

        # get project info on a project context.
        self.portal.invokeFactory('PPMProject', 'project1')
        project = getattr(self.portal, 'project1')
        project.xppm_repo_url = repoUrl
        project.xppm_browse_code_url = browseUrl

        renderer = self.renderer(context=project,
                                 assignment=projectOverview.Assignment())
        info = renderer.projectInfo()
        self.assertEquals(info['url'], project.absolute_url())
        self.assertEquals(info['title'], 'project1')
        self.assertEquals(info['svnUrl'], repoUrl)
        self.assertEquals(info['viewUrl'], browseUrl)

        # get project info on a metadata context
        project.invokeFactory('PPMMetadata', 'meta1')
        metadata = getattr(project, 'meta1')
        renderer = self.renderer(context=metadata,
                                 assignment=projectOverview.Assignment())
        info = renderer.projectInfo()
        self.assertEquals(info['url'], project.absolute_url())
        self.assertEquals(info['title'], 'project1')
        self.assertEquals(info['svnUrl'], repoUrl)
        self.assertEquals(info['viewUrl'], browseUrl)

class TestProjectSimpleNavRenderer(PlonepmPortletTestCase):

    def testAvailable(self):

        # renderer in root should not available
        renderer = self.renderer(assignment=projectSimpleNav.Assignment())
        self.failIf(renderer.available)

        # renderer in a project
        self.portal.invokeFactory('PPMProject', 'project1')
        project = getattr(self.portal, 'project1')
        renderer = self.renderer(context=project,
                                 assignment=projectSimpleNav.Assignment())
        self.failUnless(renderer.available)

        # renderer in a metadata
        project.invokeFactory('PPMMetadata', 'meta1')
        metadata = getattr(project, 'meta1')
        renderer = self.renderer(context=metadata,
                                 assignment=projectSimpleNav.Assignment())
        self.failUnless(renderer.available)

    def testProjectInfo(self):

        # get project info on a project context.
        self.portal.invokeFactory('PPMProject', 'project1')
        project = getattr(self.portal, 'project1')
        renderer = self.renderer(context=project,
                                 assignment=projectSimpleNav.Assignment())
        info = renderer.projectInfo()
        self.assertEquals(info['url'], project.absolute_url())
        self.assertEquals(info['title'], 'project1')

        # get project info on a metadata context
        project.invokeFactory('PPMMetadata', 'meta1')
        metadata = getattr(project, 'meta1')
        renderer = self.renderer(context=metadata,
                                 assignment=projectSimpleNav.Assignment())
        info = renderer.projectInfo()
        self.assertEquals(info['url'], project.absolute_url())
        self.assertEquals(info['title'], 'project1')

    def testInterationsInfo(self):

        # preparing the dummy data.
        self.portal.invokeFactory('PPMProject', 'project1')
        project = getattr(self.portal, 'project1')
        project.invokeFactory('PPMMetadata', 'meta1')
        metadata = getattr(project, 'meta1')
        # preparing iteration.
        project.invokeFactory('PPMIteration', 'iter1')
        iteration1 = getattr(project, 'iter1')
        project.invokeFactory('PPMIteration', 'iter2')
        iteration2 = getattr(project, 'iter2')

        renderer = self.renderer(context=project,
                                 assignment=projectSimpleNav.Assignment())
        iterations = renderer.iterations()
        self.assertEquals(len(iterations), 2)
        self.assertEquals(iterations[0]['url'], iteration2.absolute_url())
        self.assertEquals(iterations[0]['title'], 'iter2')
        self.assertEquals(iterations[1]['url'], iteration1.absolute_url())
        self.assertEquals(iterations[1]['title'], 'iter1')

        renderer = self.renderer(context=metadata,
                                 assignment=projectSimpleNav.Assignment())
        iterations = renderer.iterations()
        self.assertEquals(len(iterations), 2)
        self.assertEquals(iterations[0]['url'], iteration2.absolute_url())
        self.assertEquals(iterations[0]['title'], 'iter2')
        self.assertEquals(iterations[1]['url'], iteration1.absolute_url())
        self.assertEquals(iterations[1]['title'], 'iter1')

    def testStoriesInfo(self):

        # preparing the dummy data.
        self.portal.invokeFactory('PPMProject', 'project1')
        project = getattr(self.portal, 'project1')
        project.invokeFactory('PPMMetadata', 'meta1')
        metadata = getattr(project, 'meta1')
        # preparing stories
        project.invokeFactory('PPMStory', 'story1')
        story1 = getattr(project, 'story1')
        #self.portal.portal_catalog.indexObject(story1)
        project.invokeFactory('PPMStory', 'story2')
        story2 = getattr(project, 'story2')
        #self.portal.portal_catalog.indexObject(story2)
        project.invokeFactory('PPMStory', 'story3')
        story3 = getattr(project, 'story3')
        #self.portal.portal_catalog.indexObject(story3)

        renderer = self.renderer(context=project,
                                 assignment=projectSimpleNav.Assignment())
        stories = renderer.stories()
        self.assertEquals(len(stories), 3)
        self.assertEquals(stories[0]['url'], story3.absolute_url())
        self.assertEquals(stories[0]['title'], 'story3')
        self.assertEquals(stories[1]['url'], story2.absolute_url())
        self.assertEquals(stories[1]['title'], 'story2')
        self.assertEquals(stories[2]['url'], story1.absolute_url())
        self.assertEquals(stories[2]['title'], 'story1')

class TestRecentArtifactsRenderer(PlonepmPortletTestCase):

    def testAvailable(self):

        # renderer in root should not available
        renderer = self.renderer(assignment=recentArtifacts.Assignment())
        self.failIf(renderer.available)

        # renderer in a project
        self.portal.invokeFactory('PPMProject', 'project1')
        project = getattr(self.portal, 'project1')
        renderer = self.renderer(context=project,
                                 assignment=recentArtifacts.Assignment())
        self.failUnless(renderer.available)

        # renderer in a metadata
        project.invokeFactory('PPMMetadata', 'meta1')
        metadata = getattr(project, 'meta1')
        renderer = self.renderer(context=metadata,
                                 assignment=recentArtifacts.Assignment())
        self.failUnless(renderer.available)

    def testArtifacts(self):

        self.portal.invokeFactory('PPMProject', 'project1')
        project = getattr(self.portal, 'project1')
        project.invokeFactory('PPMStory', 'story1')
        story1 = getattr(project, 'story1')
        project.invokeFactory('PPMFuncReq', 'funcReq1')
        funcReq1 = getattr(project, 'funcReq1')
        project.invokeFactory('PPMIteration', 'iter1')
        iter1 = getattr(project, 'iter1')
        project.invokeFactory('PPMSysReq', 'sysReq1')
        sysReq1 = getattr(project, 'sysReq1')

        renderer = self.renderer(context=project,
                                 assignment=recentArtifacts.Assignment())
        artifacts = renderer.artifacts()
        self.assertEquals(len(artifacts), 4)
        self.assertEquals(artifacts[0]['url'], sysReq1.absolute_url())
        self.assertEquals(artifacts[0]['title'], 'sysReq1')
        self.assertEquals(artifacts[2]['url'], funcReq1.absolute_url())
        self.assertEquals(artifacts[2]['title'], 'funcReq1')

        renderer = self.renderer(context=story1,
                                 assignment=recentArtifacts.Assignment())
        artifacts = renderer.artifacts()
        self.assertEquals(len(artifacts), 4)
        self.assertEquals(artifacts[1]['url'], iter1.absolute_url())
        self.assertEquals(artifacts[1]['title'], 'iter1')
        self.assertEquals(artifacts[3]['url'], story1.absolute_url())
        self.assertEquals(artifacts[3]['title'], 'story1')

def test_suite():

    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestProjectPortlets))
    suite.addTest(unittest.makeSuite(TestProjectOverviewRenderer))
    suite.addTest(unittest.makeSuite(TestProjectSimpleNavRenderer))
    suite.addTest(unittest.makeSuite(TestRecentArtifactsRenderer))

    return suite
