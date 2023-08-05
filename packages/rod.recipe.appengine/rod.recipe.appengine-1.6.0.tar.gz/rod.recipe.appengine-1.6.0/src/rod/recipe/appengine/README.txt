A brief documentation
=====================

This recipe takes a number of options:

appengine-lib
    Path to an already installed appengine library

eggs
    List of required eggs

exclude
    A list of basenames to be excluded when setting up the application files,
    e.g. the whole 'tests' directory.

packages
    A list of packages to be included into the zip archive, which will be
    uploaded to the appspot.

patch
    Specifies a patch file for patching the SDK sourcetree. This options is
    not allowed if appengine-lib is specified.

patch-options
    List of patch options separated by blanks. (Default=-p1)

server-script
    The name of the script to run the development server.

src
    The directory which contains the project source files.

url
    The url for fetching the google appengine distribution

use_setuptools_pkg_resources
    Flag whether the recipe shall copy setuptool's pkg_resources.py into the
    app directory rather than writing a dummy version. (Default=False)

zip-name
    The name of the zip archive containing all external packages ready
    to deploy.

zip-packages
    Flag whether external packages shall be zipped into a single zip file.
    (Default=True)


Tests
=====

We will define a buildout template used by the recipe:

    >>> buildout_template = """
    ... [buildout]
    ... develop = %(dev)s
    ... parts = sample
    ...
    ... [sample]
    ... recipe = rod.recipe.appengine
    ... eggs = foo.bar
    ... packages =
    ...     bazpkg
    ...     tinypkg
    ... server-script = dev_appserver
    ... zip-packages = False
    ... exclude = tests
    ... url = http://googleappengine.googlecode.com/files/google_appengine_1.3.2.zip
    ... """

We'll start by creating a buildout:

    >>> import os.path
    >>> import rod.recipe.appengine.tests as tests
    >>> egg_src = os.path.join(os.path.split(tests.__file__)[0], 'foo.bar')
    >>> baz_pkg = os.path.join(os.path.split(tests.__file__)[0], 'bazpkg')
    >>> tiny_pkg = os.path.join(os.path.split(tests.__file__)[0], 'tinypkg')
    >>> write('buildout.cfg', buildout_template %
    ...       {'dev': egg_src+' '+baz_pkg+' '+tiny_pkg})

Running the buildout gives us:

    >>> output = system(buildout)
    >>> if output.endswith("Google App Engine distribution...\n"): True
    ... else: print output
    True

And now we try to run the appserver script:

    >>> print system(os.path.join('bin', 'dev_appserver'))
    <BLANKLINE>
    ...
    Invalid arguments
    <BLANKLINE>

There should be a configuration script in bin as well:

    >>> print system(os.path.join('bin', 'appcfg'))
    Usage: appcfg [options] <action>
    <BLANKLINE>
    ...
    <BLANKLINE>

Let's see if the 'tests' directory has been excluded:

    >>> l = os.listdir(os.sep.join(['parts', 'sample', 'foo', 'bar']))
    >>> assert 'tests' not in l

There should be a baz package within our application directory:

    >>> assert 'baz' in os.listdir(os.sep.join(['parts', 'sample']))

Let's define another buildout template used by the recipe:

    >>> buildout_template = """
    ... [buildout]
    ... develop = %(dev)s
    ... parts = second_sample
    ...
    ... [second_sample]
    ... recipe = rod.recipe.appengine
    ... eggs = foo.bar
    ... use_setuptools_pkg_resources = True
    ... packages =
    ...     bazpkg
    ...     tinypkg
    ... patch = %(patch)s
    ... patch-options = -p1
    ... zip-packages = False
    ... exclude = tests
    ... url = http://googleappengine.googlecode.com/files/google_appengine_1.3.2.zip
    ... """

We'll start by creating a buildout:

    >>> import os.path
    >>> import rod.recipe.appengine.tests as tests
    >>> egg_src = os.path.join(os.path.split(tests.__file__)[0], 'foo.bar')
    >>> baz_pkg = os.path.join(os.path.split(tests.__file__)[0], 'bazpkg')
    >>> tiny_pkg = os.path.join(os.path.split(tests.__file__)[0], 'tinypkg')
    >>> patch = os.path.join(os.path.split(tests.__file__)[0], 'patch.diff')
    >>> write('buildout.cfg', buildout_template %
    ...       {'dev': egg_src+' '+baz_pkg+' '+tiny_pkg, 'patch': patch})

Running the buildout gives us:

    >>> output = system(buildout)
    >>> if output.endswith(
    ...     "patching file lib/patched/patched.txt\n"): True
    ... else: print output
    True

And now we try to run the appserver script:

    >>> print system(os.path.join('bin', 'second_sample'))
    <BLANKLINE>
    ...
    Invalid arguments
    <BLANKLINE>

Let's have a look if all dependent packages are copied into our application
directory: 

    >>> os.path.isfile(os.path.join('parts', 'second_sample', 'tinymodule.py'))
    True
    >>> os.path.isdir(os.path.join('parts', 'second_sample', 'baz'))
    True

Setuptool's original pkg_resources.py file should be copied into our app
directory:

    >>> pkg_resources = os.path.join(
    ...     'parts', 'second_sample', 'pkg_resources.py')
    >>> os.path.isfile(pkg_resources)
    True
    >>> pkg_resources_file = open(pkg_resources, "r")
    >>> pkg_resources_file.read().startswith('def _dummy_func')
    False
    >>> pkg_resources_file.close()

We've configured the recipe to patch the SDK's source tree:

    >>> gae_sdk_root = os.path.join('parts', 'google_appengine')
    >>> patched_dir = os.listdir(os.path.join(gae_sdk_root, 'lib'))
    >>> patched_file = open(
    ...     os.path.join(gae_sdk_root, 'google', 'appengine', 'tools',
    ...                  'dev_appserver.py')).read()[:1300]
    >>> 'patched' in patched_dir
    True
    >>> '# This file is patched by the patch command.' in patched_file
    True
