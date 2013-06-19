"""Definition of the Profilo content type
"""
from AccessControl import ClassSecurityInfo

from plone.registry.interfaces import IRegistry

from Products.Archetypes import atapi
from Products.Archetypes.Schema import getSchemata
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata
from Products.CMFCore import permissions

from uniba.bandilavoro.interfaces import IProfilo, ISettingsBandi
from uniba.bandilavoro.config import PROJECTNAME
from uniba.bandilavoro import bandiMessageFactory as _

from zope.interface import implements
from zope.component import getMultiAdapter, getUtility

ProfiloSchema = folder.ATFolderSchema.copy() + atapi.Schema((
    
    atapi.TextField('oggettoprestazione',
             required=True,
             searchable=False,
             validators = ('isTidyHtmlWithCleanup',),
             default_output_type = 'text/x-html-safe',
             widget = atapi.RichWidget(
                       label = _(u'label_profilo_oggettoprestazione', default=u'Oggetto prestazione'),
                       description = _(u'desc_profilo_oggettoprestazione',
                                             default=u'Oggetto della prestazione lavorativa'),
                       rows=5,
                       allow_buttons=(
                               'pastetext',
                               'bold',
                               'italic',
                               'link',
                               'unlink',
                               ),
                       )),
    atapi.TextField('requisitiprofilo',
            required=False,
            searchable=False,
            validators = ('isTidyHtmlWithCleanup',),
            default_output_type = 'text/x-html-safe',
            widget = atapi.RichWidget(
                      label = _(u'label_profilo_requisitiprofilo', default=u'Requisiti per la partecipazione'),
                      rows=5,
                      allow_buttons=(
                              'pastetext',
                              'bold',
                              'italic',
                              'link',
                              'unlink',
                              ),
                      )),
    atapi.StringField('tipoprofilo',
           required=False,
           searchable=True,
           vocabulary='getTipoprofilo',
           widget = atapi.SelectionWidget(
                     label = _(u'label_profilo_tipoprofilo', default=u'Tipologia del profilo richiesto'),
                     )),
    atapi.IntegerField('durata',
            required=True,
            searchable=False,
            validators = ('isInt',),
            widget = atapi.StringWidget(
                      label = _(u'label_profilo_durata', default=u'Durata del contratto'),
                       description = _(u'desc_profilo_durata',
                                               default=u'Solo un numero di tipo intero'),
                      )),
    atapi.StringField('durataespressain',
          required=True,
          searchable=False,
          vocabulary=(['giorni','mesi','anni']),
          widget = atapi.SelectionWidget(
                    label = _(u'label_profilo_durataespressain', default=u'Durata espressa in '),
                    )),
    atapi.FixedPointField('compenso',
          required=True,
          searchable=False,
          widget = atapi.StringWidget(
                    label = _(u'label_profilo_compenso', default=u'Compenso'),
                    description = _(u'desc_profilo_compenso', default=u'Da inputare con punteggiatura per le sole decine, es. 10000.00'),
                    )),

))

# Set storage on fields copied from ATFolderSchema, making sure
# they work well with the python bridge properties.

ProfiloSchema['title'].storage = atapi.AnnotationStorage()
ProfiloSchema['description'].storage = atapi.AnnotationStorage()
ProfiloSchema['description'].widget.visible = {'view': 'hidden', 'edit': 'hidden' }

schemata.finalizeATCTSchema(
    ProfiloSchema,
    folderish=True,
    moveDiscussion=False
)


class Profilo(folder.ATFolder):
    """Profilo messo a concorso tramite bando"""
    implements(IProfilo)

    meta_type = "Profilo"
    schema = ProfiloSchema
    
    def getCampi(self):
        """ tramite questo metodo mostro i campi della presente classe 
            utile per il tipo di oggetto 'Rettifica' 
            in formato DisplayList (utile per costruire Vocabulary)"""
        from Products.Archetypes.utils import DisplayList
        dl = DisplayList()
        # filtro i campi della presente classe ottenendo solo quelli della schemata default
        campi = self.schema.filterFields(schemata='default')
        # costruisco il dizionaro in DisplayList
        # testo anche se hanno l'attributo default posto
        dl.fromList([(x.getName(), x.widget.label.default) for x in campi if hasattr(x.widget.label, 'default')])
        return dl
    
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

    # ottengo le tipologie di profilo mappate dal pannello di controllo
    def getTipoprofilo(self):
        """ ottengo le tipologie di profilo"""
        registry = getUtility(IRegistry)
        settings = registry.forInterface(ISettingsBandi)
        tipoprofilo = settings.settingTipoprofilo
        return tipoprofilo

atapi.registerType(Profilo, PROJECTNAME)
