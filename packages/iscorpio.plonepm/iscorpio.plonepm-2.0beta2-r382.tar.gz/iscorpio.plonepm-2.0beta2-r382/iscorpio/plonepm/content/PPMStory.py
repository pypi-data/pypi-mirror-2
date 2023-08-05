
# PPMStory.py

__doc__ = """PPMStory defines a story for a software project in Agile approach."""
__docformat__ = 'plaintext'

import logging
from time import time

from zope.interface import implements
from AccessControl import ClassSecurityInfo
# from Archetypes
from Products.Archetypes.public import Schema
from Products.Archetypes.public import TextField
from Products.Archetypes.public import TextAreaWidget
from Products.Archetypes.public import RichWidget
from Products.Archetypes.public import LinesField
from Products.Archetypes.public import InAndOutWidget
from Products.Archetypes.public import LinesWidget
from Products.Archetypes.public import DisplayList
from Products.Archetypes.public import IntDisplayList
from Products.Archetypes.public import SelectionWidget
from Products.Archetypes.public import DateTimeField
from Products.Archetypes.public import CalendarWidget
from Products.Archetypes.public import IntegerField
from Products.Archetypes.public import IntegerWidget
from Products.Archetypes.public import StringField
from Products.Archetypes.public import FloatField
from Products.Archetypes.public import registerType
# from ATContentTypes
from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from Products.ATContentTypes.atct import ATFolder
from Products.ATContentTypes.atct import ATFolderSchema
from Products.ATContentTypes.lib.historyaware import HistoryAwareMixin

from Products.CMFCore.permissions import ModifyPortalContent
from Products.CMFCore.utils import getToolByName

# the configruation info for this project.
from iscorpio.plonepm.config import PROJECTNAME
from iscorpio.plonepm.content.base import XPPMBase
from iscorpio.plonepm.interfaces import IPPMStory

__author__ = 'Sean Chen'
__email__ = 'sean.chen@leocorn.com'

# the schema for story.
PPMStorySchema = ATFolderSchema.copy() + Schema((

        # scope details
        TextField(
            'xppm_text',
            searchable = True,
            required = True,
            default_output_type = 'text/x-html-safe',
            widget = RichWidget(
                label = 'Details',
                description = 'Details description for this story',
                rows = 18,
                ),
            ),

        # iteration plan
        StringField(
            'xppm_iteration',
            searchable = False,
            required = True,
            vocabulary = 'vocabulary_iterations',
            widget = SelectionWidget(
                label = u'Iteration Plan',
                description = u'Select the iteration plan for this story',
                format = 'select',
                ),
            ),

        # use cases for this story.
        LinesField(
            'xppm_use_cases',
            searchable = False,
            required = False,
            vocabulary = 'vocabulary_useCases',
            widget = InAndOutWidget(
                label = 'Story Use Case(s)',
                descrpiton = "Please select use cases for this story",
                ),
            ),

        # planned completed date, 90% finish deadline
        DateTimeField(
            'xppm_completion_date',
            searchable = False,
            required = True,
            widget = CalendarWidget(
                label = '90% Completion Deadline',
                description = 'Specify the date when this task should be completed at less 90%',
                #starting_year = 2007,
                show_hm = False,
                ),
            schemata = 'Manage',
            ),

        # Progress Status in percentage. 0% - 100%
        FloatField(
            'xppm_story_progress_percent',
            searchable = False,
            required = False,
            default = 0.0,
            ),

        # estimated hours for this task.
        IntegerField(
            'xppm_story_estimated_hours',
            searchable = False,
            required = False,
            widget = IntegerWidget(
                label = 'Estimated Hours',
                descrpiton = 'Put here the estimated hours for this task',
                ),
            schemata = 'Manage',
            ),

        # used hours for this task.
        FloatField(
            'xppm_story_used_hours',
            searchable = False,
            required = False,
            default = 0.0,
            ),

        # owner of this task.??? select from membership.
        # getToolByName(self, 'portal_membership')
        LinesField(
            'xppm_story_owners',
            searchable = False,
            required = False,
            vocabulary = 'vocabulary_developers',
            widget = InAndOutWidget(
                label = 'Story Owner(s)',
                descrpiton = "Please select owners for this story",
                ),
            schemata = 'Manage',
            ),

        # depended stories list.
        LinesField(
            'xppm_story_dependencies',
            searchable = False,
            required = False,
            vocabulary = 'vocabulary_allStoriesList',
            widget = InAndOutWidget(
                label = 'Dependencies Stories',
                description = 'Please select dependencies stories',
                ),
            schemata = 'Manage',
            ),

        # system requirements list.
        LinesField(
            'xppm_story_sysreqs',
            searchable = False,
            required = False,
            vocabulary = 'vocabulary_allSysreqsList',
            widget = InAndOutWidget(
                label = 'System Requirements',
                description = 'Please select system requirements for your story',
                ),
            schemata = 'Manage',
            ),
        ),
    )

