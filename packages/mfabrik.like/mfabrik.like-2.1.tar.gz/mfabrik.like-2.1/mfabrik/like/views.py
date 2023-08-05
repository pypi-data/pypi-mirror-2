"""
    
    Define views used in this add-on.

    http://mfabrik.com

"""

__license__ = "GPL 2"
__copyright__ = "2010 mFabrik Research Oy"
__author__ = "Mikko Ohtamaa <mikko.ohtamaa@mfabrik.com>"
__docformat__ = "epytext"


import Acquisition
from zope.component import getUtility, getMultiAdapter
from Products.Five.browser import BrowserView

try:
    # plone.app.registry 1.0b1
    from plone.app.registry.browser.form import RegistryEditForm
    from plone.app.registry.browser.form import ControlPanelFormWrapper
except ImportError:
    # plone.app.registry 1.0b2+
    from plone.app.registry.browser.controlpanel import RegistryEditForm
    from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
    
    
from mfabrik.like.interfaces import ISettings
from plone.registry.interfaces import IRegistry
from plone.z3cform import layout

class ControlPanelForm(RegistryEditForm):
    schema = ISettings

ControlPanelView = layout.wrap_form(ControlPanelForm, ControlPanelFormWrapper)