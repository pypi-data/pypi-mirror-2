.. contents:: local

Introduction
-------------

This Plone CMS add-on product adds the standard Facebook Like-button to Plone pages
as a viewlet.

Usage
-----

Add::

        eggs
                ...
                mfabrik.like
                
.. to your buildout.

Rerun buildout.

Restart Plone.

Like it.

Customization
-------------

* Subclass mfabrik.like.viewlets.LikeViewlet

* Override getIFrame(), getStyle() and like.pt

* Use a browser layer specific to your customization add-on product to override the default LikeViewlet

Changing the location
----------------------

You want to do this in your site theming add-on product.

* Use @@manage-viewlets to hide the default instance

* Use ZCML to bind viewlet to a new location
                   
More information
-----------------

* http://developers.facebook.com/docs/reference/plugins/like

Internationalization
--------------------

The product does not contain any user visible texts.

Author
------

`mFabrik Research Oy <mailto:info@mfabrik.com>`_ - Python and Plone professionals for hire.

* `mFabrik web site <http://mfabrik.com>`_ 

* `mFabrik mobile site <http://mfabrik.mobi>`_ 

* `Blog <http://blog.mfabrik.com>`_

* `More about Plone <http://mfabrik.com/technology/technologies/content-management-cms/plone>`_ 

       
      