from zope.component import getMultiAdapter
from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.statusmessages.interfaces import IStatusMessage



class PrefsDropDownView(BrowserView):
    """DropDown configlet.
    
    """

    template = ViewPageTemplateFile('templates/prefs_dropdownmenu_edit_form.pt')

    def __init__(self, context, request):
        super(PrefsDropDownView, self).__init__(context, request)
        self.portal_state = getMultiAdapter((self.context, self.request),
                                             name='plone_portal_state')
        self.portal = self.portal_state.portal()
        self.pp = getToolByName(self.portal, 'portal_properties')
        self.dp = getattr(self.pp, 'dropdownmenu_properties', None)

    def menu(self):
        menu = ''
        if self.dp is not None:
             menu = self.dp.getProperty('menu', '')
        return menu 

    def __call__(self):
        save = self.request.get('save', None)
        update = self.request.get('regenerate_menu', None)
        status = IStatusMessage(self.request)

        if save is not None:

            if self.dp is None:
                status.addStatusMessage(
                """Dropdown menu property sheet does not exist.
                Please, firstly regenerate menu before editing it.""")
                return self.template()

            menu = self.menu()
            if not menu:
                status.addStatusMessage(
                """Menu field does not exist in dropdown menu property sheet.
                Please, firstly regenerate menu before editing it.""")
                return self.template()

            self.dp.manage_changeProperties(menu=self.request.get('menu'))
            status.addStatusMessage("DropDown Menu updated.")
            return self.template()
            
        if update is not None:
            getToolByName(self.portal, 'portal_dropdownmenu').regenerateMenu()
            status.addStatusMessage("DropDown Menu regenerated.")

        return self.template()
