eggtestinfo README
==================

Overview
--------

This package is a setuptools plugin:  it adds a file to the generated
``.egg-info`` directory, capturing the information used by the
``setup.py test`` command when running tests.

In particular, the generated file contains the following information:

``test_module``
    The dotted name of a module holding a ``test_suite`` function which
    can be called to compute a ``unittest.TestSuite`` for the package.

    - This option conflicts with ``test_suite``.

    - This option can be overridden on the command line, e.g.::

      $ python setup.py test --test_module=my_package.tests

``test_suite``
    The dotted name of a function  which can be called to compute a
    ``unittest.TestSuite`` for the package.
    
    - This option conflicts with ``test_module``.
    
    - Note that this name does *not* use the same conventions use by other
      setuptools callables:  the function name is appended to the dotted
      name of the module with a dot, rather than a colon.

    - This option can be overridden on the command line, e.g.::

      $ python setup.py test --test_suite=my_package.utils.find_tests

``test_loader``
    A setuptools entry point which, when called, returns an instalance of
    a loader class, suitable for passing as thet ``testLoader`` argument
    to ``unittest.main()``.

    - This option cannot be overridden on the command line;  it can only
      be specified as an argument to ``setup()``.

``tests_require``
    A list of setuptools requirement specifications for packages which
    must be importable when running the tests.

    - This option cannot be overridden on the command line.

Using the Extension
-------------------

The package registers a entrypoint for setuptools' ``egg_info.writers``
group:  it will therefore be used when building egg info in any environment
where it is present on the PYTHONPATH.

To ensure that your packages get the test information recorded, even when
used from an environment where this package is not already installed,
add the following to your call to ``setup()``::

  from setuptools import setup
  setup(name='my_package',
        # ...
        setup_requires=['eggtestinfo'],
        #...
       )

Examples
--------

The following examples show the generated ``test_info.txt`` file for
various sample packages.

- For a package whose tests are finadable by setuptools' default loader, but
  whose tests depend on another package which is not part of the "normal"
  dependencies of the package::

    test_module = None
    test_suite = None
    test_loader = None
    tests_require = another_package

- For a package which has a module, 'tests', which contains a 'test_suite'
  function that returns the test suite for the whole package::

    test_module = my_package.tests
    test_suite = None
    test_loader = None
    tests_require = None

- For a package which has a function, 'find_tests', in its 'utils' module,
  that returns the test suite for the package::

    test_module = None
    test_suite = my_package.utils.find_tests
    test_loader = None
    tests_require = None

- For a package which uses the "skip layers" loader from zope.testing::

    test_module = None
    test_suite = None
    test_loader = zope.testing.testrunner.eggsupport:SkipLayers
    tests_require = zope.testing>=3.7dev
