Introduction
============

The HSCustom theme was originally created for my band. The band died but the theme lives on!

Installation
------------

Add ``Products.HSCustom`` to the ``eggs`` parameter of your
``plone.recipe.zope2instance`` section::

    [plone]
    recipe = plone.recipe.zope2instance
    ...
    eggs =
        ...
        Products.HSCustom

Now run buildout, restart Plone, and install the theme in Site Setup ->
Add-ons.

.. Note::

    This theme generally looks terrible; it's just for fun (and the Plone 4
    support needs some work.)

