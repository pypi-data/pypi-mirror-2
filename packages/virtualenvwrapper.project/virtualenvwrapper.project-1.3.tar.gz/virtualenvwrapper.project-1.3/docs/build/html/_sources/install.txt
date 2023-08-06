==============
 Installation
==============

Basic Installation
==================

virtualenvwrapper.project should be installed using pip_::

  $ pip install virtualenvwrapper.project

You will want to install it into the same Python site-packages area
where virtualenvwrapper and virtualenv are located.  You may need
administrative privileges to do that.  Refer to the `virtualenvwrapper
documentation
<http://www.doughellmann.com/docs/virtualenvwrapper/install.html>`__
for configuration instructions for virtualenvwrapper.

.. note::

  virtualenvwrapper.project is loaded into your shell environment when
  virtualenvwrapper is initialized. After installing it, you will need
  to start a new shell or re-source ``virtualenvwrapper.sh`` to cause
  it to be activated for the current shell.

PROJECT_HOME
============

The variable ``PROJECT_HOME`` tells virtualenvwrapper.project where to
place your project working directories.  The variable must be set and
the directory created before :ref:`command-mkproject` is used.

You will want to add a line like::

    export PROJECT_HOME=$HOME/Devel

to your shell startup file.

.. _pip: http://pypi.python.org/pypi/pip
