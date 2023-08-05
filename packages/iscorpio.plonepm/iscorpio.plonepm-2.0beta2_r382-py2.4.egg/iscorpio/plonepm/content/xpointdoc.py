# xpointdoc.py

__doc__ = """XPointDocument is the super class of PlonePM general
documents, such as memo, buildjounal, proposal, and issue."""
__author__ = 'iScorpio <iscorpio@users.sourceforge.net>'
__docformat__ = 'plaintext'

from AccessControl import ClassSecurityInfo
# Import modules and functions, etc. used in the following codes. 
from Products.Archetypes.public import Schema
from Products.Archetypes.public import DisplayList
from Products.Archetypes.public import TextField
from Products.Archetypes.public import RichWidget
from Products.Archetypes.public import StringField
from Products.Archetypes.public import SelectionWidget
from Products.Archetypes.public import DisplayList

from Products.ATContentTypes.interfaces import IATDocument
from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from Products.ATContentTypes.content.base import ATCTContent
from Products.ATContentTypes.lib.historyaware import HistoryAwareMixin
from Products.ATContentTypes.configuration import zconf

from Products.CMFCore.permissions import View

# the XPointDocument Schema.
XPointDocumentSchema = ATCTContent.schema.copy() + Schema((

        # The body of the build journal.
        TextField(
            'xpproject_text',
            searchable = True,
            required = True,
            default_output_type = 'text/x-html-safe',
            widget = RichWidget(
                label = u'Body Text',
                rows = 22
                ),
            ),

        # the status for this issue.
        StringField(
            'xpproject_document_status',
            searchable = False,
            required = False,
            index = "FieldIndex:schema",
            default = '',
            vocabulary = 'vocabulary_documentStatus',
            widget = SelectionWidget(
                label = 'Document Status',
                descrpiton = 'Set status for this issue.',
                format = 'select',
                ),
            ),

        ),
    )

# Plone 3 will re-organize all fields' shemata by using this method.
finalizeATCTSchema(XPointDocumentSchema)

# xpproject document status is invisible by default.
XPointDocumentSchema['xpproject_document_status'].widget.visible = False

# move the related items to the default shemata.
XPointDocumentSchema['relatedItems'].widget.visible = True
XPointDocumentSchema['relatedItems'].widget.description = \
    "Select related items"
XPointDocumentSchema['relatedItems'].schemata = 'default'
XPointDocumentSchema.moveField('relatedItems', pos='bottom')

# the XPointDocument class.
class XPointDocument(ATCTContent, HistoryAwareMixin):

    schema = XPointDocumentSchema

    # type, name, icon should be set by sub class.

    __implements__ = (ATCTContent.__implements__,
                      IATDocument,
                      HistoryAwareMixin.__implements__,
                     )

    _at_rename_after_creation = True

    security = ClassSecurityInfo()

    security.declareProtected(View, 'CookedBody')
    def CookedBody(self, stx_level = 'ignored'):
        """CMF compatibility method
        """
        return self.getXpproject_text()

    def initializeArchetype(self, **kwargs):
        ATCTContent.initializeArchetype(self, **kwargs)

    # the default vocabulary.
    def vocabulary_documentStatus(self):
        """ return a list of tuple (status, status desc) for the
        document status select.
        """
        return DisplayList([('open', 'Open'),
                            ('close', 'Close'),
                            ]
                           )
