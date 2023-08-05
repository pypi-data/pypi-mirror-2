
# recentArtifacts.py

"""
a small portlets to show the recent changes artifacts: stories, responses,
iterations, etc.
"""

from zope.interface import implements
from Acquisition import aq_inner

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from plone.app.portlets.portlets import base

from interfaces import IRecentArtifactsPortlet

__author__ = "Sean Chen"
__email__ = "sean.chen@leocorn.com"

# the assignment class.
class Assignment(base.Assignment):
    """
    The assignment for this portlet.
    """

    implements(IRecentArtifactsPortlet)

    # init.
    def __init__(self):
        pass

    # title for this portlet,
    @property
    def title(self):

        return "Recent Artifacts Update"

# the renderering class.
class Renderer(base.Renderer):
    """
    returns the HTML for the portlet.
    """

    _template = ViewPageTemplateFile('recentArtifacts.pt')

    def __init__(self, *args):

        base.Renderer.__init__(self, *args)

        # we need the project root to get update for all artifacts.
        try:
            self.project = aq_inner(self.context).getProjectRoot()
        except AttributeError:
            # not a project context, set to None.
            self.project = None

    # Here we returns the HTML for this portlet.
    def render(self):

        return self._template()

    @property
    def available(self):
        """
        only available for a project context.
        """

        if not self.project:
            return False
        else:
            return True

    def artifacts(self):
        """
        returns the recent changed items.
        """

        infos = []
        # TODO: make this configurable!
        types = ['PPMIteration', 'PPMStory', 'PPMFuncReq',
                 'PPMSysReq', 'PPMUseCase']
        # TODO: the limit should be configuarable too!
        artifacts = self.project.xpCatalogSearch(portal_type=types,
                                                 sort_on='modified',
                                                 sort_order='reverse',
                                                 sort_limit=5)
        for artifact in artifacts:
            obj = artifact.getObject()
            infos.append({
                'url' : obj.absolute_url(),
                'modified' : obj.modified(),
                'title' : obj.title or obj.id,
                'obj' : obj,
                })

        return infos

# the add form.
class AddForm(base.NullAddForm):

    def create(self):

        return Assignment()
