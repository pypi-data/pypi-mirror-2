tranchitella.recipe.nose
========================

This recipe creates a nose_ test runner script.

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

defaults

    The defaults option lets you specify testrunner default options.

extra-paths

    One or more extra paths to include in the generated test script.

This is a minimal ''buildout.cfg'' file which creates a test runner::

    [test]
    recipe = tranchitella.recipe.nose
    eggs = myapplication
    defaults =
        --where src
        --with-coverage
        --cover-package myapplication

.. _nose: http://somethingaboutorange.com/mrl/projects/nose/
