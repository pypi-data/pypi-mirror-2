# proposal.py

__doc__ = """XPointMemo records proposal for a XPoint Project."""
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

# the XPointProposal schema.
XPointProposalSchema = XPointDocument.schema.copy()

# make description invisible.
XPointProposalSchema['description'].widget.visible = False
# make document status visible.
XPointProposalSchema['xpproject_document_status'].required = True
XPointProposalSchema['xpproject_document_status'].widget.visible = True
XPointProposalSchema['xpproject_document_status'].widget.label = \
    "Proposal Status"
XPointProposalSchema['xpproject_document_status'].widget.description = \
    "Status for this proposal."

# the class.
class XPointProposal(XPointDocument):
    """ XPointProposal records a proposal for a XPoint Project.
    """

    schema = XPointProposalSchema

    # type and name
    meta_type = 'XPointProposal'
    portal_type = 'XPointProposal'
    archetype_name = "XP Proposal"

    _at_rename_after_creation = True

    security = ClassSecurityInfo()

    def vocabulary_documentStatus(self):
        """ return a list of tuple (status, status desc) for the
        document status select.
        """
        return DisplayList([('draft', 'Draft'),
                            ('pending', 'Pending'),
                            ('accepted', 'Accepted'), 
                            ]
                           )

# register this type to plone add-on product.
registerType(XPointProposal, PROJECTNAME)
