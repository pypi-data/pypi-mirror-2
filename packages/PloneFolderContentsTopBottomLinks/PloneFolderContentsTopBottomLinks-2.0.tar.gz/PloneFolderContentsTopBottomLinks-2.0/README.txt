=================================
PloneFolderContentsTopBottomLinks
=================================

Patch Plone's folder_contents view to disable the draggable ordering and show
up/down/top/bottom links.

Installation
============

Plone 4
-------

Add package to your instance's eggs and zcml::

    [instance]
    eggs +=
        PloneFolderContentsTopBottomLinks

Plone 3.x
---------

For Plone 3.x use PloneFolderContentsTopBottomLinks 1.x::

    [instance]
    eggs +=
        PloneFolderContentsTopBottomLinks
    zcml +=
        PloneFolderContentsTopBottomLinks

    [versions]
    PloneFolderContentsTopBottomLinks = 1.0
