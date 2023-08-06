Introduction
============

Include plone.app.discussion for article.

The following features for raptus.article are provided by this package:

Content
-------
    * include plone.app.discussion in article

Dependencies
------------
    * plone.app.discussion

Installation
============

Plone 3.x Buildout Installation
-------------------------------

Take a look at http://pypi.python.org/pypi/plone.app.discussion ::

    [buildout]
    ...
    extends =
        ...
        http://good-py.appspot.com/release/plone.app.discussion/1.0b12


Plone 3.x and 4 Buildout Installation
-------------------------------------

To install raptus.article.discussion into your Plone instance, locate the file
buildout.cfg in the root of your Plone instance directory on the file system,
and open it in a text editor.

Add the actual raptus.article.discussion add-on to the "eggs" section of
buildout.cfg. Look for the section that looks like this::

    eggs =
        Plone

This section might have additional lines if you have other add-ons already
installed. Just add the raptus.article.discussion on a separate line, like this::

    eggs =
        Plone
        raptus.article.discussion

Note that you have to run buildout like this::

    $ bin/buildout

Then go to the "Add-ons" control panel in Plone as an administrator, and
install or reinstall the "raptus.article.default" product.

Note that if you do not use the raptus.article.default package you have to
include the zcml of raptus.article.discussion either by adding it
to the zcml list in your buildout or by including it in another package's
configure.zcml.


Copyright and credits
=====================

raptus.article is copyrighted by `Raptus AG <http://raptus.com>`_ and licensed under the GPL. 
See LICENSE.txt for details.
