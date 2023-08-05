# buildjournal.py

__doc__ = """XPointBuildJournal Product for Plone to record build
journal."""
__author__ = 'iScorpio <iscorpio@users.sourceforge.net>'
__docformat__ = 'plaintext'

from AccessControl import ClassSecurityInfo
# Import modules and functions, etc. used in the following codes. 
from Products.Archetypes.public import registerType

from iscorpio.plonepm.content.xpointdoc import XPointDocument
# the configruation info for this project.
from iscorpio.plonepm.config import PROJECTNAME

# the XPointBuildJournal Schema.
XPointBuildJournalSchema = XPointDocument.schema.copy()

# Decide to use the build in plone keywording as the projects selection.
# Plone Keywording field is defined as subject in class
# Archetypes.ExtensibleMetadata.ExtensibleMetadata
# by default this LinesField is located in propertie tab (metadata),
# we need move it to the default tab and set it to required.
XPointBuildJournalSchema['subject'].schemata = 'default' # used to 'metadata'
XPointBuildJournalSchema['subject'].required = True
XPointBuildJournalSchema['subject'].widget.label = 'Projects'
XPointBuildJournalSchema['subject'].widget.description = \
    "Select projects for this build journal, holding CTRL key to select more than one project"
XPointBuildJournalSchema['subject'].widget.size = 6
XPointBuildJournalSchema.moveField('subject', after='description')

# the XPointBuildJournal class.
class XPointBuildJournal(XPointDocument):

    schema = XPointBuildJournalSchema

    meta_type = 'XPointBuildJournal'
    portal_type = 'XPointBuildJournal'
    archetype_name = 'Build Journal'

    security = ClassSecurityInfo()

registerType(XPointBuildJournal, PROJECTNAME)
