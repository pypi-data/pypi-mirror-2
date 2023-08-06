Introduction
============

.. contents:: **Table of contents**

When you need this
------------------

You need this product when you want to give to your non-technical users the ability to
manage the *portal tabs* section of your Plone site.

Going deeply:

* you don't want that your users (even if Manager) go to ZMI
* you users don't know nothing about TAL and python, and commonly want only to add static
  links to the site
* your additional tab don't need advanced features like condition for being seen, or permissions

When you don't need this
------------------------

If you only need to port into Plone the "*portal_action*" tool customization, you will find
a great product in `quintagroup.plonetabs`__

__ http://pypi.python.org/pypi/quintagroup.plonetabs/

How to use
==========

First note
----------

This product only manage portal tabs that are not automatically generated from Plone. For this
reason, a warning message is displayed if the "*Automatically generate tabs*" option is selected
in the "*Navigation settings*" panel.

Handling tabs
-------------

From the "*Site Setup*" panel, go to the new "*Manage portal tabs*" link you'll find after the
product installation.

.. image:: http://keul.it/images/plone/collective.portaltabs-0.1.0a-1.png
   :alt: View of the Site Setup panel

The "*Portal Tabs settings*" view is composed by two section; the first one for make changes to
existing tabs (and also order and delete them), and the second for adding new tabs.

.. image:: http://keul.it/images/plone/collective.portaltabs-0.1.0a-2.png
   :alt: Manage portal tabs panel view

Newly created tab only need two kind of information: the name of the tab to be displayed (title)
and the URL. When creating a tab you can also handle the id of the tab, or this will be
automatically generated.

What I can write inside an URL section?
---------------------------------------

The product try to hide some of the too-technical feature you have available in the ZMI
portal_actions tool management, however all features are still there.

* to create a link to something, just type the link (e.g: "http://foo.org")
* TAL espression are still available, but you need to start them with a "*tal:*"
* inside an URL, you can still use expressions in the normal form "${foo1/foo2/...}"

Manage additional actions categories
------------------------------------

You can use collective.portaltabs to handle also others than "*portal_tabs*". To do this you
need to go to ZMI, in the "*portal_properties*" tool and change the "*portaltabs_settings*".

In the "*manageable_categories*" you can add additional entries::

    portal_tabs|Portal tabs
    foo_tabs|My special tabs 

All entries are if the form "actions_id|Title to be displayed" and the *action_id*
action category *must* be exists.
Going back to the "*Portal Tabs settings*" make possible to handle also those new actions

.. image:: http://keul.it/images/plone/collective.portaltabs-0.1.0a-3.png
   :alt: Multiple CMF Category panel

TODO
====

* Simplify creation of tabs that simply are links to site contents
* Make possible for non-Manager users to handle tabs
* Error checking
* Block users from creating TAL/Python expression if you don't want
* Tests

Bug report and feature request
==============================

Please, go to the `product's issue tracker`__ on plone.org website.

__ http://plone.org/products/collective.portaltabs/issues/

Authors
=======

This product was developed by RedTurtle Technology team.

.. image:: http://www.redturtle.net/redturtle_banner.png
   :alt: RedTurtle Technology Site
   :target: http://www.redturtle.net/

