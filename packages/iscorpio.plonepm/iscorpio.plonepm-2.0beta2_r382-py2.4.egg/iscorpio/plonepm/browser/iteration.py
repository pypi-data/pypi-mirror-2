
# iteration.py

"""
browser views for project iteration.
"""

from Acquisition import aq_inner
from Products.Five.browser import BrowserView

__author__ = "Sean Chen"
__email__ = "chyxiang@gmail.com"

# the default view.
class IterationView(BrowserView):
    """
    the default view for an iteration.
    """

    def __init__(self, context, request):

        self.context = context
        self.request = request

    # returns the whole estimated hour for this iteration.
    def getIterationEstimatedHours(self):
        """
        returns the amount of hours estimated for this iteration.
        """

        context = aq_inner(self.context)
        stories = context.getIterationStories()
        hours = 0
        for story in stories:
            hours = hours + \
                    story.getObject().xppm_story_estimated_hours

        return hours

    # returns the whole estimated hour for this iteration.
    def getIterationUsedHours(self):
        """
        returns the amount of hours estimated for this iteration.
        """

        context = aq_inner(self.context)
        stories = context.getIterationStories()
        hours = 0
        for story in stories:
            hours = hours + \
                    story.getObject().xppm_story_used_hours

        return hours

    # progress percent
    def getIterationProgressPercent(self):
        """
        returns the progress status as a percentage for this iteration. 
        """

        context = aq_inner(self.context)
        stories = context.getIterationStories()
        progressPercent = 0
        if len(stories) > 0:
            progress = 0
            for story in stories:
                progress = progress + \
                           story.getObject().xppm_story_progress_percent

            progressPercent = progress / len(stories)

        return progressPercent
