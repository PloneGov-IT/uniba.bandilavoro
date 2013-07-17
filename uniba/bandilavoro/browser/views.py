from plone.registry.interfaces import IRegistry

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.Five.browser import BrowserView

from uniba.bandilavoro.interfaces import IBando, ISettingsBandi

from zope.component import getMultiAdapter, getUtility

class bandoView(BrowserView):
    """ view per l'oggetto Bando """
    index = ViewPageTemplateFile("bando_view.pt")
    
    def render(self):
        return self.index()
        
    def __call__(self):
        return self.render()
        
    def getDipartimentobando(self,dipartimentoinbreve):
        registry = getUtility(IRegistry)
        settings = registry.forInterface(ISettingsBandi)
        dipartimenti = settings.settingDipartimenti