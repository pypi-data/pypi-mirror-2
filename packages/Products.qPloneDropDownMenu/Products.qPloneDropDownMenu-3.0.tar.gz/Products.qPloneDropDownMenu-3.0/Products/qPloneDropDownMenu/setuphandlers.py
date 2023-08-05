from Products.CMFCore.utils import getToolByName

from utils import updateMenu
from config import PROPERTY_SHEET, PROPERTY_FIELD

def installMenu(context):

    if context.readDataFile('qplonedropdownmenu_various.txt') is None:
        return

    site = context.getSite()
    portal_props = getToolByName(site, 'portal_properties')

    # skip adding property if it already exists
    prop_sheet = getattr(portal_props.aq_base, PROPERTY_SHEET, None)
    if prop_sheet is not None:
        prop_field = getattr(prop_sheet.aq_base, PROPERTY_FIELD, None)
        if prop_field is not None:
            return

    updateMenu(site)
