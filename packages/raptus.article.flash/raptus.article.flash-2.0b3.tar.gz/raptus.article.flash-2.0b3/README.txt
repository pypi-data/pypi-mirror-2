Introduction
============

Provides support for flash movies

The following features for raptus.article are provided by this package:

Content
-------
    * Flash - add your flash files in an article.

Components
----------
    * Flash (displays flash files contained in the article over the whole width)
    * Flash left (displays flash files contained in the article on the left side)
    * Flash right  (displays flash files contained in the article on the right side) 
    * Flash teaser (displays flash files contained in the article over the whole width and displayed above the columns)

Dependencies
------------
    * hexagonit.swfheader
    * Products.ContentTypeValidator
    * raptus.article.core

Installation
============

To install raptus.article.flash into your Plone instance, locate the file
buildout.cfg in the root of your Plone instance directory on the file system,
and open it in a text editor.

Add the actual raptus.article.flash add-on to the "eggs" section of
buildout.cfg. Look for the section that looks like this::

    eggs =
        Plone

This section might have additional lines if you have other add-ons already
installed. Just add the raptus.article.flash on a separate line, like this::

    eggs =
        Plone
        raptus.article.flash

Note that you have to run buildout like this::

    $ bin/buildout

Then go to the "Add-ons" control panel in Plone as an administrator, and
install or reinstall the "raptus.article.default" product.

Note that if you do not use the raptus.article.default package you have to
include the zcml of raptus.article.flash either by adding it
to the zcml list in your buildout or by including it in another package's
configure.zcml.

Usage
=====

Add flash
---------
You may now add flash files in your article. Click the "Add new" menu and select "Flash" in the pull down menu.
You get the standard plone form to add your flash file. 

Components
----------
Navigate to the "Components" tab of your article, select one of the flash components
and press "save and view". Note that at least one flash file has to be contained
in the article in which this component is active.

Copyright and credits
=====================

raptus.article is copyrighted by `Raptus AG <http://raptus.com>`_ and licensed under the GPL. 
See LICENSE.txt for details.
