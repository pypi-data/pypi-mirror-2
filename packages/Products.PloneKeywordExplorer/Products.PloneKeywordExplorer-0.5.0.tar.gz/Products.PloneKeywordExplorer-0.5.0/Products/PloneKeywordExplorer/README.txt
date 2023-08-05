====================
PloneKeywordExplorer
====================

© 2003-2010 Ingeniweb

PloneKeywordExplorer is an alternative to the usual Plone search.  Searches are
restricted to combinations of keywords.

The search is iterative. Keywords can be added and removed from the search at
any time, allowing the user to conveniently explore the document space. The
result set can be narrowed down to a few documents in a few steps.

PloneKeywordExplorer depends on well-chosen keywords, and supports finding
documents that don't have keywords associated. When you click on the [no
keywords], you get a list of all documents that do not have keywords. You can
browse through this list and start annotating your documents.

Requirements
============

Plone 2.1, Plone 2.5 or Plone 3.x


How does it work?
=================

A search form is provided that offers a choice of keywords. These keywords are
chosen from the published documents of your site.  You can select and remove
keywords by clicking on them.


Install
=======

Add ``Products.PloneKeywordExplorer`` to the ``eggs`` list in your
``plone.recipe.zope2instance`` of your ``zc.buildout`` configuration file. Like
this::

  [instance]
  recipe = plone.recipe.zope2instance
  ...
  eggs =
      ...
      Products.PloneKeywordExplorer
      ...

Then install in your Plone site using the ``portal_quickinstaller`` tool or in
the extensions Plone control panel.

* Use the QuickInstaller Tool to install.

Upgrading
=========

.. admonition::
   Warning

   if upgrading from the non-egg distribution of this component (version 0.4 and
   earlier) you will need to delete in ZMI the content of
   ``/Control_Panel/TranslationService`` before restarting your instance.
