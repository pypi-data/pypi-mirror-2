
# project.py

"""
view adapter for project view.
"""

from Acquisition import aq_inner
from Products.Five.browser import BrowserView

__author__ = "Sean Chen"
__email__ = "chyxiang@gmail.com"

# the default project View
class ProjectView(BrowserView):
    """
    the default view for a project.
    """

    # we need adapt Request too.
    def __init__(self, context, request):

        self.context = context
        self.request = request
        self.project = aq_inner(self.context)

    # return all metata data definition as a dict
    def getMetadata(self):

        return self.project.getMetadata()

    # returns the whole estimated hour for this project.
    def getProjectEstimatedHours(self):
        """
        returns the amount of hours estimated for this project.
        """

        stories = self.project.getAllStories()
        hours = 0
        for story in stories:
            hours = hours + \
                    story.getObject().xppm_story_estimated_hours

        return hours

    # progress percent
    def getProjectProgressPercent(self):
        """
        returns the progress status as a percentage for this project. 
        """

        stories = self.project.getAllStories()
        progressPercent = 0
        if len(stories) > 0:
            progress = 0
            for story in stories:
                progress = progress + \
                           story.getObject().xppm_story_progress_percent

            progressPercent = progress / len(stories)

        return progressPercent

class IterationsView(BrowserView):
    """
    A list of all iterations for this project.
    """

    # preparing the iteration plan data for this view.
    def getIterationData(self):
        """
        returns a list of interation data for the view.
        """

        context = aq_inner(self.context)
        iterations = context.getAllIterations()
        iterData = []
        for iteration in iterations:
            anIter = {}
            anIter['title'] = iteration.title or iteration.id
            anIter['url'] = iteration.absolute_url()
            anIter['icon'] = iteration.getIcon()
            anIter['date'] = iteration.getXppm_completion_date()
            # stories for this iteration
            stories = iteration.getIterationStories()
            hours = 0
            used = 0
            progress = 0
            for story in stories:
                # estimated hours.
                hours = hours + \
                        story.getObject().xppm_story_estimated_hours
                used = used + \
                       story.getObject().xppm_story_used_hours
                progress = progress + \
                           story.getObject().xppm_story_progress_percent

            anIter['estimatedHours'] = hours
            anIter['usedHours'] = used
            if len(stories) > 0:
                anIter['progressPercent'] = progress / len(stories)
            else:
                anIter['progressPercent'] = 0

            iterData.append(anIter)

        return iterData

class StorysView(BrowserView):
    """
    a list of all stories for this project.
    """

    # preparing the stories info for this view.
    def getStoryInfos(self):
        """
        return a list of story's info.
        """

        context = aq_inner(self.context)
        stories = context.getAllStories()
        storyInfos = []

        for story in stories:

            aStory = {}

            storyInfos.append(aStory)

        return storyInfos
