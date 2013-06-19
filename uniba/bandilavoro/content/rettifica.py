"""Definition of the Rettifica content type
"""
from AccessControl import ClassSecurityInfo

from plone.registry.interfaces import IRegistry

from Products.Archetypes import atapi
from Products.Archetypes.Schema import getSchemata
from Products.Archetypes.utils import DisplayList
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata
from Products.ATContentTypes.content.file import ATFileSchema
from Products.CMFCore import permissions

# -*- Message Factory Imported Here -*-

from uniba.bandilavoro.interfaces import IRettifica
from uniba.bandilavoro.config import PROJECTNAME
from uniba.bandilavoro import bandiMessageFactory as _

from zope.interface import implements
from zope.component import getMultiAdapter, getUtility

# eredito lo schema del tipo File classico
RettificaSchema = ATFileSchema.copy() + atapi.Schema((

    atapi.LinesField('rettificapercampi',
           required=False,
           searchable=True,
           multiValued=True,
           vocabulary='getCampiDaRettificare',
           widget = atapi.MultiSelectionWidget(
                     label = _(u'label_rettifica_rettificapercampi', default=u'Campi da rettificare'),
                     description = _(u'desc_rettifica_rettificapercampi', default=u'E\' selezionabile anche piu\' di un campo'),
                     )),

))

# Set storage on fields copied from ATContentTypeSchema, making sure
# they work well with the python bridge properties.

RettificaSchema['title'].storage = atapi.AnnotationStorage()
RettificaSchema['description'].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(RettificaSchema, moveDiscussion=False)


class Rettifica(base.ATCTContent):
    """File di rettifica al bando"""
    implements(IRettifica)

    meta_type = "Rettifica"
    schema = RettificaSchema
    
    def getCampiDaRettificare(self):
        """ ottengo i campi chiamando il metodo getCampi """
        
        return self.getCampi()
    
    # nascondo gli schemata che non servono
    security = ClassSecurityInfo()
    security.declareProtected(permissions.View, 'Schemata')
    def Schemata(self,):
        """ override dello schema per nascondere altre azioni agli utenti"""
        blacklist = ['categorization',
                     'dates',
                     'creators',
                     'settings',
                     ]
        pps = getMultiAdapter((self, self.REQUEST), name=u'plone_portal_state')
        member = pps.member()
        
        schemata = getSchemata(self)
        
        if member.has_role('Manager'):
            return schemata
        
        for x in blacklist:
            schemata.pop(x)
        
        return schemata

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')

    # -*- Your ATSchema to Python Property Bridges Here ... -*-

atapi.registerType(Rettifica, PROJECTNAME)
