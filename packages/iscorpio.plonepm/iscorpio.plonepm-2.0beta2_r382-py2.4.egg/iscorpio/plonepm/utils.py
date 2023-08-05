
# utils.py

"""
Some handy facility script.
"""

import re

__author__ = "Sean Chen"
__email__ = "sean.chen@leocorn.com"

REVISION_PATTERN = r'(r([0-9]+))'

def revision2Link(description, linkBase):
    """
    convert the reversion number to SVN web view changeset.
    """

    revisions = re.findall(REVISION_PATTERN, description)
    newDesc = description
    for rNumber, number in revisions:

        link = "<a href='%s?view=rev&revision=%s'>%s</a>" % \
               (linkBase, number, rNumber)
        newDesc = newDesc.replace(rNumber, link)

    return newDesc
