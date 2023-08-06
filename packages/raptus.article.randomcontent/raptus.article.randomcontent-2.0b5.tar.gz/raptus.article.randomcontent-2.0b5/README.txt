Introduction
============

Provides a component which displays a random article.

The following features for raptus.article are provided by this package:

Components
----------
    * Random content (Random article with it's image displayed over the whole width)
    * Random content left (Random article with it's image displayed on the left side)
    * Random content right (Random article with it's image displayed on the right side)
    * Random content teaser (Random article with it's image displayed over the whole width and displayed above the columns)

Dependencies
------------
    * raptus.article.nesting

Installation
============

To install raptus.article.randomcontent into your Plone instance, locate the file
buildout.cfg in the root of your Plone instance directory on the file system,
and open it in a text editor.

Add the actual raptus.article.randomcontent add-on to the "eggs" section of
buildout.cfg. Look for the section that looks like this::

    eggs =
        Plone

This section might have additional lines if you have other add-ons already
installed. Just add the raptus.article.randomcontent on a separate line, like this::

    eggs =
        Plone
        raptus.article.randomcontent

Note that you have to run buildout like this::

    $ bin/buildout

Then go to the "Add-ons" control panel in Plone as an administrator, and
install or reinstall the "raptus.article.default" product.

Note that if you do not use the raptus.article.default package you have to
include the zcml of raptus.article.randomcontent either by adding it
to the zcml list in your buildout or by including it in another package's
configure.zcml.

Usage
=====

Components
----------
Navigate to the "Components" tab of your article and select one of the random content
components and press "save and view". Note that at least one article has to be contained
in the article in which this component is active.

Copyright and credits
=====================

raptus.article is copyrighted by `Raptus AG <http://raptus.com>`_ and licensed under the GPL. 
See LICENSE.txt for details.
