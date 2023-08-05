
# setuphandlers.py

"""
miscellaneous set up steps that are not handled by GS import/export
handlers.
"""

from StringIO import StringIO

from Products.CMFCore.utils import getToolByName
from Products.CMFEditions.setuphandlers import DEFAULT_POLICIES

__author__ = "Sean Chen"
__email__ = "sean.chen@leocorn.com"

# put your custom types in this list
TYPES_TO_VERSION = ('PPMProject', 'PPMStory', 'PPMIteration', 'PPMUseCase')

def importVarious(context):
    """
    make sure we have membrane installed.
    """

    if context.readDataFile('plonepm_various.txt') is None:
        # 
        return

    portal = context.getSite()
    setupVersioning(portal)

def setupVersioning(portal):

    portal_repository = getToolByName(portal, 'portal_repository')
    versionable_types = list(portal_repository.getVersionableContentTypes())
    for type_id in TYPES_TO_VERSION:
        if type_id not in versionable_types:
            # use append() to make sure we don't overwrite any
            # content-types which may already be under version control
            versionable_types.append(type_id)
            # Add default versioning policies to the versioned type
            for policy_id in DEFAULT_POLICIES:
                portal_repository.addPolicyForContentType(type_id, policy_id)
    portal_repository.setVersionableContentTypes(versionable_types)
