==================
SharkbyteSSOPlugin
==================

About
=====

This is a PAS Plugin which gets a variable from the request and uses it to
authenticate to the other PAS plugins.

Tested and know to work with LDAPUserFolder

Installation
============

Add this egg in any Zope instance as you prefer.

pip or easy_install
-------------------

With ``easy_install`` / ``setuptools``::

  $ easy_install Products.SharkbyteSSOPlugin

With ``pip``::

  $ pip install Products.SharkbyteSSOPlugin

zc.buildout
-----------

Your Zope app is supposed to be built with `plone.recipe.zope2instance
<http://pypi.python.org/pypi/plone.recipe.zope2instance>`_ recipe. This sample says all::

  [buildout]
  ...
  parts =
      instance
      ...
  ...
  [instance]
  recipe = plone.recipe.zope2instance
  ...
  eggs =
      ...
      Products.SharkbyteSSOPlugin
      ...
  ...

In your PAS or PlonePAS user folder
-----------------------------------

* Add a **SharkbyteSSOPlugin** from the drop down menu

* Click on the **sbs-sso** that has been created and tick the two plugins you want
  it to use.

* By default it uses the ``X_REMOTE_USER`` header, but if you want to change it,
  click on properties and change it.

* If you want it to work with other plugins, you'll have to change the variable
  names the credentials use (ie: user_id).


Credits, copyright and license
==============================

Copyright (c), 2006-2010, Sharkbyte Studios Ltd

Licensed under the GPL.

.. admonition::
   Sharkbyte Studios Limited

   | 0845 22 66 537
   | PO BOX 50372 LONDON W4 5SJ
   | http://www.sharkbyte.co.uk

Developers
----------

* `Ben Mason <mailto:ben_AT_sharkbyte.co.uk>`_: original developer
* `Encolpe Degoute <mailto:encolpe.degoute_AT_free.fr>`_: added IIS challenge
* `Gilles Lenfant <mailto:gilles.lenfant_AT_alterway.fr>`_: eggification
