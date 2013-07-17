from plone.app.registry.browser import controlpanel
from plone.registry.interfaces import IRegistry

from Products.statusmessages.interfaces import IStatusMessage

from uniba.bandilavoro.interfaces import ISettingsBandi
from uniba.bandilavoro import bandiMessageFactory as _

from z3c.form import form, button
from z3c.form.interfaces import ActionExecutionError


class BandiSettingsEditForm(controlpanel.RegistryEditForm):

    schema = ISettingsBandi
    label = _(u"Configurazione bandi dipartimentali")
    description = _(u"""Gestione dei parametri di configurazione per i bandi""")

    def updateFields(self):
        super(BandiSettingsEditForm, self).updateFields()


    def updateWidgets(self):
        super(BandiSettingsEditForm, self).updateWidgets()
        

class BandiSettingsControlPanel(controlpanel.ControlPanelFormWrapper):
    form = BandiSettingsEditForm
