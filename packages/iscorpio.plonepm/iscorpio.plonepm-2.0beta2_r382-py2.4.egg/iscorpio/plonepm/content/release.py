# release.py

__doc__ = """XPointRelease defines the release note for a XPoint Project."""
__author__ = 'iScorpio <iscorpio@users.sourceforge.net>'
__docformat__ = 'plaintext'

import logging

from AccessControl import ClassSecurityInfo
# from Archetypes
from Products.Archetypes.public import registerType

from iscorpio.plonepm.content.xpointdoc import XPointDocument
# the configruation info for this project.
from iscorpio.plonepm.config import PROJECTNAME

# define the schema for XPointRelease
XPointReleaseSchema = XPointDocument.schema.copy()

# XPointRelease class.
class XPointRelease(XPointDocument):
    """ XPointRelease will hold a release note for a XPoint Project.
    """

    schema = XPointReleaseSchema

    # define type and name.
    meta_type = 'XPointRelease'
    portal_type = 'XPointRelease'
    archetype_name = 'XP Release'

    _at_rename_after_creation = True

    security = ClassSecurityInfo()

# register this type to plone add-on product.
registerType(XPointRelease, PROJECTNAME)
