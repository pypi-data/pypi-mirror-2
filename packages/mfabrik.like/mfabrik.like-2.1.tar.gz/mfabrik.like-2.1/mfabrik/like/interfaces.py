import zope.interface
from zope import schema
from zope.publisher.interfaces.browser import IBrowserRequest

from plone.directives import form
from z3c.form.browser.checkbox import CheckBoxFieldWidget

class IFacebookLikeButtonEnabler(zope.interface.Interface):
    """ Marker interface to explicitly enable Facebook Like-button on some pages """
    
class IAddOnInstalled(IBrowserRequest):
    """ This layer is active when mfabrik.like has been run through portal_quickinstaller """

class INeedFacebookConnect(IBrowserRequest):
    """ This layer is applied on HTTPRequest object in portlet or viewlet update() if Facebook Connect JS must be loaded 
    
    XXX: This approach does not work because viewlets are rendered before portlets and this
    goes for update() method do.
    
    Viewlet architecture is limited piece of shit.
    """


class ISettings(form.Schema):
    """ Define schema for settings of the add-on product """

    like_button = schema.Bool(title=u"Enable IFrame-button", description=u"Enable Like-button on selected content types and marker interface marked pages. This buttons allows visitors to share the Plone content item in their Facebook news feed.", required=False, default=False)
    
    application_id = schema.TextLine(title=u"Facebook application id", description=u"You need to sign in to Facebook developer to receive application id for your site  (for Facebook Connect API only)", required=False)
    
    api_key = schema.TextLine(title=u"Facebook API-key", description=u"CURRENTLY NOT USED", required=False)

#    form.widget(enabled_overrides=CheckBoxFieldWidget)
    content_types = schema.List(title=u"Enabled content types",
                               description=u"On which content types Facebook Like-button should appear. You can also add the button to individual pages by toggling IFacebookLikeEnabler marker interface through ZMI.",
                               required=False, default=["Document"],
                               value_type=schema.Choice(source="mfabrik.like.content_types"),
                               )
