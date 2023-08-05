
# PPMUseCase.py

__doc__ = """PPMUseCases defines a use case for a software project.
A use case could explain a funcationality from function specification.
"""
__author__ = 'iScorpio <iscorpio@users.sourceforge.net>'
__docformat__ = 'plaintext'

import logging

from zope.interface import implements

from AccessControl import ClassSecurityInfo
# from Archetypes
from Products.Archetypes.public import Schema
from Products.Archetypes.public import registerType

# the configruation info for this project.
from iscorpio.plonepm.config import PROJECTNAME
from iscorpio.plonepm.content.base import XPPMBase
from iscorpio.plonepm.content.base import XPPMDocBase
from iscorpio.plonepm.interfaces import IPPMUseCase

# the use case schema.
PPMUseCaseSchema = XPPMDocBase.schema.copy()

# set up the label and description for generic field.
PPMUseCaseSchema['xppm_text'].widget.label = "Use Case Text"
PPMUseCaseSchema['xppm_text'].widget.description = "Details explain for this use case."

# the use case class.
class PPMUseCase(XPPMBase, XPPMDocBase):
    """ content type class for a use case.
    """

    schema = PPMUseCaseSchema

    meta_type = "PPMUseCase"
    portal_type = "PPMUseCase"
    archetype_name = "PPMUseCase"

    __implements__ = (
        XPPMDocBase.__implements__,
        )
    implements(IPPMUseCase)

    xppm_id_prefix = "uc"
    log = logging.getLogger("PlonePM PPMUseCase")
    security = ClassSecurityInfo()

registerType(PPMUseCase, PROJECTNAME)
