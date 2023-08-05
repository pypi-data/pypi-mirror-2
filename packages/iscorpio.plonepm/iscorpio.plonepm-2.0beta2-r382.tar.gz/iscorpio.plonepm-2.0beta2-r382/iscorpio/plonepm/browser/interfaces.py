
# interfaces.py

"""
Define interfaces for browser views.
"""

from zope.interface import Interface
from zope.schema import Text
from zope.schema import Float
from zope.schema import Datetime
from zope.schema import Choice
from zope.viewlet.interfaces import IViewletManager

__author__ = "Sean Chen"
__email__ = "sean.chen@leocorn.com"

class IPlonepmTimesheet(IViewletManager):
    """
    Marker interface for the PlonePM timesheet viewlet manager
    """

# the interface and schema for timesheet fill out form.
class ITimesheetForm(Interface):

    when = Datetime(title=u'When', required=True,
                    description=u'Please specify when the work is done',
                    readonly=False)

    who = Choice(title=u'Who', required=False,
                 description=u'Please select who did the work, default is current user',
                 values=['abc', 'cde'],
                 readonly=False)

    description = Text(title=u'Work Description', required=True,
                       description=u'Please provide brief description about what bas been done.',
                       readonly=False)

    duration = Float(title=u'Duration (Hours)', required=True,
                     description=u'Please specify how much time you spent on this work.',
                     readonly=False)

    percentage = Float(title=u'Story Finish Percentage', required=False,
                       description=u'Please specify the finish percentage for this story.',
                       readonly=False)
