Introduction
============

This is a Plone product that provides a way to select a theme for a specific 
section of your site. The theme will by applied at publication time using a 
custom header in conjuction with deliverance as proxy.

This product use the `plone.app.registry`_ packages to provide a simlpe way to 
add new entries in the product configuration for custom products using 
genericsetup.

.. contents:: Table of contents

Instalation
===========

Using Buildout
--------------

* Add ``yaco.deliverancethemeselector`` to the list of eggs to install, e.g.::

    [buildout]
    ...
    eggs =
        ...
        yaco.deliverancethemeselector

* Tell the plone.recipe.zope2instance recipe to install a ZCML slug::

    [instance]
    recipe = plone.recipe.zope2instance
    ...
    zcml =
        ...
        yaco.deliverancethemeselector

* Re-run buildout, e.g. with::

    $ ./bin/buildout


Dependencies
------------

 * `plone.app.registry`_

Repository
----------

svn repository 
`http://svn.plone.org/svn/collective <http://svn.plone.org/svn/collective>`_

Sponsorship
===========

This product was sponsored by "Universidad de Extremadura" (`www.unex.es`_)
and Yaco Sistemas (`www.yaco.es`_)


.. _plone.app.registry: http://pypi.python.org/pypi/plone.app.registry
.. _www.yaco.es: http:///www.yaco.es
.. _www.unex.es: http://www.unex.es


