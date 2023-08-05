"""

    Facebook like viewlet for Plone.

    http://mfabrik.com

"""

__license__ = "GPL 2"
__copyright__ = "2010 mFabrik Research Oy"
__author__ = "Mikko Ohtamaa <mikko.ohtamaa@mfabrik.com>"
__docformat__ = "epytext"

import urllib

from plone.app.layout.viewlets import common as base

class LikeViewlet(base.ViewletBase):
    """ Add a Like button
    
    http://developers.facebook.com/docs/reference/plugins/like
    """
    
    def contructParameters(self):
        """ Create HTTP GET query parameters send to Facebook used to render the button.
        
        href=http%253A%252F%252Fexample.com%252Fpage%252Fto%252Flike&amp;layout=standard&amp;show_faces=true&amp;width=450&amp;action=like&amp;font&amp;colorscheme=light&amp;height=80
        """
        
       
        context = self.context.aq_inner
        href = context.absolute_url()
        
        params = {
                  "href" : href,
                  "layout" : "standard",
                  "show_faces" : "true",
                  "width" : "450",
                  "height" : "40",
                  "action" : "like",
                  "colorscheme" : "light",                
        }
        
        return params
    
    def getIFrameSource(self):
        """
        @return: <iframe src=""> string
        """
        params = self.contructParameters()
        return "http://www.facebook.com/plugins/like.php" + "?" + urllib.urlencode(params)  


    def getStyle(self):
        """ Construct CSS style for Like-button IFRAME.
        
        Use width and height from contstructParameters()
        
        style="border:none; overflow:hidden; width:450px; height:80px;" 
        
        @return: style="" for <iframe>
        """
        params = self.contructParameters()
        return "margin-left: 10px; border:none; overflow:hidden; width:%spx; height:%spx;" % (params["width"], params["height"]) 
        