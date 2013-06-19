from z3c.form import interfaces

from zope import schema
from zope.interface import Interface

from zope.i18nmessageid import MessageFactory
from uniba.bandilavoro import bandiMessageFactory as _


class ISettingsBandi(Interface):
    """Settaggi da controlpanel utili per la definizione di vocabolari
    """

    settingTipocontratto = schema.List(title=_(u"Tipologia contrattuale"), description=_(u"Un tipo per linea"),
                                  required=True,
                                  value_type=schema.TextLine(required=True))
    
    settingTipoprofilo = schema.List(title=_(u"Tipologia profilo"), description=_(u"Un tipo per linea"),
                                required=False,
                                value_type=schema.TextLine(required=False))

    settingDipartimenti = schema.List(title=_(u"Dipartimenti"), description=_(u"Uno per linea"),
                                required=True,
                                value_type=schema.TextLine(required=True))