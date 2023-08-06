Introduction
============

Provides a content flow component which shows the contained articles
like the coverflow used in iTunes.

The following features for raptus.article are provided by this package:

Components
----------
    * Content flow (showing the contained articles like in iTunes)
    * Content flow teaser (showing the contained articles like in iTunes and is displayed above the columns)

Dependencies
------------
    * raptus.contentflow
    * raptus.article.teaser
    * raptus.article.nesting

Installation
============

To install raptus.article.contentflow into your Plone instance, locate the file
buildout.cfg in the root of your Plone instance directory on the file system,
and open it in a text editor.

Add the actual raptus.article.contentflow add-on to the "eggs" section of
buildout.cfg. Look for the section that looks like this::

    eggs =
        Plone

This section might have additional lines if you have other add-ons already
installed. Just add the raptus.article.contentflow on a separate line, like this::

    eggs =
        Plone
        raptus.article.contentflow

Note that you have to run buildout like this::

    $ bin/buildout

Then go to the "Add-ons" control panel in Plone as an administrator, and
install or reinstall the "raptus.article.default" product.

Note that if you do not use the raptus.article.default package you have to
include the zcml of raptus.article.contentflow either by adding it
to the zcml list in your buildout or by including it in another package's
configure.zcml.

Usage
=====

Components
----------
Navigate to the "Components" tab of your article and select one of the content flow
components and press "save and view". Note that at least one article has to be contained
in the article in which this component is active.

Copyright and credits
=====================

raptus.article is copyrighted by `Raptus AG <http://raptus.com>`_ and licensed under the GPL. 
See LICENSE.txt for details.
