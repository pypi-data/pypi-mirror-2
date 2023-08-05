from zope.publisher.interfaces.browser import IBrowserRequest

class IAddOnInstalled(IBrowserRequest):
    """ This layer is active when mfabrik.like has been run through portal_quickinstaller """
