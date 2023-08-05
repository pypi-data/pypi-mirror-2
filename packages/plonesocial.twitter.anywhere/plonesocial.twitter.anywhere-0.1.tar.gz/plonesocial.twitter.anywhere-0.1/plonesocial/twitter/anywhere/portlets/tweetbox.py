import uuid
import simplejson

from zope.interface import Interface
from zope.interface import implements

from plone.app.portlets.portlets import base
from plone.memoize.instance import memoize
from plone.portlets.interfaces import IPortletDataProvider

from Products.CMFPlone import PloneMessageFactory as _

from zope import schema
from zope.formlib import form
from zope.component import getMultiAdapter
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName


class ITweetboxPortlet(IPortletDataProvider):
    """A Tweetbox portlet
    """
    
    width = schema.Int(title=_(u"Box Width"),
                              description=_(u"specify the width of the entry box"),
                              default=220,
                              required=True)
    height = schema.Int(title=_(u"Box Height"),
                              description=_(u"specify the height of the entry box"),
                              default=220,
                              required=True)
    label = schema.TextLine(title=_(u"Label"),
                              description=_(u"specify the label above the portlet"),
                              required=False)

    default_content = schema.Text(title=_(u"Default Content of the entry box"),
                              description=_(u"specify hashtags, RTs or something else."),
                              required=False)

    show_counter = schema.Bool(title=_(u"Show the counter"),
                              description=_(u"Uncheck if you don't want the char counter to be visible."),
                              default=True,
                              required=False)

    

class Assignment(base.Assignment):
    """Portlet assignment.

    This is what is actually managed through the portlets UI and associated
    with columns.
    """

    implements(ITweetboxPortlet)
    width = 220
    height = 220
    label = None
    default_content = None
    show_counter = True

    def __init__(self,
            width = 220,
            height = 220,
            label = None,
            default_content = None,
            show_counter = True):
        self.width = width
        self.height = height
        self.label = label
        self.default_content = default_content
        self.show_counter = show_counter

    @property
    def title(self):
        return u"Tweetbox portlet"


class Renderer(base.Renderer):
    """Portlet renderer.
    """

    render = ViewPageTemplateFile('tweetbox.pt')

    def show(self):
        return True
        
    def js(self):
        """return a javascript snippet for rendering"""
        
        uid = unicode(uuid.uuid4())
        conf = {
            'width' : self.data.width,
            'height' : self.data.height,
            'counter' : self.data.show_counter,
        }
        if self.data.label is not None:
            conf['label'] = self.data.label
        if self.data.default_content is not None:
            conf['defaultContent'] = self.data.default_content
            
        conf_js = simplejson.dumps(conf)
            
        return u"""<div id="%s"></div>
        <script language="Javascript">
            var f = {
                id: '%s',
                conf: %s,
            }
            ta_config.tweet_boxes.push(f)
        </script>        
        """ %(uid, uid, conf_js)


class AddForm(base.AddForm):
    """Portlet add form.
    """

    form_fields = form.Fields(ITweetboxPortlet)
    label = _(u"Add a Tweetbox portlet")
    description = _(u"This portlet shows a Twitter entry form.")

    def create(self, data):
        return Assignment(**data)

class EditForm(base.EditForm):
    form_fields = form.Fields(ITweetboxPortlet)
    label = _(u"Edit Tweetbox portlet")
    description = _(u"This portlet shows a Twitter entry form.")
