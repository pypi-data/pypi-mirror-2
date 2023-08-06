jsb.recipe.jsonbot
==================

`jsb.recipe.jsonbot` provides a series of `zc.buildout <http://pypi.python.org/pypi/zc.buildout>`_
recipes to help with `JSONBOT <http://code.google.com/p/jsb/>`_
development. It is inspired by `rod.recipe.appengine <http://pypi.python.org/pypi/rod.recipe.appengine>`_,
but using a different layout and with extended functionalities. It is also
split in different recipes. Currently `jsb.recipe.jsonbot` has 1 recipe:

:jsb.recipe.jsonbot\:install: Downloads libraries from PyPi and installs in
    the app directory.

Source code and issue tracker can be found at
`http://code.google.com/p/jsb-recipe/ <http://code.google.com/p/jsb-recipe/>`_.

jsb.recipe.jsonbot:install
------------------------

Installs a JSONBOT in the buildout directory.

This recipe extends `zc.recipe.egg.Scripts <http://pypi.python.org/pypi/zc.recipe.egg>`_,
so all the options from that recipe are also valid.

Options
~~~~~~~

:sdk-directory: Path to the App Engine SDK directory. It can be an
    absolute path or a reference to the `appfy.recipe.gae:sdk` destination
    option. Default is `${buildout:parts-directory}/jsonbot`.

Example
~~~~~~~

::

  [jsonbot]
  # Installs appcfg, dev_appserver and python executables in the bin directory.
  recipe = jsb.recipe.jsonbot:install
  sdk-directory = ${gae_sdk:destination}/jsonbot
