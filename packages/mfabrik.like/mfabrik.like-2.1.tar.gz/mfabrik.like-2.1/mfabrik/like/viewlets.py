"""

    Facebook like viewlet for Plone.

    http://mfabrik.com

"""

__license__ = "GPL 2"
__copyright__ = "2010 mFabrik Research Oy"
__author__ = "Mikko Ohtamaa <mikko.ohtamaa@mfabrik.com>"
__docformat__ = "epytext"

import urllib

import Acquisition
from zope.component import getUtility, getMultiAdapter
from zope.component.interfaces import ComponentLookupError 

from plone.app.layout.viewlets import common as base
from plone.registry.interfaces import IRegistry


from plone.portlets.interfaces import IPortletRetriever, IPortletManager

from mfabrik.like.interfaces import ISettings, IFacebookLikeButtonEnabler, INeedFacebookConnect
from mfabrik.like.locales import map_locale
from mfabrik.like.portlets import IFacebookLikeBoxData 

# Allow browser to process Connect API after
# everything else is loaded
FB_ASYNC_INIT_CODE="""
<script type="text/javascript">
  window.fbAsyncInit = function() {
    FB.init({appId: '%(app_id)s', status: true, cookie: true,
             xfbml: true});
  };
  var fb_load = function() {
    var e = document.createElement('script'); e.async = true;
    e.src = document.location.protocol +
      '//connect.facebook.net/%(locale)s/all.js';
    document.getElementById('fb-root').appendChild(e);
  };
  jq(window).load(fb_load);
</script>  
"""


class FacebookBaseViewlet(base.ViewletBase):
    """ Base class for different Facebook viewlets """

    
    def fetchSettings(self):
        """ Load Facebook Like-button settings from the registry """
        
    
        try:
    
            # Will raise an exception if plone.app.registry is not quick installed
            registry = getUtility(IRegistry)
    
            settings = registry.forInterface(ISettings)
        except (KeyError, ComponentLookupError), e:
            # Registry schema and actual values do not match
            # Quick installer has not been run or need to rerun 
            # to update registry.xml values to database
            # http://svn.plone.org/svn/plone/plone.registry/trunk/plone/registry/registry.py
            return None
        
        return settings
                
    def update(self):
        
        self.settings = self.fetchSettings()
        if not self.settings:
            # registry is down or missing
            return

    def getCurrentLanguage(self):
        """ What language the user has.
        
        @return: Two letter lang code
        """
    
        context = Acquisition.aq_inner(self.context)
        portal_state = getMultiAdapter((context, self.request), name=u'plone_portal_state')

        current_language = portal_state.language()
    
        return current_language

    def isEnabledOnContent(self):
        """
        @return: True if the current content item supports Like-button
        """
            
        content_types = self.settings.content_types
            
        # Don't assume that all content items would have portal_type attribute
        # available (might be changed in the future / very specialized content)
        current_content_type =  portal_type = getattr(Acquisition.aq_base(self.context), 'portal_type', None)
        
        return current_content_type in content_types
                
        return helper.isLikeButtonVisible()    
    
    def isEnabledByMarkerInterface(self):
        raise NotImplementedError("Subclass must implement")
    
    def isEnabled(self):
        """
        @return: Should this viewlet be rendered on this page.
        """
        raise NotImplementedError("The subclass must implement")

    def render(self):
        """ Render viewlet only if it is enabled.
        
        """
                
        # Perform some condition check
        if self.isEnabled():
            # Call parent method which performs the actual rendering
            return super(FacebookBaseViewlet, self).render()
        else:
            # No output when the viewlet is disabled
            return ""
        
    def getLocale(self):
        """ Get language_COUNTRY locale used to localize Facebook content """
        lang = self.getCurrentLanguage()
        locale = map_locale(lang)
        return locale 

