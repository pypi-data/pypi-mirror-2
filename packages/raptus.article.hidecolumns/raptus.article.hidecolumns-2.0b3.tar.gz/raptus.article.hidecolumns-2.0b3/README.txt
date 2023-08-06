Introduction
============

Article gets the option to hide the left or the right column or both.

Following features for raptus.article are provided by this package:

    * Option to hide the portlet columns

Dependencies:

    * raptus.article.core

Installation
============

To install raptus.article.hidecolumns into your Plone instance, locate the file
buildout.cfg in the root of your Plone instance directory on the file system,
and open it in a text editor.

Add the actual raptus.article.hidecolumns add-on to the "eggs" section of
buildout.cfg. Look for the section that looks like this::

    eggs =
        Plone

This section might have additional lines if you have other add-ons already
installed. Just add the raptus.article.hidecolumns on a separate line, like this::

    eggs =
        Plone
        raptus.article.hidecolumns

Note that you have to run buildout like this::

    $ bin/buildout

Then go to the "Add-ons" control panel in Plone as an administrator, and
install or reinstall the "raptus.article.default" product.

Note that if you do not use the raptus.article.default package you have to
include the zcml of raptus.article.hidecolumns either by adding it
to the zcml list in your buildout or by including it in another package's
configure.zcml.

Usage
=====

Edit your article. You will now have two new options in the "settings" tab:

- Hide left portletslot
- Hide right portletslot

If you select them one of them the selected column will be hidden.

Copyright and credits
=====================

raptus.article is copyrighted by raptus_, and licensed under the GPL. 
See LICENSE.txt for details.

.. _raptus: http://raptus.com/ 