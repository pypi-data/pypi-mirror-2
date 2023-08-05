
# interfaces.py

"""
defines the marker interfaces for portlets.  All portlet should implement
interface IPortletDataProvider.
"""

from plone.portlets.interfaces import IPortletDataProvider

__author__ = "Sean Chen"
__email__ = "sean.chen@leocorn.com"

# the overview portlet for a project.
class IProjectOverviewPortlet(IPortletDataProvider):
    """
    The marker interface for project overview portlet.
    """

# This portlet is trying to provide a simple navigation for a project.
class IProjectSimpleNavPortlet(IPortletDataProvider):
    """
    The marker interface for project simple navigation portlet.
    """

# a portlet to list recent updates for this project.
class IRecentArtifactsPortlet(IPortletDataProvider):
    """
    the marker interface for a portlet to list recent changed artifacts.
    """

# a portlet to show summary about a story.
class IStoryFactsPortlet(IPortletDataProvider):
    """
    The marker interface for the story facts portlet.
    """