# finalize the schema.
finalizeATCTSchema(PPMStorySchema)

# set the description field invisible.
PPMStorySchema['description'].widget.visible = False
# time tracking will update the following fields.
PPMStorySchema['xppm_story_progress_percent'].widget.visible = False
PPMStorySchema['xppm_story_used_hours'].widget.visible = False

# the class.
class PPMStory(XPPMBase, ATFolder, HistoryAwareMixin):

    schema = PPMStorySchema

    meta_type = "PPMStory"
    portal_type = "PPMStory"
    archetypes_type = "PPMStory"

    __implements__ = (ATFolder.__implements__,
                      HistoryAwareMixin.__implements__,
                      )
    implements(IPPMStory)

    # set up the prefix for auto generated ids.
    xppm_id_prefix = 'xps'
    # the logger.
    log = logging.getLogger("PlonePM PPMStory")
    # preparing class security info for methods.
    security = ClassSecurityInfo()

    def getStoryRoot(self):
        """
        returns the story object itself.
        """

        return self

    security.declarePublic('vocabulary_allSysreqsList')
    def vocabulary_allSysreqsList(self):
        """ Returns a display list for all system requirement, the format is
        like [id, id + title]
        """

        ret = []
        for req in self.getAllSysReqs():
            ret.append((req.id, req.id + ' ' + req.Title))

        self.log.debug('we got %s system requirement', len(ret))
        return DisplayList(ret)

    #security.declareProtected('vocabulary_allMembersList')
    def vocabulary_developers(self):
        """ Return a list of tuple (user_id, fullname, email) for all
        the members of the portal.
        """
        members = []
        portalMembers = getToolByName(self, 'portal_membership')
        developers = self.getProjectDevelopers()
        for memberId in developers:
            members.append((memberId,
                            portalMembers.getMemberById(memberId).getProperty('fullname',
                                                                              memberId))
                           )

        return DisplayList(members)

    security.declareProtected(ModifyPortalContent, 'setXppm_story_owners')
    def setXppm_story_owners(self, owners):
        """
        mutator for field xppm_story_owners, set local role for new owners.
        """

        field = self.getField('xppm_story_owners')

        for owner in owners:
            if owner:
                self.manage_setLocalRoles(owner, ['Editor'])

        field.set(self, owners)

    security.declareProtected(ModifyPortalContent, 'logTimesheet')
    def logTimesheet(self, when, description, duration,
                     percentage=None, memberId=None):
        """
        logging the billable time as format:
        datetime, description, duration, percentage
        """

        if not memberId:
            # no member specified, using the current logged in user.
            memberId = self.getCurrentMember().getId()

        if not percentage:
            # using the current percentage.
            percentage = self.getXppm_story_progress_percent()

        # we split datetime to logtime and worktime: indicates the timestamp
        # for this log and timestamp for the work been done.  log time pretty
        # much for future usage.

        # TODO: migration script to convert the legacy data!

        # TODO: should initialize this in __init__
        try:
            self._changeLog
        except AttributeError:
            self._changeLog = []
        self._changeLog.append({'logtime' : time(),
                                'worktime' : when,
                                'memberId' : memberId,
                                'description' : description,
                                'duration' : duration,
                                'percentage' : percentage})

        # update context with new spent time and progress.
        self.setXppm_story_used_hours(self.xppm_story_used_hours + duration)
        self.setXppm_story_progress_percent(percentage)

    def getChangeLog(self):

        # TODO: should initialize this in __init__
        try:
            self._changeLog
        except AttributeError:
            try:
                self._changeLog = self._timesheet
            except AttributeError:
                self._changeLog = []

        return self._changeLog

# register to the plone add-on product.
registerType(PPMStory, PROJECTNAME)
