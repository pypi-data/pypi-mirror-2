try:
    from Products.CMFCore import permissions
except ImportError:
    from Products.CMFCore import CMFCorePermissions as permissions
 
MANAGE_PERMISSION = permissions.ManagePortal

PROJECT_NAME = 'qPloneDropDownMenu'
UNIQUE_ID = "portal_dropdownmenu"

PROPERTY_SHEET = 'dropdownmenu_properties'
PROPERTY_FIELD = 'menu'
