## Controller Python Script "csshover_save"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=enabled=False, csshovering=[], sheetId='csshover.css', title='CSS Hover'
##title=
##

from Products.CMFCore.utils import getToolByName
from Products.qPloneDropDownMenu.utils import addCSS
folder = getToolByName(context, 'portal_skins').restrictedTraverse('custom')

if csshovering.find('.cssHoverCSSExists {}') == -1: csshovering = '.cssHoverCSSExists {}\n\n' + csshovering
if not sheetId in folder.objectIds():
    if csshovering.find('Use this configlet in IE') != -1: csshovering = " "
    addCSS(folder, sheetId, title, csshovering)
    message = 'Added %s to plone_skins  custom folder. ' % sheetId
else:
    if csshovering.find('Use this configlet in IE') == -1:
        getattr(folder, sheetId).manage_edit(csshovering,title)
        message = 'Updated %s. ' % sheetId
    else: message = 'Visit this page in IE to see and activate generated CSS. '
cssreg = getToolByName(context, 'portal_css', None)
if cssreg is not None:
    stylesheet_ids = cssreg.getResourceIds()
    if sheetId not in stylesheet_ids:
        cssreg.registerStylesheet(id=sheetId, enabled=enabled)
        try: cssreg.moveResource(sheetId, cssreg.getResourcePosition('textLarge.css')+1)
        except: pass
        cssreg.cookResources()
    else:
        cssreg.updateStylesheet(sheetId, **{'enabled' : enabled})
        cssreg.cookResources()
else:
    message += "For activating csshover.css customize ploneCustom.css and add <dtml-var csshover.css> line before <dtml-var drop_down.css>"

context.plone_utils.addPortalMessage(message)

return state.set(status='success')