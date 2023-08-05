
# base.py

__doc__ = """ this package will contain the base classes for xpoint project management."""
__docformat__ = 'plaintext'

import logging
import transaction

from AccessControl import ClassSecurityInfo

from Products.Archetypes.public import Schema
from Products.Archetypes.public import TextField
from Products.Archetypes.public import RichWidget
from Products.Archetypes.public import StringField
from Products.Archetypes.public import SelectionWidget
from Products.Archetypes.public import DisplayList

from Products.ATContentTypes.interfaces import IATDocument
from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from Products.ATContentTypes.content.base import ATCTContent
from Products.ATContentTypes.lib.historyaware import HistoryAwareMixin

from Products.CMFCore.permissions import View

__author__ = 'Sean Chen'
__email__ = 'chyxiang@gmail.com'

# the base class
class XPPMBase:
    """ the base class for XPoint Project Management content type.
    """

    # The prefix for auto generated object id.  Each content can give it's
    # own prefix.
    xppm_id_prefix = "xppm"

    log = logging.getLogger("PlonePM XPPMBase")

    # override renameAfterCreation to generate the unique id for
    # contact. This method is defined in Archetypes.BaseObject.py.
    # The method getNextUniqueId should be defined in the root content of
    # XPoint Project Management.
    def _renameAfterCreation(self, check_auto_id=False):

        # Can't rename without a subtransaction commit when using
        # portal_factory!
        transaction.savepoint(optimistic=True)
        newId = str(self.getNextUniqueId())
        self.log.info('the next value for xppm sequence: %s',
                      newId)
        self.setId(self.xppm_id_prefix + newId)

# the base class for all document base content in XPoint Project Management
XPPMDocBaseSchema = ATCTContent.schema.copy() + Schema((

        # the details description for a use case.
        TextField(
            'xppm_text',
            searchable = True,
            required = True,
            default_output_type = 'text/x-html-safe',
            widget = RichWidget(
                label = u'Text Area Label',
                description = u'The details description Here.',
                rows = 25,
                ),
            ),

        # the status for this issue.
        StringField(
            'xppm_status',
            searchable = False,
            required = False,
            default = '',
            # this the default vocabulary, we can change for each one.
            vocabulary = 'vocabulary_status',
            widget = SelectionWidget(
                label = 'Document Status',
                descrpiton = 'Set status for this issue.',
                format = 'select',
                ),
            ),

        ),
    )

# finalize here ?
finalizeATCTSchema(XPPMDocBaseSchema)

class XPPMDocBase(ATCTContent, HistoryAwareMixin):

    schema = XPPMDocBaseSchema

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
        return self.getXppm_text()

    # the default vocabulary.
    def vocabulary_status(self):
        """ return a list of tuple (status, status desc) for the
        document status select.
        """
        return DisplayList([('open', 'Open'),
                            ('close', 'Close'),
                            ]
                           )
