
# PPMResponse.py

__doc__ = """PPMResponse defines a """
__docformat__ = 'plaintext'

import logging

from zope.interface import implements

from AccessControl import ClassSecurityInfo
# from Archetypes
from Products.Archetypes.public import Schema
from Products.Archetypes.public import StringField
from Products.Archetypes.public import StringWidget
from Products.Archetypes.public import SelectionWidget
from Products.Archetypes.public import TextAreaWidget
from Products.Archetypes.public import DisplayList
from Products.Archetypes.public import registerType
# from ATContentTypes
from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from Products.ATContentTypes.content.base import ATCTContent
from Products.ATContentTypes.lib.historyaware import HistoryAwareMixin

# the configruation info for this project.
from iscorpio.plonepm.config import PROJECTNAME
from iscorpio.plonepm.content.base import XPPMBase
from iscorpio.plonepm.interfaces import IPPMMetadata

__author__ = 'Sean Chen'
__email__ = 'sean.chen@leocorn.com'

# define the schema for the metadata.
PPMMetadataSchema = ATCTContent.schema.copy() + Schema((

        # the type of this metadata.
        StringField(
            'xppm_metadata_type',
            vocabulary = 'vocabulary_metadataTypes',
            widget = SelectionWidget(
                label = 'Metadata Type',
                description = 'Set up the type for your metadata',
                format = 'select',
                ),
            ),
        )
    )

finalizeATCTSchema(PPMMetadataSchema)

class PPMMetadata(XPPMBase, ATCTContent, HistoryAwareMixin):
    """
    a metadata for PPM Project.
    """

    schema = PPMMetadataSchema

    meta_type = "PPMMetadata"
    portal_type = "PPMMetadata"
    archetypes_type = "PPMMetadata"

    __implements__ = (ATCTContent.__implements__,
                      HistoryAwareMixin.__implements__,
                      )
    implements(IPPMMetadata)

    # the prefix for the auto generated ids.
    xppm_id_prefix = 'xpm'
    # log.
    log = logging.getLogger("PlonePM PPMMetadata")

    security = ClassSecurityInfo()

    def vocabulary_metadataTypes(self):
        """ return all metadata types as a vocabulary.
        """

        return DisplayList([('priority', 'Artifact Priority'),
                            ('category', 'Artifact Category'),
                            ('status', 'Artifact Status'),
                            ('tag', 'Artifact Tag'),
                            ])

# register to the plone add-on product.
registerType(PPMMetadata, PROJECTNAME)