class ConnectFacebookBaseViewlet(FacebookBaseViewlet):
    """ Viewlet which is enabled when Like-button can be rendered using Connect API """ 
    

    def isEnabled(self):
        """ Check whether we have elements on the page needing Connect API loading """
        
        # fuck can't do this fuck fuck fuck
        # return INeedFacebookConnect.providedBy(self.request)
        
        # Hardcoded check if the context has like box portlet active
        
        for column in ["plone.leftcolumn", "plone.rightcolumn"]:
            
            manager = getUtility(IPortletManager, name=column)
            
            retriever = getMultiAdapter((self.context, manager), IPortletRetriever)

            portlets = retriever.getPortlets()

            for portlet in portlets:
                
                # portlet is {'category': 'context', 'assignment': <FacebookLikeBoxAssignment at facebook-like-box>, 'name': u'facebook-like-box', 'key': '/isleofback/sisalto/huvit-ja-harrasteet
                # Identify portlet by interface provided by assignment 
                if IFacebookLikeBoxData.providedBy(portlet["assignment"]):
                    return True
                
        return False                
                

class FacebookLoaderDivViewlet(ConnectFacebookBaseViewlet):
    """
    This hidden div is needed for asynchronous Connect API loading.
    
    It is separate from FacebookConnectJavascriptViewlet because
    you might have several FBML apps on the same page - you need
    to load the hidden div only once.
    
    TODO: Later we want to make this HTTPRequest marker interface
    on render() so that arbitary page elements can toggle the load
    of Facebook Connect (like portlets).
    """
    
            
class FacebookConnectJavascriptViewlet(ConnectFacebookBaseViewlet):
    """ This will render Facebook Javascript load in <head>.
    
    <head> section is retrofitted only if the viewlet is enabled.
    
    """
    
    def getConnectScriptSource(self):
        base = "http://static.ak.connect.facebook.com/connect.php/"        
        return base + self.getLocale()
    
    def getInitScriptTag(self):
        """ Get <script> which boostraps Facebook stuff.
        """
        
        
        data = {
                "app_id" : self.settings.application_id,
                "locale" : self.getLocale()                
        }
        
        return FB_ASYNC_INIT_CODE % data
   
class LikeButtonIFrameViewlet(FacebookBaseViewlet):
    """ Add a Like button using IFRAME
    
    http://developers.facebook.com/docs/reference/plugins/like
    """
    
    def isEnabledByMarkerInterface(self):
        return IFacebookLikeButtonEnabler.providedBy(self.context)
    

    def isEnabled(self):
        
        if not self.settings:
            # Settings not available - user must configure something
            return False
        
        return (self.isEnabledOnContent() or self.isEnabledByMarkerInterface()) and self.settings.like_button

    def contructParameters(self):
        """ Create HTTP GET query parameters send to Facebook used to render the button.
        
        href=http%253A%252F%252Fexample.com%252Fpage%252Fto%252Flike&amp;layout=standard&amp;show_faces=true&amp;width=450&amp;action=like&amp;font&amp;colorscheme=light&amp;height=80
        """
        
       
        context = self.context.aq_inner
        href = context.absolute_url()
        
        locale = self.getLocale()
        
        params = {
                  "href" : href,
                  "locale" : locale,
                  "layout" : "standard",
                  "show_faces" : "false",
                  "width" : "450",
                  "height" : "80",
                  "action" : "like",
                  "colorscheme" : "light",                
        }
        
        return params
    
    def getIFrameSource(self):
        """
        @return: <iframe src=""> string
        """
        params = self.contructParameters()
        return "http://www.facebook.com/plugins/like.php?" + urllib.urlencode(params)  


    def getStyle(self):
        """ Construct CSS style for Like-button IFRAME.
        
        Use width and height from contstructParameters()
        
        style="border:none; overflow:hidden; width:450px; height:80px;" 
        
        @return: style="" for <iframe>
        """
        params = self.contructParameters()
        return "margin-left: 10px; margin-top: 10px; border:none; overflow:hidden; width:%spx; height:%spx;" % (params["width"], params["height"]) 
        

            