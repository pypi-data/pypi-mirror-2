=========================
collective.folderposition
=========================

Extended ordering controls for folder contents.

Installation
============

Plone 4
-------

Add package to your instance's eggs::

    [instance]
    eggs +=
        collective.folderposition

Plone 3.x
---------

Without z3c.autoinclude, you must add the package to both eggs and zcml::

    [instance]
    eggs +=
        collective.folderposition
    zcml +=
        collective.folderposition
