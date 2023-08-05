"""

    Map Plone two letter locale to Facebook locale.

    http://mfabrik.com

"""

__license__ = "GPL 2"
__copyright__ = "2010 mFabrik Research Oy"
__author__ = "Mikko Ohtamaa <mikko.ohtamaa@mfabrik.com>"
__docformat__ = "epytext"

def map_locale(language):
    """ Guess what Facebook locale should be used for Like-button.
    
    http://wiki.developers.facebook.com/index.php/Facebook_Locales
    
    http://wiki.developers.facebook.com/index.php/Like_Box    
    
    @param language: two letter or four letter language code
    
    @return: facebook locale string to be used for Like-button
    """
    
    # We have plentiful list of choices here...
    
    if language.startswith("fi"):
        return "fi_FI"
    else:
        return "en_US"
        