
# projectSimpleNav.py

"""
a portlet to provide simple navigation for a project.

list each iteration, all stories, all function requirments, etc.
"""

from zope.interface import implements
from Acquisition import aq_inner

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from plone.app.portlets.portlets import base

from interfaces import IProjectSimpleNavPortlet

__author__ = "Sean Chen"
__email__ = "sean.chen@leocorn.com"

class Assignment(base.Assignment):
    """
    persistent data for this portlet.  Let's keep it simple now.
    """

    # mark this as a portlet data provider.
    implements(IProjectSimpleNavPortlet)

    def __init__(self):
        pass

    @property
    def title(self):

        return "Project Navigation"

# renderering the portlet on page.
class Renderer(base.Renderer):
    """
    returns the HTML for the portlet on page.
    """

    _template = ViewPageTemplateFile('projectSimpleNav.pt')

    def __init__(self, *args):

        base.Renderer.__init__(self, *args)
        try:
            self.project = aq_inner(self.context).getProjectRoot()
        except AttributeError:
            self.project = None

    def render(self):

        return self._template()

    @property
    def available(self):
        """
        The condition to show this portlet. This portlet will only
        show up within a project context.  It will also show up for all
        contents of a project.
        """
        if not self.project:
            return False
        else:
            return True

    def projectInfo(self):

        return {'url' : self.project.absolute_url(),
                'title' : self.project.title or self.project.id}

    def iterations(self):
        """
        returns the latest active 5 iterations.
        """

        infos = []
        iterations = self.project.xpCatalogSearch(portal_type='PPMIteration',
                                                  sort_on='modified',
                                                  sort_order='reverse',
                                                  sort_limit=5)
        for iteration in iterations:
            obj = iteration.getObject()
            infos.append({
                'url' : obj.absolute_url(),
                'title' : obj.title or obj.id,
                'icon' : obj.getIcon(),
                })

        return infos

    def stories(self):
        """
        returns the last 5 recent changed stories.
        """

        values = []
        stories = self.project.xpCatalogSearch(portal_type='PPMStory',
                                               sort_on='modified',
                                               sort_order='reverse',
                                               sort_limit=5)
        for story in stories:
            obj = story.getObject()
            #import pdb; pdb.set_trace()
            values.append({
                'url' : obj.absolute_url(),
                'title' : obj.title or obj.id,
                'icon' : obj.getIcon(),
                })

        return values

# the form for add this portlet.
class AddForm(base.NullAddForm):

    def create(self):

        return Assignment()
