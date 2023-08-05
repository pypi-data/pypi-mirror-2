# permission.py

import logging

from AccessControl import ModuleSecurityInfo
from AccessControl import Permissions

try: # Plone 3.0.x
    from Products.CMFCore import permissions as CMFCorePermissions
except: # Old CMF
    from Products.CMFCore import CMFCorePermissions
import Products.Archetypes.public as atapi
import config

log = logging.getLogger('PlonePM permissions')

# The setting of the permission and the roll is made. This function is 
# called from __ init__.py.
def initialize():
    # Container that stores permission according to contents type finally 
    # output.
    permissions = {}

    # The list of the contents type registered to Archetype is acquired.
    types = atapi.listTypes(config.PROJECTNAME)

    # The permission setting of each contents type is added.
    for atype in  types:
        # The permission name displayed in the permission tab of ZMI is 
        # made.
        permission = "%s: Add %s" % (config.PROJECTNAME, atype['portal_type'])

        # The permission made for the dictionary of the contents type is 
        # preserved.
        permissions[atype['portal_type']] = permission

        # The permission name and the access permit at each roll 
        # corresponding to the permission name is set to CMFCore.
        CMFCorePermissions.setDefaultRoles(permission, ('Manager','Owner'))

    return permissions
