import zope.component
from plone.indexer import indexer

def reDatatermine(obj, event):
    """ reindexa gli oggetti Profilo eventualmente presenti nel bando modificato """
    profili = obj.getFolderContents(contentFilter={'portal_type':'Profilo'})
    for profilo in profili:
        profilo.getObject().reindexObject(idxs=['datatermine'])
        
    return
