from App.class_init import InitializeClass
from OFS.SimpleItem import SimpleItem
from AccessControl import ClassSecurityInfo

from Products.CMFCore.utils import UniqueObject, getToolByName

from utils import updateMenu
from config import MANAGE_PERMISSION, PROJECT_NAME, UNIQUE_ID


class DropDownMenuTool(UniqueObject, SimpleItem):

    meta_type = 'DropDownMenu Tool'
    id = UNIQUE_ID
    title="DropDown Menu Tool"

    security = ClassSecurityInfo()

    security.declareProtected(MANAGE_PERMISSION, 'regenerateMenu')
    def regenerateMenu(self):
        portal = getToolByName(self, 'portal_url').getPortalObject()
        updateMenu(portal)

InitializeClass(DropDownMenuTool)
