tranchitella.recipe.testrunner
==============================

This recipe creates a zope.testing_ test runner script which supports code
coverage analysis using the coverage_ python library.

Usage
-----

The recipe supports the following options:

eggs

    The eggs option specified a list of eggs to test given as one ore more
    setuptools requirement strings.  Each string must be given on a separate
    line.

script-name

    The script option gives the name of the script to generate, in the buildout
    bin directory.  Of the option isn't used, the part name will be used.

extra-paths

    One or more extra paths to include in the generated test script.

defaults

    The defaults option lets you specify testrunner default options.

working-directory

    The working-directory option lets to specify a directory where the tests
    will run. The testrunner will change to this directory when run. If the
    working directory is the empty string or not specified at all, the recipe
    will create a working directory among the parts.

environment

    A set of environment variables that should be exported before starting the
    tests.

initialization

    Provide initialization code to run before running tests.

relative-paths

    Use egg, test, and working-directory paths relative to the test script.

This is a minimal ''buildout.cfg'' file which creates a test runner::

    [test]
    recipe = tranchitella.recipe.testrunner
    eggs = myapplication

    [test-coverage]
    recipe = tranchitella.recipe.testrunner
    eggs = myapplication
    defaults = ['--coverage-module', 'myapplication', '--coverage-branch']

.. _coverage: http://nedbatchelder.com/code/modules/rees-coverage.html
.. _zope.testing: http://pypi.python.org/pypi/zope.testing
