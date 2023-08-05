"""
    
    Facebook portlets.

    http://wiki.developers.facebook.com/index.php/Like_Box    
    
"""

__license__ = "GPL 2"
__copyright__ = "2010 mFabrik Research Oy"
__author__ = "Mikko Ohtamaa <mikko.ohtamaa@mfabrik.com>"
__docformat__ = "epytext"


import zope.interface
from zope.interface import Interface
from zope.interface import implements
from zope.component import getUtility, getMultiAdapter
from zope.component.interfaces import ComponentLookupError 

from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider

from zope import schema
from zope.formlib import form
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from Acquisition import aq_inner
from zope.component import getMultiAdapter
from plone.memoize.instance import memoize
from plone.app.portlets.cache import render_cachekey
from plone.registry.interfaces import IRegistry

from mfabrik.like.interfaces import INeedFacebookConnect
from mfabrik.like.interfaces import ISettings, IFacebookLikeButtonEnabler, INeedFacebookConnect


class IFacebookLikeBoxData(IPortletDataProvider):
    """ Settings for Like box portlet.
    """

    become_a_fan = schema.Bool(title=u"Become a fan mode", description=u"Show only become a fan text. Set also connections to 0.", required=True)

    page_id = schema.TextLine(title=u"Facebook page ID", description=u"Facebook page ID Like box clickers become fan of (for Facebook Connect API only)", required=True)

    width = schema.Int(title=u"Width", description=u"In pixels", default=200, required=True)
    
    height = schema.Int(title=u"Height", description=u"In pixels", default=200, required=True)
    
    connections = schema.Int(title=u"Connections", description=u"Number of connections to show", default=8, required=True)
    
    logobar = schema.Bool(title=u"Logobar", description=u"Undocumented by Facebook", required=False)

    stream = schema.Bool(title=u"Stream", description=u"Show mini event stream of the target page", required=False)

    header = schema.Bool(title=u"Header", description=u"Show header", required=False)

    
    #page_title = schema.TextLine(title=u"Facebook page name", description=u"Page name (UNUSED FOR NOW)", required=False)

class FacebookLikeBoxAssignment(base.Assignment):
    """Portlet assignment.

    This is what is actually managed through the portlets UI and associated
    with columns.
    """

    implements(IFacebookLikeBoxData)
    
    def __init__(self, page_id, become_a_fan, width, height, connections, logobar, stream, header):
        # Copy all items from the edit form output to this persistent assignment
        self.page_id = page_id
        self.become_a_fan = become_a_fan
        self.width = width
        self.height = height
        self.connections = connections
        self.logobar = logobar
        self.stream = stream
        self.header = header
    
    @property
    def title(self):
        """This property is used to give the title of the portlet in the
        "manage portlets" screen.
        """
        return u"Facebook Like-box"


class FacebookLikeBoxRenderer(base.Renderer):
    """Portlet renderer.

    This is registered in configure.zcml. The referenced page template is
    rendered, and the implicit variable 'view' will refer to an instance
    of this class. Other methods can be added and referenced in the template.
    """
    render = ViewPageTemplateFile('like-box-connect.pt')

    def update(self):
        # DOES NOT WORK
        # Mark HTTP request so that when viewlets are rendered,
        # necessary viewlets for including Connect Javascript are there
        # zope.interface.alsoProvides(self.request, INeedFacebookConnect)
        self.settings = self.fetchSettings()

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

    @property    
    def available(self):
        return True    

    def getPageId(self):
        """
        @return: Facebook page id which we Like
        """
        return self.data.page_id
    
    def getStream(self):
        """ Is FB stream enabled  
        
        @return: "true" or "false"
        """
        return self.data.stream and "true" or "false"

    def getHeader(self):
        """ Is FB header  
        
        @return: "true" or "false"
        """
        return self.data.header and "true" or "false"
    
    def getHeight(self):
        """ """
        
        if self.data.become_a_fan:
            return 64 # Hardcoded FB value
        else:
            return self.data.height
        
    def getWidth(self):
        """ """
        return self.data.width
    
    def getConnections(self):
        """ """
        return self.data.connections
    
    def getLogobar(self):
        # Convert to text
        return self.data.logobar and "true" or "false" 
    
    def hasAPIData(self):
        """ Is control panel configuration properly done """
        
        # NOTE: looks like no application id or API key is needed for Like Box for now
        return True
        
        #return self.settings.application_id not in ("", None)
           
# NOTE: If this portlet does not have any configurable parameters, you can
# inherit from NullAddForm and remove the form_fields variable.

class FacebookLikeBoxAddForm(base.AddForm):

    form_fields = form.Fields(IFacebookLikeBoxData)
    label = u"Create Facebook Like-box"

    def create(self, data):
        return FacebookLikeBoxAssignment(**data)


class FacebookLikeBoxEditForm(base.EditForm):
    """Portlet edit form.

    This is registered with configure.zcml. The form_fields variable tells
    zope.formlib which fields to display.
    """
    form_fields = form.Fields(IFacebookLikeBoxData)
    label = u"Edit Facebook Like-box"

