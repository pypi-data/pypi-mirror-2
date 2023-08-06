.. contents::

Introduction
============

This product change the Plone behavior that manage **portal tabs**. Installing this will change nothing
in your Plone site, but gives you a way (through ZMI) to change the way used for obtaining those links
in Plone *subsites*.

In Plone 4, when a folder is marked as ``INavigationRoot``, the folder become more or less a subsite.

By default, standard portal tabs links are ok (link to the home page, followed by auto-generated tabs taken
loading all first level subsection of the site or subsite), but if you customized portal tabs adding new ones
you will see those new tabs also in subsites.

Also, you have no way to see custom portal tabs links only in the subsite.

Customize your tabs
===================

This product will change this behavior. If you want to have some additional portal tabs in a folder with id
"*my-subsection*" that you marked with ``INavigationRoot``, you simply need to add to the **portal_actions**
tool a new "*CMF Action Category*" with id "*portal_``my_subsection``_tabs*" (folder id will be normalized
to use only simple character and "_" character).

Will be kept this order:

* Plone site default portal tab 1
* Plone site default portal tab 2
* ...
* Subsite portal tab 1
* Subsite portal tab 2
* ...
* Auto generated tabs (if enabled)

Dont' want to inherit?
----------------------

If you don't want to see also portal tabs defined for the Plone site, simply add a ZMI boolean property
in your CMF Action Category, naming it ``block_inherit`` and putting its values to ``True``.
In this way you'll see only tabs defined in the subsite.

If you don't provide this property (default) or put it to false, you will continue seeing also portal tab links.

Additional products
===================

About subsites
--------------

This product has been develop for additional needs of `redturtle.subsites`__, but can be used outside the
project itself.

__ http://plone.org/products/redturtle.subsites

Don't want to use ZMI?
----------------------

You can rely on `collective.portaltabs`__ if you want a user friendly interface for managing portal tabs
(of the root site or subsites) from Plone.

__ http://plone.org/products/collective.portaltabs

Credits
=======

Developed with the support of `Rete Civica Mo-Net - Comune di Modena`__;
Rete Civica Mo-Net supports the `PloneGov initiative`__.

.. image:: http://www.comune.modena.it/grafica/logoComune/logoComunexweb.jpg
   :alt: Comune di Modena - logo

__ http://www.comune.modena.it/
__ http://www.plonegov.it/

Authors
=======

This product was developed by RedTurtle Technology team.

.. image:: http://www.redturtle.net/redturtle_banner.png
   :alt: RedTurtle Technology Site
   :target: http://www.redturtle.net/




