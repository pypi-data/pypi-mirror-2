.. contents:: :local: 

Introduction
-------------

This Plone CMS add-on product adds the standard Facebook Like-button 
and Like boxes to Plone pages.

Features
---------

There are several kind of like features

* Like box a.k.a. fan box. Enlists clickers as the fan of your Facebook product page.
  This is available as an addable portlet. (This is the modern "Become a fan" button.)
  
* Like button allows users to share the current content item URL in their Facebook news feed.
  This can be enabled on selected content types or pages using Zope marker interfaces.

Other features

* Facebook content is localized by mapping Plone language to Facebook locale (add your own languages to ``locales.py``) 

* Asynchronous Facebook Connect API Javascript loader is used to optimize the page loading time

Installation
-------------

Installing the code
===================

Add the following to your buildout.cfg::

        eggs
                ...
                mfabrik.like
                
.. to your buildout.

Rerun buildout.

Restart Plone.

Enabling Like-button
=======================

Like-button is enabled on normal Page content type by default.

You can edit these settings by going *Site control panel* -> *Facebook Like-button settings*.

You can also explicitly enable Like-button on some content items by applying
``mfabrik.like.interfaces.IFacebookLikeEnabler`` marker interface on them
through Zope Management Interface.

Adding Like box portlet
=======================

* Add Facebook application id to *Site control panel* -> *Facebook Like-button settings*

* Create new portlet

* Add Facebook page id in the portlet settings (this is the long number which you can pick from Facebook page URL) 

* Show either full Like box or just "Become a fan" text

.. note::

        Like box minimum width is 200 px, recommended by Facebook. The height of bare Become a fan box is 64 px.
        With all features on, the height is ~580 px. You can adjust font sizes etc. with your site CSS
        as Like box is rendered using Javascript/FBML, not IFRAME, technology.
        
* http://wiki.developers.facebook.com/index.php/Like_Box       

Plone 3 and beta components
============================

This add-on product uses software components which are not yet officially deployed
for Plone 3 (and maybe never will) like plone.app.registry. To make these components
work correctly you probably need to use "good-py version pindowns" in your
buildout.cfg.

For more information, see

* http://plone.org/products/dexterity/documentation/manual/developer-manual/pre-requisites/buildout-configuration

Example sites
-------------

* `Siida - Sami Museum <http://www.siida.fi>`_

* `Saariselka / North Lapland travel <http://www.saariselka.fi>`_

Customization
-------------

* Subclass viewlet or portlet rendere classes

* Override necessary methods

* Customize template 

* Use a browser layer specific to your customization add-on product to override the default 
  viewlet / portlet renderer

Changing the location of the Like-button viewlet
-------------------------------------------------

You want to do this in your site theming add-on product.

* Use @@manage-viewlets to hide the default instance

* Use ZCML to bind viewlet to a new location

Source code
------------

* http://svn.plone.org/svn/collective/mfabrik.like/trunk
                   
More information
-----------------

* http://developers.facebook.com/docs/reference/plugins/like

Author
------

`mFabrik Research Oy <mailto:info@mfabrik.com>`_ - Python and Plone professionals for hire.

* `mFabrik web site <http://mfabrik.com>`_ 

* `mFabrik mobile site <http://mfabrik.mobi>`_ 

* `Blog <http://blog.mfabrik.com>`_

* `More about Plone <http://mfabrik.com/technology/technologies/content-management-cms/plone>`_ 

       
      