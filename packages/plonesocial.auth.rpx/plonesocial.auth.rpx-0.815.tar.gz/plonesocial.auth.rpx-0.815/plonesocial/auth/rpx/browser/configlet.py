from zope.formlib import form
from zope import schema
from zope.component import adapts, queryUtility
from zope.interface import Interface, implements
from plone.app.controlpanel.form import ControlPanelForm
from Products.CMFDefault.formlib.schema import SchemaAdapterBase
from Products.CMFPlone.interfaces import IPloneSiteRoot
from Products.CMFCore.interfaces import IPropertiesTool

from plonesocial.auth.rpx import rpxMessageFactory as _

class IRPXConfiguration(Interface):
    """This interface defines the configlet."""
    api_key = schema.TextLine(title=u"RPX API key",
                                  required=True)
    domain = schema.TextLine(title=u"RPX domain",
                                  required=True)


class RPXControlPanelAdapter(SchemaAdapterBase):

    adapts(IPloneSiteRoot)
    implements(IRPXConfiguration)

    def __init__(self, *args, **kwargs):
        super(RPXControlPanelAdapter, self).__init__(*args, **kwargs)
        self.props = getattr(queryUtility(IPropertiesTool), 'rpx_properties', None)

    def get_api_key(self):
        return self.props.getProperty('api_key', None)

    def set_api_key(self, value):
        self.props.api_key = value

    def get_domain(self):
        return self.props.getProperty('domain', None)

    def set_domain(self, value):
        self.props.domain = value

    api_key = property(get_api_key, set_api_key)
    domain = property(get_domain, set_domain)


class RPXConfigurationForm(ControlPanelForm):

    form_fields = form.Fields(IRPXConfiguration)
    label = _(u"RPX settings")
    description = _(u"You can find your RPX settings under your RPX account at http://RPXnow.com")
    form_name = _(u"RPX Settings")

