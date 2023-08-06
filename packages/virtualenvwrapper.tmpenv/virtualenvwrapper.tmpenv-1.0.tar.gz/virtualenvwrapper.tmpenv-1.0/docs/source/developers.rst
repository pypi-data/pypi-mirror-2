================
 For Developers
================

If you would like to contribute to virtualenvwrapper.tmpenv directly,
these instructions should help you get started.  Patches, bug reports,
and feature requests are all welcome through the `BitBucket site
<http://bitbucket.org/dhellmann/virtualenvwrapper.tmpenv/>`__.
Contributions in the form of patches or pull requests are easier to
integrate and will receive priority attention.

.. note::

  Before contributing new features to virtualenvwrapper.tmpenv,
  please consider whether they should be implemented as an extension
  instead.

Building Documentation
======================

The documentation for virtualenvwrapper.tmpenv is written in
reStructuredText and converted to HTML using Sphinx. The build itself
is driven by make.  You will need the following packages in order to
build the docs:

- Sphinx
- docutils

Once all of the tools are installed into a virtualenv using
pip, run ``make html`` to generate the HTML version of the
documentation.

Running Tests
=============

The test suite for virtualenvwrapper.tmpenv uses shunit2_ and tox_.
The shunit2 source is included in the ``tests`` directory, but tox
must be installed separately (``pip install tox``).

To run the tests under bash, zsh, and ksh for Python 2.4 through 2.7,
run ``tox`` from the top level directory of the hg repository.

To run individual test scripts, use a command like::

  $ tox tests/test.sh

To run tests under a single version of Python, specify the appropriate
environment when running tox::

  $ tox -e py27

Combine the two modes to run specific tests with a single version of
Python::

  $ tox -e py27 tests/test.sh

Add new tests by modifying an existing file or creating new script in
the ``tests`` directory.

.. _shunit2: http://shunit2.googlecode.com/

.. _tox: http://codespeak.net/tox
