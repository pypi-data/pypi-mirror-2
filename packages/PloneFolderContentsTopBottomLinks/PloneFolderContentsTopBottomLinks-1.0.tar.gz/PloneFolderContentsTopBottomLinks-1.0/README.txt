=================================
PloneFolderContentsTopBottomLinks
=================================

Patch Plone's folder_contents view to disable the draggable ordering and show
up/down/top/bottom links.

Installation
============

Add package to your instance's eggs and zcml::

    [instance]
    eggs +=
        PloneFolderContentsTopBottomLinks
    zcml +=
        PloneFolderContentsTopBottomLinks
