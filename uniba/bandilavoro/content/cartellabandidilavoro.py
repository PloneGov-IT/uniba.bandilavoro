"""Definition of the Cartella Bandi di lavoro content type
"""

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

from uniba.bandilavoro import bandiMessageFactory as _
from uniba.bandilavoro.interfaces import ICartellaBandidiLavoro
from uniba.bandilavoro.config import PROJECTNAME

from zope.interface import implements


CartellaBandidiLavoroSchema = folder.ATFolderSchema.copy() + atapi.Schema((

    atapi.LinesField(name='elencodipartimenti',
            widget=atapi.LinesWidget(
                label=_(u"label_cartellabandi_elencodipartimenti",
                        default=u"Elenco dei dipartimenti"),
                description=_(u"desc_cartellabandi_elencodipartimenti",
                              default=u"Elencare i dipartimenti uno per linea"),
                ),
            required=True,
        ),
    atapi.LinesField(name='elencotipologiecontrattuali',
            widget=atapi.LinesWidget(
                label=_(u"label_cartellabandi_elencotipologiecontrattuali",
                        default=u"Elenco delle tipologie contrattuali"),
                description=_(u"desc_cartellabandi_elencotipologiecontrattuali",
                              default=u"Elencare le tipologie (tipo Co.co.co.) una per linea"),
                ),
            required=True,
        ),
    atapi.LinesField(name='elencotipologieprofilo',
            widget=atapi.LinesWidget(
                label=_(u"label_cartellabandi_elencotipologieprofilo",
                        default=u"Elenco delle tipologie di profilo"),
                description=_(u"desc_cartellabandi_elencotipologieprofilo",
                              default=u"Elencare le tipologie di profilo (tipo 'Didattico', 'Non didattico', 'Tecnico') una per linea"),
                ),
            required=True,
        ),
    atapi.LinesField(name='elencoarchi',
            widget=atapi.LinesWidget(
                label=_(u"label_cartellabandi_elencoarchi",
                        default=u"Elenco archi temporali per i profili"),
                description=_(u"desc_cartellabandi_elencoarchi",
                              default=u"Elencare le tipologie di archi temporali disponibili (tipo 'giorni', 'mesi', 'anni') una per linea"),
                ),
            required=True,
        ),
))

CartellaBandidiLavoroSchema['title'].storage = atapi.AnnotationStorage()
CartellaBandidiLavoroSchema['description'].storage = atapi.AnnotationStorage()
CartellaBandidiLavoroSchema['elencodipartimenti'].storage = atapi.AnnotationStorage()
CartellaBandidiLavoroSchema['elencotipologiecontrattuali'].storage = atapi.AnnotationStorage()
CartellaBandidiLavoroSchema['elencotipologieprofilo'].storage = atapi.AnnotationStorage()
CartellaBandidiLavoroSchema['elencoarchi'].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(
    CartellaBandidiLavoroSchema,
    folderish=True,
    moveDiscussion=False
)


class CartellaBandidiLavoro(folder.ATFolder):
    """Cartella che raccoglie tutti i Bandi di lavoro dei Dipartimenti"""
    implements(ICartellaBandidiLavoro)

    meta_type = "CartellaBandidiLavoro"
    schema = CartellaBandidiLavoroSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')

    

atapi.registerType(CartellaBandidiLavoro, PROJECTNAME)
