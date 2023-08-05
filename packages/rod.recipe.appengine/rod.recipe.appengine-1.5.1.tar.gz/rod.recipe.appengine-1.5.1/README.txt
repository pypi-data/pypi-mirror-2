====================
rod.recipe.appengine
====================

Buildout recipe for setting up a Google App Engine development environment.

The rod.recipe.appengine is a zc.buildout recipe to build, test and deploy
projects for the Google App Engine. It makes it easy to use eggs and resolve
their dependencies automatically.

To be honest, this is a recipe for scrambled eggs. It produces a zip file
containing all configured external packages in a traditional folder hierarchy.


Credits
=======

Thanks to Attila Olah who provided a patch which fixes two issues where the
recipe wasn't able to find the original pkg_resources.py file. He also enabled
the recipe to be used together with distribute as a replacement for setuptools.
