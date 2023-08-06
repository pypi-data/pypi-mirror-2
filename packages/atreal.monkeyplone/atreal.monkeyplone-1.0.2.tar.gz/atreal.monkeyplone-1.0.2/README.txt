.. contents::

Overview
========

atreal.monkeyplone display fullname in portlet review and change security for
cut/copy/paste/delete actions in Plone.


Description
============

Technically
-----------

* it changes the Permission on the tree methods : manage_cutObjects,
  manage_delObjects and manage_pasteObjects of BaseFolderMixin from
  Products.Archetypes.BaseFolder.

* it patches the method _verifyObjectPaste from Products.CMFCore.PortalFolder
  who check the delete permission on parent object.
  
* it applies on actions this modifications.


Functionnally
-------------

 When a user "can add" on a folder, now he can cut and delete his own creation.


Note
====

Use with precaution;)


Authors
=======

|atreal|_

* `atReal Team`_

  - Jean-Nicolas Bes [drjnut]
  - Florent Michon [f10w]

.. |atreal| image:: http://downloads.atreal.net/logos/atreal-logo-48-white-bg.png
.. _atreal: http://www.atreal.net
.. _atReal Team: mailto:contact@atreal.net
