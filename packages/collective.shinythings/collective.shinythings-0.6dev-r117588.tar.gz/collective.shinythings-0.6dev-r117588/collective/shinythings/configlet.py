from collective.shinythings.interfaces import IShinythingsConfiguration
from Products.CMFCore.utils import getToolByName
from plone.app.controlpanel.form import ControlPanelForm
from Products.CMFCore.interfaces import IPropertiesTool
from Products.CMFDefault.formlib.schema import ProxyFieldProperty
from Products.CMFDefault.formlib.schema import SchemaAdapterBase
from Products.CMFPlone.interfaces import IPloneSiteRoot
from zope.component import adapts, getUtility
from zope.formlib.form import FormFields
from zope.i18nmessageid import MessageFactory
from zope.interface import implements

_ = MessageFactory('collective.shinythings')

class ShinythingsControlPanelAdapter(SchemaAdapterBase):
    adapts(IPloneSiteRoot)
    implements(IShinythingsConfiguration)
    
    def __init__(self, context):
        super(ShinythingsControlPanelAdapter, self).__init__(context)
        self.context = getUtility(IPropertiesTool).shinythings_properties

    roundcorners_on = ProxyFieldProperty(IShinythingsConfiguration['roundcorners_on'])
    roundcorners_top_on = ProxyFieldProperty(IShinythingsConfiguration['roundcorners_top_on']) 
    roundcorners_bottom_on = ProxyFieldProperty(IShinythingsConfiguration['roundcorners_bottom_on']) 
    shadow_on = ProxyFieldProperty(IShinythingsConfiguration['shadow_on']) 
    fonteffect_on = ProxyFieldProperty(IShinythingsConfiguration['fonteffect_on']) 
    fadein = ProxyFieldProperty(IShinythingsConfiguration['fadein']) 
    fontfamily = ProxyFieldProperty(IShinythingsConfiguration['fontfamily']) 
    fontfamilysize = ProxyFieldProperty(IShinythingsConfiguration['fontfamilysize']) 
            
class ShinythingsControlPanel(ControlPanelForm):
    form_fields = FormFields(IShinythingsConfiguration)
    label = _(u"Shinythings configuration.")
    description = _(u'Settings to configure shinythings.')
    form_name = _(u'Shinythingssettings')
    def _on_save(self, data=None):
        jsregistry = getToolByName(self.context,
                                   'portal_javascripts')
        jsregistry.cookResources()

