from zope.interface import Interface
# -*- Additional Imports Here -*-


class IProfilo(Interface):
    """Profilo messo a concorso tramite bando"""

    # -*- schema definition goes here -*-
    
class IMoneyFormat(Interface):
    """
    Used to retrieve correct format as money value
    """