"""Definition of the Profilo content type
"""
from AccessControl import ClassSecurityInfo

from plone.registry.interfaces import IRegistry

from Products.Archetypes import atapi
from Products.Archetypes.Schema import getSchemata
from Products.Archetypes.utils import DisplayList
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata
from Products.CMFCore import permissions

from uniba.bandilavoro.interfaces import IProfilo, ISettingsBandi
from uniba.bandilavoro.config import PROJECTNAME
from uniba.bandilavoro import bandiMessageFactory as _

from zope.interface import implements
from zope.component import getMultiAdapter, getUtility


ProfiloSchema = folder.ATFolderSchema.copy() + atapi.Schema((

    atapi.IntegerField('nposti',
            required=True,
            searchable=False,
            default=1,
            validators = ('isInt',),
            widget = atapi.IntegerWidget(
                      label = _(u'label_profilo_nposti', default=u'Numero posti a concorso'),
                      )),
    
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
           required=True,
           searchable=False,
           default=None,
           vocabulary='getTipologiaprofilo',
           widget = atapi.SelectionWidget(
                     label = _(u'label_profilo_tipoprofilo', default=u'Tipologia del profilo richiesto'),
                     format = 'select',
                     )),
    atapi.IntegerField('durata',
            required=True,
            searchable=False,
            validators = ('isInt',),
            widget = atapi.IntegerWidget(
                      label = _(u'label_profilo_durata', default=u'Durata del contratto'),
                       description = _(u'desc_profilo_durata',
                                               default=u'Solo un numero di tipo intero'),
                      )),
    atapi.StringField('durataespressain',
          required=True,
          searchable=False,
          vocabulary=(('gg', 'giorni'),('mm', 'mese/1'),('aa', 'anno/i'),),
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

    # ---- SCHEMATA APPROVAZIONE ATTI ----
     atapi.StringField('decretoapprovazioneatti',
              schemata='approvazione',
              required=False,
              searchable=False,
              widget = atapi.StringWidget(
                        label = _(u'label_profilo_decretoapprovazioneatti', default=u'Decreto di approvazione atti'),
                        description = _(u'desc_profilo_decretoapprovazioneatti',
                                        default=u'E\' auspicabile inserire informazioni complete come ad esempio: DD. 80/2013'),
                        )),
    atapi.LinesField('vincitori',
             schemata='approvazione',
             required=False,
             searchable=False,
             widget = atapi.LinesWidget(
                       label = _(u'label_profilo_vincitori', default=u'Nominativo/i del vincitore/i per il presente profilo'),
                       description = _(u'desc_profilo_vincitori',
                                       default=u'Uno per linea'),
                       )),
     atapi.FileField('fileapprovazioneatti',
            schemata='approvazione',
            required=False,
            widget = atapi.FileWidget(
                      label = _(u'label_profilo_fileapprovazioneatti', default=u'File decreto di approvazione atti'),
                      )),
))

# Set storage on fields copied from ATFolderSchema, making sure
# they work well with the python bridge properties.

ProfiloSchema['title'].storage = atapi.AnnotationStorage()
ProfiloSchema['description'].storage = atapi.AnnotationStorage()
ProfiloSchema['description'].widget.visible = {'view': 'hidden', 'edit': 'hidden' }
ProfiloSchema['nposti'].storage = atapi.AnnotationStorage()
ProfiloSchema['oggettoprestazione'].storage = atapi.AnnotationStorage()
ProfiloSchema['requisitiprofilo'].storage = atapi.AnnotationStorage()
ProfiloSchema['tipoprofilo'].storage = atapi.AnnotationStorage()
ProfiloSchema['durata'].storage = atapi.AnnotationStorage()
ProfiloSchema['durataespressain'].storage = atapi.AnnotationStorage()
ProfiloSchema['compenso'].storage = atapi.AnnotationStorage()
ProfiloSchema['decretoapprovazioneatti'].storage = atapi.AnnotationStorage()
ProfiloSchema['vincitori'].storage = atapi.AnnotationStorage()
ProfiloSchema['fileapprovazioneatti'].storage = atapi.AnnotationStorage()

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
    
    def index_html(self):
        """ redirige sul contenitore di tipo bando 
            richiamando il metodo mioURL presente solo in tale oggetto """
        portal_tools = getMultiAdapter((self, self.REQUEST), name="plone_tools")
        response = self.REQUEST.response
        # in caso di editore allora passo la view standard
        if portal_tools.membership().checkPermission('Modify portal content',self):
            return response.redirect(self.absolute_url()+'/base_view')
        else:            
            urlbando = self.mioURL()
            return response.redirect(urlbando, status=303)
    
    def getCampi(self):
        """ tramite questo metodo mostro i campi della presente classe 
            utile per il tipo di oggetto 'Rettifica' 
            in formato DisplayList (utile per costruire Vocabulary)"""
        dl = DisplayList()
        # filtro i campi della presente classe ottenendo solo quelli della schemata default e approvazione
        campi = self.schema.getSchemataFields('default')
        campiapprovazione = self.schema.getSchemataFields('approvazione')
        for campo in campiapprovazione: campi.append(campo)
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
    nposti = atapi.ATFieldProperty('nposti')

    # ottengo le tipologie di profilo mappate dal pannello di controllo
    def getTipologiaprofilo(self):
        """ ottengo le tipologie di profilo in formato DisplayList"""
        registry = getUtility(IRegistry)
        settings = registry.forInterface(ISettingsBandi)
        tipoprofilo = settings.settingTipoprofilo
        dl = DisplayList()
        for x in tipoprofilo:
            dl.add(x,x)
        return dl

atapi.registerType(Profilo, PROJECTNAME)
