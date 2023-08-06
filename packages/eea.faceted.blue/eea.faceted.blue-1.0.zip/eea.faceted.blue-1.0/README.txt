Introduction
============

This package applies a blue color theme to the eea.facetednavigation interface.

Three CSS files are used:

* view.css - always loaded, contains CSS overrides for the facetednavigation
  styles displayed on view;

* edit.css - loaded for the configuration page;

* js.css - always loaded, contains JavaScript and plugins overrides.

Replacement images are also provided (used for loading animations and
placeholder indicators on the configuration page)

The CSS overrides work by simply providing a more exact selector for
the elements. This is accomplished by placing `div` in front of the
default facetednavigation selector, e.g.:

::

    div .tags-cloud li {
      color: #CDE0EF;
    }

Installation
============

If you are using zc.buildout and the plone.recipe.zope2instance
recipe to manage your project, you can do this:

* Add ``eea.faceted.blue`` to the list of eggs to install, e.g.:

::

    [buildout]
    ...
    eggs =
        ...
        eea.faceted.blue


* Tell the plone.recipe.zope2instance recipe to install a ZCML slug:

::

    [instance]
    recipe = plone.recipe.zope2instance
    ...
    zcml =
        eea.faceted.blue

* Re-run buildout, e.g. with:

    $ ./bin/buildout

