# memo.py

__doc__ = """XPointMemo defines the memo for a XPoint Project."""
__author__ = 'iScorpio <iscorpio@users.sourceforge.net>'
__docformat__ = 'plaintext'

import logging

from AccessControl import ClassSecurityInfo
# from Archetypes
from Products.Archetypes.public import registerType

from iscorpio.plonepm.content.xpointdoc import XPointDocument
# the configruation info for this project.
from iscorpio.plonepm.config import PROJECTNAME

# define the schem for XPointMemo.
XPointMemoSchema = XPointDocument.schema.copy()

# we don't need descrpiton field for a memo.
XPointMemoSchema['description'].widget.visible = False

# XPointMemo class.
class XPointMemo(XPointDocument):
    """ XPointMemo defines the note for a XPoint Project.
    """

    schema = XPointMemoSchema

    # type, name.
    meta_type = 'XPointMemo'
    portal_type = 'XPointMemo'
    archetype_name = 'XP Memo'

    _at_rename_after_creation = True

    security = ClassSecurityInfo()


def modify_fti(fti):
    # Hide unnecessary tabs (usability enhancement)
    for a in fti['actions']:
        if a['id'] in ['metadata']:
            a['visible'] = 0
    return fti

# register this type to plone add-on product.
registerType(XPointMemo, PROJECTNAME)
