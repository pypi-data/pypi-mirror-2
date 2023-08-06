================
 For Developers
================

If you would like to contribute to virtualenvwrapper.project directly,
these instructions should help you get started.  Patches, bug reports,
and feature requests are all welcome through the `BitBucket site
<http://bitbucket.org/dhellmann/virtualenvwrapper.project/>`__.
Contributions in the form of patches or pull requests are easier to
integrate and will receive priority attention.

.. note::

  Before contributing new features to virtualenvwrapper.project,
  please consider whether they should be implemented as an extension
  instead.

Building Documentation
======================

The documentation for virtualenvwrapper.project is written in
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

The test suite for virtualenvwrapper.project uses `shunit2
<http://shunit2.googlecode.com/>`_.  To run the tests under bash, sh,
and zsh, use ``make test``.  To add new tests, modify or create an
appropriate script in the ``tests`` directory.

Creating a New Template
=======================

virtualenvwrapper.project templates work like `virtualenvwrapper
plugins
<http://www.doughellmann.com/docs/virtualenvwrapper/plugins.html>`__.
The *entry point* group name is
``virtualenvwrapper.project.template``.  Configure your entry point to
refer to a function that will **run** (source hooks are not supported
for templates).

The argument to the template function is the name of the project being
created.  The current working directory is the directory created to
hold the project files (``$PROJECT_HOME/$envname``).

Help Text
---------

One difference between project templates and other virtualenvwrapper
extensions is that only the templates specified by the user are run.
The ``mkproject`` command has a help option to give the user a list of
the available templates.  The names are taken from the registered
entry point names, and the descriptions are taken from the docstrings
for the template functions.
