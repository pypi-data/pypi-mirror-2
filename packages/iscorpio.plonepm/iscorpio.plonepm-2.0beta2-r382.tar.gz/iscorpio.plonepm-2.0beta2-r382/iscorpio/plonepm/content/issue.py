# issue.py

__doc__ = """XPointMemo records issue for a XPoint Project."""
__author__ = 'iScorpio <iscorpio@users.sourceforge.net>'
__docformat__ = 'plaintext'

import logging

from AccessControl import ClassSecurityInfo
# from Archetypes
from Products.Archetypes.public import DisplayList
from Products.Archetypes.public import registerType

from iscorpio.plonepm.content.xpointdoc import XPointDocument
# the configruation info for this project.
from iscorpio.plonepm.config import PROJECTNAME

# the XPointIssue schema.
XPointIssueSchema = XPointDocument.schema.copy()

# make description invisible.
XPointIssueSchema['description'].widget.visible = False
# make document status visible.
XPointIssueSchema['xpproject_document_status'].required = True
XPointIssueSchema['xpproject_document_status'].widget.visible = True
XPointIssueSchema['xpproject_document_status'].widget.label = \
    "Issue Status"
XPointIssueSchema['xpproject_document_status'].widget.description = \
    "Status for this issue."

# the class.
class XPointIssue(XPointDocument):
    """ XPointIssue records a issue for a XPoint Project.
    """

    schema = XPointIssueSchema

    # type and name
    meta_type = 'XPointIssue'
    portal_type = 'XPointIssue'
    archetype_name = "XP Issue"

    _at_rename_after_creation = True

    security = ClassSecurityInfo()

    def vocabulary_documentStatus(self):
        """ return a list of tuple (status, status desc) for the
        document status select.
        """
        return DisplayList([('open', 'Open'),
                            ('pending', 'Pending'),
                            ('close', 'Close'),
                            ]
                           )

# register this type to plone add-on product.
registerType(XPointIssue, PROJECTNAME)
