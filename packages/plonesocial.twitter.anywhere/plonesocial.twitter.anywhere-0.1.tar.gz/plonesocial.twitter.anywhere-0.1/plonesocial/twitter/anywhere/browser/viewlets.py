import simplejson

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets.common import ViewletBase
from Products.CMFCore.utils import getToolByName
from zope.component import queryUtility
from Products.CMFCore.interfaces import IPropertiesTool

TEMPLATE = """\
<script src="http://platform.twitter.com/anywhere.js?id=%(api_key)s&v=%(version)s" 
    type="text/javascript"></script>
<script language="Javascript">    
    var ta_config = %(conf)s;
</script>
"""


class TwitterAnywhereHeadViewlet(ViewletBase):

    version = 1

    def update(self):
        self.props = getattr(queryUtility(IPropertiesTool), 'twitter_anywhere_properties', None)
        
    def render(self):
        """return the script tag with the API key"""
        if self.props is None:
            return u"" # do nothing if property sheet is unavailable
        
        # TODO: render this safer?
        s = {
            'linkify_enabled' : self.props.getProperty("linkify_enabled", "false"),
            'hovercard_enabled' : self.props.getProperty("hovercard_enabled", "false"),
            'follower_buttons' : [],
            'tweet_boxes' : [],
        }
        conf_js = simplejson.dumps(s)
        out = TEMPLATE %(dict(
            conf = conf_js,
            api_key = self.props.getProperty("api_key"),
            version = self.version,
            ))
        return out

        
        
