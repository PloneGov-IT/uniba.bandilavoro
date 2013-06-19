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
    description = _(u"""""")

    def updateFields(self):
        super(BandiSettingsEditForm, self).updateFields()


    def updateWidgets(self):
        super(BandiSettingsEditForm, self).updateWidgets()
        
    @button.buttonAndHandler(_(u"Save"), name='save')
    def handleSave(self, action):
        data, errors = self.extractData()
        #controllo duplicati e creo lista unica
        if (data):
            data['settingTipocontratto']=sorted(data['settingTipocontratto'])
            import collections
            listone = collections.Counter(data['settingTipocontratto'])            
            data['settingTipocontratto'] = list(listone)
        
        if errors:
            self.status = self.formErrorsMessage
            return
        #ordino la lista in ordine alfabetico
        self.applyChanges(data)
        IStatusMessage(self.request).addStatusMessage(
            _(u"Dati salvati"),
            "info")
        self.request.response.redirect(self.request.getURL())

    @button.buttonAndHandler(_(u"Cancel"), name='cancel')
    def handleCancel(self, action):
        IStatusMessage(self.request).addStatusMessage(
            _(u"Modifiche annullate"),
            "info")
        self.request.response.redirect("%s/%s" % (
            self.context.absolute_url(),
            self.control_panel_view))

class BandiSettingsControlPanel(controlpanel.ControlPanelFormWrapper):
    form = BandiSettingsEditForm
