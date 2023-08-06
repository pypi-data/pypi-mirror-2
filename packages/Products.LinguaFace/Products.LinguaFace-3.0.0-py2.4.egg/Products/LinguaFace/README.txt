===================
Products.LinguaFace
===================


About
=====

LinguaFace : A product provinding an alternate view and behaviour for LinguaPlone

Features:

* Neutral contents is now visible in all the translations of its parent folder
* Copy/pase, cut/paste, delete now acts on all the translations of a content
* Workflow is optionally (in the ZMI) synchronised between the translations of a content

Dependencies:

* LinguaPlone 3.x
* Plone 3.1.x
* Zope 2.10.4

**Important**

After installation your portal catalog will be cleaned because a new index & new
metadata are created You need to rebuild it. See "Install" below.

Install
=======

1. Copy the directory of this product in your product's directory of your Zope
   instance.

2. Go to the Plone ControlPanel > Addon Products, and install LinguaFace.

3. Go to the ZMI > your plone site > portal_catalog, Click on Advanced tab,
   Click on "Clear and rebuild" to rebuild your site catalog


How does it work?
=================

LinguaFace overloads a subset of LinguaPlone's and Archetype's templates.  It
also adds a new extended path index which is the path of the canonical
translation.

Known problems when displaying neutral contents from all translated folders:

- getObjPositionInParent has no more sense, so it will be useful to change the
  default sort_on parameter for navtree and folder views.
  TODO: an option in tool to change the ``sort_on`` parameter

- In some situations, you could have some surprises when using the
  getFolderContents method, to retrieve the standard behavior just add
  ``contentFilter['getPhysicalTree'] = True``.

Download
========

* On Plone.org : http://plone.org/products/linguaface

* On SF SVN ::

     $ svn co \
     > https://ingeniweb.svn.sourceforge.net/svnroot/ingeniweb/Products.LinguaFace/trunk \
     > Products.LinguaFace

Copyright and License
=====================

Copyright (c) 2006 Ingeniweb SAS

This software is subject to the provisions of the GNU General Public
License, Version 2.0 (GPL).  A copy of the GPL should accompany this
distribution.  THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL
EXPRESS OR IMPLIED WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF TITLE, MERCHANTABILITY,
AGAINST INFRINGEMENT, AND FITNESS FOR A PARTICULAR PURPOSE

More details in the ``LICENSE`` file included in this package.

Credits
=======

The Ingeniweb team <http://www.ingeniweb.com> (c) 2006

Support
=======

Mail to Ingeniweb support <mailto:support@ingeniweb.com>

Donations are welcome for new features <http://sourceforge.net/project/project_donations.php?group_id=74634>
