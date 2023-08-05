
# PPMSysReq.py

__doc__ = """PPMSysReq defines a system requirment for a software project."""
__docformat__ = 'plaintext'

import logging

from Products.Archetypes.public import Schema
from Products.Archetypes.public import registerType

from iscorpio.plonepm.config import PROJECTNAME
from iscorpio.plonepm.content.base import XPPMBase
from iscorpio.plonepm.content.base import XPPMDocBase

__author__ = 'Sean Chen'
__email__ = 'chyxiang@gmail.com'

# the function requirement schema
PPMSysReqSchema = XPPMDocBase.schema.copy()

# set up label and description for generic fields.
PPMSysReqSchema['xppm_text'].widget.label = "System Requirement Text"
PPMSysReqSchema['xppm_text'].widget.description = "The details explain of the system requirement."

# the classes.
class PPMSysReq(XPPMBase, XPPMDocBase):
    """ content type for a system requirement.
    """

    schema = PPMSysReqSchema

    meta_type = "PPMSysReq"
    portal_type = "PPMSysReq"
    archetype_name = "PPMSysReq"

    __implements__ = (
        XPPMDocBase.__implements__,
        )

    xppm_id_prefix = "xpsr"
    log = logging.getLogger("PlonePM PPMSysReq")

registerType(PPMSysReq, PROJECTNAME)
