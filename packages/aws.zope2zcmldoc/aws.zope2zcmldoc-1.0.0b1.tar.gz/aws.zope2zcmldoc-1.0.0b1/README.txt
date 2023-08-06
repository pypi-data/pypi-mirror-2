================
aws.zope2zcmldoc
================

A new Zope 2 control panel that renders the live ZCML documentation, this means
the ZCML that is installed in your Zope instance. Read more details and see some
screenshots in `this blog post
<http://glenfant.wordpress.com/2011/04/20/zcml-wadda-want-a-live-zcml-doc/>`_.

Intended audience
=================

This component is clearly dedicated to Zope developers and integrators. This
component does not provide features for the end user.

Works with
==========

``aws.zope2zcmldoc`` has been tested with Zope 2.10, Zope 2.11, and Zope
2.12. It may or may not work with earlier or later versions of Zope.

Tests reports with other Zope versions, and related contributions are welcome
(note that supporting Zope 2.8 and earlier versions is not considered).

Installation
============

With ``zc.buildout`` and ``plone.recipe.zope2instance``, you just need to add
this in your ``buildout.cfg`` file ::

  ...
  [instance]
  recipe = plone.recipe.zope2instance
  ...
  eggs =
      ...
      aws.zope2zcmldoc
      ...
  zcml =
      ...
      aws.zope2zcmldoc
      ...

Start your Zope instance, open a browser in your Zope root as Manager and type
in your address bar: http://<your-zope-root>/@@install-aws-zope2zcmldoc

Now go to the Zope Control Panel and learn the various ZCML namespaces, elements
and attributes.

Uninstallation
==============

Before removing the ``aws.zope2zcmldoc`` from your ``buildout.cfg`` and
rebuilding your instance, you may want to remove the control panel entry.

Removing the Control Panel entry is not essential, but if you don't do this, a
slate entry will be left in the Zope Control Panel of your Zope instance.

Start your Zope instance, open a browser in your Zope root as Manager and type
in your address bar: http://<your-zope-root>/@@uninstall-aws-zope2zcmldoc

License
=======

This software is licensed under GNU GPL available here:
http://www.gnu.org/licenses/gpl.html

Some URLs
=========

On Pypi:
   http://pypi.python.org/pypi/aws.zope2zcmldoc

Subversion repository:
   https://svn.plone.org/svn/collective/aws.zope2zcmldoc/

Contributors
============

* `Gilles Lenfant <gilles.lenfant@-NO-SPAM-alterway.fr>`_

Sponsored by Alter Way
======================

http://www.alterway.fr
