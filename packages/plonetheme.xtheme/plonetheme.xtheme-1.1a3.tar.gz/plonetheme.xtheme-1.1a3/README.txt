Introduction
============

A theme implementing an elegant, original and monochrome-like design with 
rounded corners.


Installation
============

Assuming that you are using zc.buildout and the plone.recipe.zope2instance
recipe to manage your project, proceed this way:

* Add plonetheme.xtheme to the list of eggs to install, e.g.:

::

  [buildout]
   ...
   eggs =
       ...
       plonetheme.xtheme

* Re-run buildout, e.g. with:

::

  $ ./bin/buildout


Then you can install the product into your Plone site from the Plone control
panel.

In Plone 4, if you uninstall plonetheme.xtheme you will notice that the site
will start looking very raw in style. This is because 'Plone Default' is set as
default skin after uninstallation. To change the default skin you need to go to
the Themes tool in the control panel and select a default skin different from
'Plone Default'.
