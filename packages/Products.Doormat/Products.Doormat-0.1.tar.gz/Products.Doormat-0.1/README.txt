Introduction
============

A doormat is a large collection of links which are presented in a structured
way. (See examples_ of doormats.) 

This product adds a couple of content types (Archetypes), which are used to
create a structure which is used for generating a doormat. A viewlet on this
doormat is placed in the Plone footer. The links in the Doormat are managed as
content, making the Doormat more flexible than a sitemap.  It's also possible
to add external links.


Getting started
===============

After installing the product in your site, you can add a "Doormat" item to your
Plone site. (Exclude it from navigation using the "Settings" tab.) Inside it,
you can create a hierarchical structure of Columns, Sections and links (both
internal and external). 

The Doormat will look like this::

    +-- Doormat -----------------------------------------+
    |                                                    |
    |  +-- Column 1 ----------+  + Column 2 -----------+ |
    |  |                      |  |                     | |
    |  |  +-- Section 1 ----+ |  | +-- Section 1 ----+ | |
    |  |  |                 | |  | |                 | | |
    |  |  |  +-- Link 1 --+ | |  | |  +-- Link 1 --+ | | |
    |  |  |  +------------+ | |  | |  +------------+ | | |
    |  |  |                 | |  | |                 | | |
    |  |  |  +-- Link 2 --+ | |  | |  +-- Link 2 --+ | | |
    |  |  |  +------------+ | |  | |  +------------+ | | |
    |  |  |                 | |  | |                 | | |
    |  |  +-----------------+ |  | +-----------------+ | |
    |  |                      |  |                     | |
    |  +----------------------+  +---------------------+ |
    |                                                    |
    +----------------------------------------------------+


Simple configuration
====================

There's a field `showTitle` on the folderish types (Doormat, Column and
Section) which allows content managers to decide if the item's title should be
displayed in the doormat.


Moving the doormat
==================

By default, the doormat viewlet is placed in the `plone.portalfooter` viewlet
manager. It's easy to modify this in an add-on product, so the doormat will
display below the global navigation (portal tabs), or anywhere else in the
site.


Caveats
=======

The viewlet does a catalog lookup for the `Doormat` portal type. If you have
more than one object of this type (nothing stops you), it will use the oldest
one.


Dependencies / Requirements
===========================

The product works on:

    * Plone 3
    * Plone 4


.. _examples: http://www.welie.com/patterns/showPattern.php?patternID=doormat

