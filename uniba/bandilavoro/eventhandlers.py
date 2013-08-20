#

def afterRettifica(obj, event):
    """ in caso avvenga la transazione di pubblicazione, allora redirigo verso l'editing del contenitore"""
    if event.status['action']=='publish':
        response = obj.REQUEST.RESPONSE
        contenitore = obj.__parent__
        url = contenitore.absolute_url()
        import pdb;pdb.set_trace()
        return response.redirect(url)
    
    pass
