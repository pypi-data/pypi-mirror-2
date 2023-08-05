
# PPMFuncReq.py

__doc__ = """PPMFuncReq defines a function requirment for a software project."""
__docformat__ = 'plaintext'

import logging

from Products.Archetypes.public import Schema
from Products.Archetypes.public import registerType

from iscorpio.plonepm.config import PROJECTNAME
from iscorpio.plonepm.content.base import XPPMBase
from iscorpio.plonepm.content.base import XPPMDocBase

# the function requirement schema
PPMFuncReqSchema = XPPMDocBase.schema.copy()

# set up label and description for generic fields.
PPMFuncReqSchema['xppm_text'].widget.label = "Function Requirement Text"
PPMFuncReqSchema['xppm_text'].widget.description = "The details explain of the function requirement."

__author__ = 'Sean Chen'
__email__ = 'chyxiang@gmail.com'

# the classes.
class PPMFuncReq(XPPMBase, XPPMDocBase):
    """ content type for a function requirement.
    """

    schema = PPMFuncReqSchema

    meta_type = "PPMFuncReq"
    portal_type = "PPMFuncReq"
    archetype_name = "PPMFuncReq"

    __implements__ = (
        XPPMDocBase.__implements__,
        )

    xppm_id_prefix = "fr"
    log = logging.getLogger("PlonePM PPMFuncReq")

registerType(PPMFuncReq, PROJECTNAME)
