from zope.interface import Interface, implements
from zope.component import adapts, getMultiAdapter, getUtility
from zope.formlib import form
from zope import schema

from Products.CMFPlone.interfaces import IPloneSiteRoot
from Products.CMFDefault.formlib.schema import SchemaAdapterBase
from plone.app.viewletmanager.interfaces import IViewletSettingsStorage
from plone.app.controlpanel.form import ControlPanelForm
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import PloneMessageFactory as _
from plone.app.form.widgets.wysiwygwidget import WYSIWYGWidget
from DateTime import DateTime
from zope.event import notify
from uwosh.simpleemergency.events import SimpleEmergencyModifiedEvent

class ISimpleEmergencySchema(Interface):
    """
    Combined schema for the adapter lookup.
    """

    display_emergency = schema.Bool(
        title=_(u"Display emergency notification?"),
        default=False
    )
    
    show_on_all_pages = schema.Bool(
        title=_(u"Should the emergency notification be displayed on all pages?"),
        default=False
    )
    
    emergency_message = schema.Text(
        title=_(u"The emergency notification...")
    )

class SimpleEmergencyControlPanelAdapter(SchemaAdapterBase):

    adapts(IPloneSiteRoot)
    implements(ISimpleEmergencySchema)

    def __init__(self, context):
        super(SimpleEmergencyControlPanelAdapter, self).__init__(context)
        
        self.props = getToolByName(context, 'portal_properties').uwosh_simpleemergency_properties
    
    def get_display_emergency(self):
        #just check if the viewlet is shown
        viewlet = "uwosh.simpleemergency"
        manager = "plone.portaltop"

        storage = getUtility(IViewletSettingsStorage)
        skinname = self.context.getCurrentSkinName()
        hidden = storage.getHidden(manager, skinname)

        return viewlet not in hidden
        
    def set_display_emergency(self, value):
        #just show or hide the viewlet
        viewlet = "uwosh.simpleemergency"
        manager = "plone.portaltop"

        storage = getUtility(IViewletSettingsStorage)
        skinname = self.context.getCurrentSkinName()
        hidden = storage.getHidden(manager, skinname)
        
        if value:
            if viewlet in hidden:
                hidden = tuple(x for x in hidden if x != viewlet)
                storage.setHidden(manager, skinname, hidden)
        else:
            if viewlet not in hidden:
                hidden = hidden + (viewlet,)
                storage.setHidden(manager, skinname, hidden)
        
    display_emergency = property(get_display_emergency, set_display_emergency)
    
    def get_show_on_all_pages(self):
        return self.props.getProperty('show_on_all_pages', False)
        
    def set_show_on_all_pages(self, value):
        self.props.show_on_all_pages = value
        
    show_on_all_pages = property(get_show_on_all_pages, set_show_on_all_pages)
    
    def get_emergency_message(self):
        return self.props.getProperty('emergency_message', '')
    
    def set_emergency_message(self, value):
        if value != self.props.emergency_message:
            self.props.emergency_message = value
            self.props.last_updated = DateTime().pCommonZ() # string representative value
            
    
    emergency_message = property(get_emergency_message, set_emergency_message)
    
    
class EmergencyNotificationConfigurationForm(ControlPanelForm):

    form_fields = form.Fields(ISimpleEmergencySchema)
    form_fields['emergency_message'].custom_widget = WYSIWYGWidget
    
    description = _(u"This is where you can configure Emergency Notification settings.")
    form_name = _(u"UW Oshkosh Emergency Notification Configuration")
    #label = _(u"UW Oshkosh Settings")
    __roles__ = ('Manager', 'uwosh.simpleemergency: Emergency message manager',)
    

    def _on_save(self, data=None):
        super(EmergencyNotificationConfigurationForm, self)._on_save(data)
        notify(SimpleEmergencyModifiedEvent(self.context, self.request))
        