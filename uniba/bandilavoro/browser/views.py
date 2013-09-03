from Acquisition import aq_inner

from Products.CMFCore.utils import getToolByName

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.Five.browser import BrowserView

from uniba.bandilavoro.interfaces import IBando

from zope.component import getMultiAdapter, getUtility

class bandoView(BrowserView):
    """ view per l'oggetto Bando """
    index = ViewPageTemplateFile("bando_view.pt")
    
    def render(self):
        return self.index()
        
    def __call__(self):
        return self.render()
        
        
    def oggettiDiRettifica(self):
        """ ritorna la lista di tutti gli oggetti Rettifica presenti nel bando e nei profili annessi 
            utile per creare la lista a destra"""
        context= self.context
        catalog = getToolByName(context, 'portal_catalog')
        folder_path = '/'.join(context.getPhysicalPath())
        results = catalog(path={'query': folder_path, 'depth': 2}, portal_type='Rettifica', sort_on='effective', sort_order='descending')
        return results
        
    def allegatiAlBando(self):
        """ ritorna la lista di tutti gli oggetti di tipo files presenti nella cartella del bando """
        context=self.context
        brains = context.getFolderContents(contentFilter={'portal_type':'File', 'sort_on':'effective', 'sort_order':'descending'})
        return brains
        
class Macros(BrowserView):
    """ macros utili per i bandi """
    template = ViewPageTemplateFile('bandilavoro_macros.pt')

    def __getitem__(self, key):
        return self.template.macros[key]
        
class rettifiche(BrowserView):
    """ ottengo le rettifiche per dato bando/profilo
        in caso stia analizzando il bando allora l'oggetto di indagine e' il contesto stesso"""
    
    def campiConRettifiche(self):
        context=self.context
        brains = context.getFolderContents(contentFilter={'portal_type':'Rettifica'})
        campirettificati = set()
        for x in brains:
            campirettificati = campirettificati.union(set(x.getObject().getRettificapercampi()))
            
        return tuple(campirettificati)