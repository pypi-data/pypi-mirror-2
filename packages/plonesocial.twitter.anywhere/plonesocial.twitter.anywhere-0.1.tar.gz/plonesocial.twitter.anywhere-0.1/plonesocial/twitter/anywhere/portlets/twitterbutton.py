import uuid

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


class ITwitterButtonPortlet(IPortletDataProvider):
    """A portlet for showing a follower button bases on Twitter @Anywhere
    """
    follower = schema.TextLine(title=_(u"Twitter account"),
                              description=_(u"specify the twitter account to follow"),
                              required=True)


class Assignment(base.Assignment):
    """Portlet assignment.

    This is what is actually managed through the portlets UI and associated
    with columns.
    """

    implements(ITwitterButtonPortlet)
    
    follower = u"comlounge"

    def __init__(self, follower=u"comlounge"):
        self.follower = follower

    @property
    def title(self):
        """This property is used to give the title of the portlet in the
        "manage portlets" screen.
        """
        return "Twitter Follow button"


class Renderer(base.Renderer):
    """Portlet renderer.

    This is registered in configure.zcml. The referenced page template is
    rendered, and the implicit variable 'view' will refer to an instance
    of this class. Other methods can be added and referenced in the template.
    """

    render = ViewPageTemplateFile('twitterbutton.pt')

    def show(self):
        return True
        
    def follower(self):
        return self.data.follower
        
    def js(self):
        """return a javascript snippet for rendering"""
        
        uid = unicode(uuid.uuid4())
        return u"""<div id="%s"></div>
        <script language="Javascript">
            var f = {
                id: '%s',
                follower: '%s',
            }
            ta_config.follower_buttons.push(f)
        </script>        
        """ %(uid, uid, self.data.follower)


# NOTE: If this portlet does not have any configurable parameters, you can
# inherit from NullAddForm and remove the form_fields variable.

class AddForm(base.AddForm):
    """Portlet add form.

    This is registered in configure.zcml. The form_fields variable tells
    zope.formlib which fields to display. The create() method actually
    constructs the assignment that is being added.
    """
    form_fields = form.Fields(ITwitterButtonPortlet)
    label = _(u"Add an Twitter @Anywhere portlet")
    description = _(u"This portlet shows a Twitter follow button.")

    def create(self, data):
        return Assignment(**data)

class EditForm(base.EditForm):
    form_fields = form.Fields(ITwitterButtonPortlet)
    label = _(u"Edit Twitter @Anywhere portlet")
    description = _(u"This portlet shows a Twitter follow button.")
