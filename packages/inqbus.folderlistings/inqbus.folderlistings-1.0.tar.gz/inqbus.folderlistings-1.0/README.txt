Introduction
============

inqbus.folderlistings provides a folderlisting view for collections
and folders. With this view you have the possibility to sort on title,
author, type and modificationdate like in a databrowser.

Installing
==========

To install it, just add it to your buildout::

    [instance]
    eggs = inqbus.folderlistings
    ...
    zcml = inqbus.folderlistings
    
and run ''bin/buildout'' from your plone root directory.

Features planed for the next version
====================================

* change the sortorder to ascending/descending via click on the little
  arrows
* batching the items to a configurable amount

Copyright and Credits
=====================

The Author of inqbus.folderlistings: Max Brauer (max.brauer@inqbus.de)