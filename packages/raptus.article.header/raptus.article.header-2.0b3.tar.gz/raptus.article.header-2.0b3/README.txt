Introduction
============

Provide header images for article.

The following features for raptus.article are provided by this package:

Content
-------
    * include raptus.header in article

Dependencies
------------
    * raptus.header

Installation
============

To install raptus.article.header into your Plone instance, locate the file
buildout.cfg in the root of your Plone instance directory on the file system,
and open it in a text editor.

Add the actual raptus.article.header add-on to the "eggs" section of
buildout.cfg. Look for the section that looks like this::

    eggs =
        Plone

This section might have additional lines if you have other add-ons already
installed. Just add the raptus.article.header on a separate line, like this::

    eggs =
        Plone
        raptus.article.header

Note that you have to run buildout like this::

    $ bin/buildout

Then go to the "Add-ons" control panel in Plone as an administrator, and
install or reinstall the "raptus.article.default" product.

Note that if you do not use the raptus.article.default package you have to
include the zcml of raptus.article.header either by adding it
to the zcml list in your buildout or by including it in another package's
configure.zcml.

Usage
=====

1.) Add a new Header from the "Add new" dropdown.
This Content will be a folder for your images.

2.) Add a new Image from the "Add new" dropdown.
Now you can add your header image.

Note that you can add more than one image. If there is more than one image, the article
will display one of these by random.

Copyright and credits
=====================

raptus.article is copyrighted by `Raptus AG <http://raptus.com>`_ and licensed under the GPL. 
See LICENSE.txt for details.
