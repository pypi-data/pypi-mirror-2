Introduction to the Web Services API for Plone
==============================================

The ``wsapi4plone.core`` (also known simply as ``wsapi4plone``) package provides
an XML-RPC API to Plone content and operations. One of the main goals is to
provide a slim, versatile and extensive way to create, read, update and delete
(CRUD) Plone content.  The secondary goal is to provide an interface on which
Plone and other systems can communicate with one another.

There are five known categories that the ``wsapi4plone`` is useful for:

- Cross site communication
- Desktop applications
- Skinning/theming
- Batch processing
- Site migration

The primary focus thus far has been on cross site communication (Plone to
Plone communication), desktop applications (desktop authoring) and site
migration (Plone import/export).

Installation (for zc.buildout)
------------------------------

To install ``wsapi4plone`` simply add the following lines to your Plone instance
declaration. The next time you start Zope the calls will be available. No
further installation is required.
::

    [instance]
    recipe = plone.recipe.zope2instance
    ...
    eggs =
        ...
        wsapi4plone.core
    zcml =
        ...
        wsapi4plone.core
