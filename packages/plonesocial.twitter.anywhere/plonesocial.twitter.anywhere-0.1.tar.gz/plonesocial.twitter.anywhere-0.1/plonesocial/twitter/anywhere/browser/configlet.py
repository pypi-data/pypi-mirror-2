from zope.formlib import form
from zope import schema
from zope.component import adapts, queryUtility
from zope.interface import Interface, implements
from plone.app.controlpanel.form import ControlPanelForm
from Products.CMFDefault.formlib.schema import SchemaAdapterBase
from Products.CMFPlone.interfaces import IPloneSiteRoot
from Products.CMFCore.interfaces import IPropertiesTool

from plonesocial.twitter.anywhere import anywhereMessageFactory as _

class IAnywhereConfiguration(Interface):
    """This interface defines the configlet."""
    api_key = schema.TextLine(title=u"Twitter @Anywhere API key",
                                  required=True)
    linkify_enabled = schema.Bool(title=u"enable auto-linking of @username elements",
                                  default=True,
                                  required=True)
    hovercard_enabled = schema.Bool(title=u"enable Twitter Hovercards on @username",
                                  default=False,
                                  required=True)

class AnywhereControlPanelAdapter(SchemaAdapterBase):

    adapts(IPloneSiteRoot)
    implements(IAnywhereConfiguration)

    def __init__(self, *args, **kwargs):
        super(AnywhereControlPanelAdapter, self).__init__(*args, **kwargs)
        self.props = getattr(queryUtility(IPropertiesTool), 'twitter_anywhere_properties', None)

    def get_api_key(self):
        return self.props.getProperty('api_key', None)

    def set_api_key(self, value):
        self.props.api_key = value

    def get_linkify(self):
        v = self.props.getProperty('linkify_enabled', 'false')
        return v=='true'

    def set_linkify(self, value):
        if value:
            self.props.linkify_enabled = 'true'
        else:
            self.props.linkify_enabled = 'false'

    def get_hovercard(self):
        v = self.props.getProperty('hovercard_enabled', 'false')
        return v=='true'

    def set_hovercard(self, value):
        if value:
            self.props.hovercard_enabled = 'true'
        else:
            self.props.hovercard_enabled = 'false'


    api_key = property(get_api_key, set_api_key)
    linkify_enabled= property(get_linkify, set_linkify)
    hovercard_enabled = property(get_hovercard, set_hovercard)


class AnywhereConfigurationForm(ControlPanelForm):

    form_fields = form.Fields(IAnywhereConfiguration)
    label = _(u"Twitter @Anywhere settings")
    description = _(u"Get your own API key at http://dev.twitter.com/anywhere/")
    form_name = _(u"Twitter @Anywhere Settings")

