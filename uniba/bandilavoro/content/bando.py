"""Definition of the Bando content type
"""
from AccessControl import ClassSecurityInfo

from DateTime.DateTime import DateTime

from plone.registry.interfaces import IRegistry

from Products.Archetypes import atapi
from Products.Archetypes.Schema import getSchemata
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata
from Products.CMFCore import permissions

from uniba.bandilavoro.interfaces import IBando, ISettingsBandi
from uniba.bandilavoro.config import PROJECTNAME
from uniba.bandilavoro import bandiMessageFactory as _

from zope.interface import implements
from zope.container.interfaces import INameChooser
from zope.component import getMultiAdapter, getUtility


BandoSchema = folder.ATFolderSchema.copy() + atapi.Schema((

    atapi.ComputedField(
            'title',
            accessor='Title',
            searchable=1,
            expression="context.computeTitle()",
        ),

    atapi.StringField('dipartimentobando',
             required=True,
             searchable=True,
             vocabulary='getDipartimento',
             widget = atapi.SelectionWidget(
                       label = _(u'label_bando_dipartimentobando', default=u'Dipartimento che emana il bando'),
                       format = 'select',
                       )),
    atapi.StringField('decretobando',
             required=True,
             searchable=True,
             widget = atapi.StringWidget(
                       label = _(u'label_bando_decretobando', default=u'Numero decreto'),
                       description = _(u'desc_bando_decretobando',
                                       default=u'E\' auspicabile inserire informazioni complete come ad esempio: DD. 80/2013'),
                       )),
    atapi.StringField('linkindagine',
             required=True,
             searchable=True,
             validators = ('isURL',),
             widget = atapi.StringWidget(
                       label = _(u'label_bando_linkindagine', default=u'Indagine conoscitiva'),
                       description = _(u'desc_bando_linkindagine',
                                          default=u'Link alla pagina web dove e\' stata pubblicata l\'indagine conoscitiva'),
                       )),
    atapi.StringField('strutturaservizio',
             required=False,
             searchable=True,
             widget = atapi.StringWidget(
                       label = _(u'label_bando_strutturaservizio', default=u'Struttura di servizio'),
                       )),
   atapi.StringField('tipocontratto',
            required=True,
            searchable=True,
            vocabulary='getTipocontratto',
            widget = atapi.SelectionWidget(
                      label = _(u'label_bando_tipocontratto', default=u'Tipologia contrattuale'),
                      )),
    atapi.DateTimeField('dataemanazione',
             required=True,
             searchable=False,
             default_method = 'getDefaultTime',
             widget = atapi.CalendarWidget(
                       future_years=1,
                       label = _(u'label_bando_dataemanazione', default=u'Data di emanzione del bando'),
                       )),
    atapi.DateTimeField('datatermine',
             required=True,
             searchable=False,
             default_method = 'getDefaultTime',
             widget = atapi.CalendarWidget(
                       future_years=1,
                       label = _(u'label_bando_datatermine', default=u'Data di termine per la presentazione delle domande'),
                       )),
    atapi.TextField('modalitapresentazione',
             required=True,
             searchable=False,
             validators = ('isTidyHtmlWithCleanup',),
             default_output_type = 'text/x-html-safe',
             widget = atapi.RichWidget(
                       label = _(u'label_bando_modalitapresentazione', default=u'Modalita\' di presentazione della domanda'),
                       rows=5,
                       allow_buttons=(
                               'pastetext',
                               'bold',
                               'italic',
                               'link',
                               'unlink',
                               ),
                       )),
    atapi.TextField('elementivalutazione',
             required=True,
             searchable=True,
             validators = ('isTidyHtmlWithCleanup',),
             default_output_type = 'text/x-html-safe',
             widget = atapi.RichWidget(
                       label = _(u'label_bando_modalitapresentazione', default=u'Elementi di valutazione della candidatura'),
                       rows=10,
                       allow_buttons=(
                               'pastetext',
                               'bold',
                               'italic',
                               'link',
                               'unlink',
                               ),
                       )),
   atapi.FileField('filedecretobando',
            required=True,
            widget = atapi.FileWidget(
                      label = _(u'label_bando_filedecretobando', default=u'File decreto'),
                      )),
   atapi.TextField('notebando',
           required=False,
           searchable=False,
           validators = ('isTidyHtmlWithCleanup',),
           default_output_type = 'text/x-html-safe',
           widget = atapi.RichWidget(
                     label = _(u'label_bando_notebando', default=u'Note'),
                     rows=10,
                     allow_buttons=(
                             'pastetext',
                             'bold',
                             'italic',
                             'link',
                             'unlink',
                             ),
                    )),       
    
    # ---- SCHEMATA COMMISSIONE ----                
    atapi.StringField('decretonominacommissione',
             schemata='commissione',
             required=False,
             searchable=False,
             widget = atapi.StringWidget(
                       label = _(u'label_bando_decretonominacommissione', default=u'Decreto di nomina della commissione'),
                       description = _(u'desc_bando_decretonominacommissione',
                                       default=u'E\' auspicabile inserire informazioni complete come ad esempio: DD. 80/2013'),
                       )),
   atapi.LinesField('componenticommissione',
            schemata='commissione',
            required=False,
            searchable=False,
            widget = atapi.LinesWidget(
                      label = _(u'label_bando_componenticommissione', default=u'Nominativi componenti della Commissione'),
                      description = _(u'desc_bando_componenticommissione',
                                      default=u'Uno per linea, ad es.: dott. Mario Rossi, cat. EP, presidente della Commissione'),
                      )),
    atapi.FileField('filecomponenticommissione',
           schemata='commissione',
           required=True,
           widget = atapi.FileWidget(
                     label = _(u'label_bando_filecomponenticommissione', default=u'File decreto di nomina Commissione'),
                     )),
   
))

