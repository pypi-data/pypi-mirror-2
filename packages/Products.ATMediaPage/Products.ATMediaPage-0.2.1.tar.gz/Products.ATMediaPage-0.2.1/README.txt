Introduction
============

ATMediaPage is a simple and easy to use Plone Page which can contain AT Images with changeable layout.

Installing
==========

This package requires Plone 3.x or later (tested on 3.3.5 and 4.0b3).

Installing without buildout
---------------------------

Install this package in either your system path packages or in the lib/python directory of your Zope instance. You can do this using either easy_install or via the setup.py script.

Installing with buildout
------------------------

If you are using `buildout`_ to manage your instance installing Products.ATMediaPage is even simpler. You can install Products.ATMediaPage by adding it to the eggs line for your instance::

    [instance]
    eggs = Products.ATMediaPage

After updating the configuration you need to run the ''bin/buildout'', which will take care of updating your system.

.. _buildout: http://pypi.python.org/pypi/zc.buildout


Usage
=====

* Add a new MediaPage in the Plone way like a new document.
* Then you can add some Images into the MediaPage like into a folder.
* You can also copy images from anywhere in your Plone site.
* The MediaPage will show the images depended on the layout of the selected page template.
* You can change the layout by choosing another view on display action-list.

Note
----

You must publish the MediaPage and all images inside the MediaPage! If you forget to publish an image it will not show up in the MediaPage!


Copyright and Credits
=====================

The MediaPage was originally developed by Maik Derstappen, Derstappen IT Consulting (maik.derstappen@inqbus.de, http://www.inqbus-hosting.de) and Torsten Hinze alias HiDeVis (info4hidevis@gmx.de), a programmer from near Cologne.

The MediaPage was redesigned by Thomas Massmann (thomas.massmann@inqbus.de).
