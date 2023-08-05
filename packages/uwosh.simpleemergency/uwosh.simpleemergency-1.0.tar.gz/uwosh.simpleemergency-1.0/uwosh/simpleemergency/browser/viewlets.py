from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets.common import ViewletBase
from zope.component import getMultiAdapter
from Products.CMFCore.utils import getToolByName
from DateTime import DateTime

class SimpleEmergencyViewlet(ViewletBase):
    render = ViewPageTemplateFile('simpleemergency.pt')

    def update(self):
        super(SimpleEmergencyViewlet, self).update()
        context_state = getMultiAdapter((self.context, self.request), name=u'plone_context_state')
        portal_props = getToolByName(self.context, 'portal_properties')
        props = portal_props.uwosh_simpleemergency_properties
        
        self.should_display = True
        
        if not props.getProperty('show_on_all_pages', False):
            #check if they only want it to be shown on the root of the site
            self.should_display = context_state.is_portal_root()
            
        if self.should_display:
            self.message = props.getProperty('emergency_message', '')
        
            site_props = portal_props.site_properties
            last_updated = props.getProperty('last_updated', None)
            try:
                dt = DateTime(last_updated)
                if str(dt.day()) + ", " + str(dt.year()) in last_updated:
                    # originally, this package did not store the complete time and the result looked like 01:07pm Apr 26, 2010
                    # This checks if it actually parses the correct date. If it doesn't, just error out and display the stored time
                    # without formatting...
                    format = site_props.getProperty('localLongTimeFormat', '%I:%M%p %b %d, %Y')
                    self.last_updated = dt.strftime(format)
                else:    
                    raise DateTime.DateTimeError
                    
            except DateTime.DateTimeError:
                self.last_updated = last_updated