# Set storage on fields copied from ATFolderSchema, making sure
# they work well with the python bridge properties.

BandoSchema['title'].storage = atapi.AnnotationStorage()
BandoSchema['title'].widget.visible = {'view': 'hidden', 'edit': 'hidden' }
BandoSchema['description'].storage = atapi.AnnotationStorage()
BandoSchema['description'].widget.visible = {'view': 'hidden', 'edit': 'hidden' }

schemata.finalizeATCTSchema(
    BandoSchema,
    folderish=True,
    moveDiscussion=False
)



class Bando(folder.ATFolder):
    """Bando di selezione per personale"""
    implements(IBando)
    
    meta_type = "Bando"
    schema = BandoSchema
    
    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')
    
    def getCampi(self):
        """ tramite questo metodo mostro i campi della presente classe 
            utile per il tipo di oggetto 'Rettifica' 
            in formato DisplayList (utile per costruire Vocabulary)"""
        from Products.Archetypes.utils import DisplayList
        dl = DisplayList()
        # filtro i campi della presente classe ottenendo solo quelli della schemata default e commissione
        campi = self.schema.getSchemataFields('default')
        campicommissione = self.schema.getSchemataFields('commissione')
        for campo in campicommissione: campi.append(campo)
        # costruisco il dizionaro in DisplayList
        # testo anche se hanno l'attributo default posto
        dl.fromList([(x.getName(), x.widget.Label('default').default) for x in campi if hasattr(x.widget.Label('default'), 'default')])
        return dl
    
    # ottengo le tipologie contrattuali mappate dal pannello di controllo
    def getDipartimento(self):
        """ ottengo la lista dei dipartimenti settata in pannello di configurazione"""
        registry = getUtility(IRegistry)
        settings = registry.forInterface(ISettingsBandi)
        dipartimenti = settings.settingDipartimenti
        return dipartimenti
    
    # ottengo le tipologie contrattuali mappate dal pannello di controllo
    def getTipocontratto(self):
        """ ottengo le tipologie contrattuali"""
        registry = getUtility(IRegistry)
        settings = registry.forInterface(ISettingsBandi)
        tipocontratto = settings.settingTipocontratto
        return tipocontratto
    
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
    
    # computo il titolo dell'oggetto (e quindi id) automaticamente
    def computeTitle(self):
        """Get object's title."""
        nomedip = self.getField('dipartimentobando')
        nomedip = nomedip.getRaw(self)
        numdecreto = self.getField('decretobando')
        numdecreto = numdecreto.getRaw(self)
        return nomedip+' '+numdecreto
    
    def getDefaultTime(self):
            return DateTime()
    

atapi.registerType(Bando, PROJECTNAME)
