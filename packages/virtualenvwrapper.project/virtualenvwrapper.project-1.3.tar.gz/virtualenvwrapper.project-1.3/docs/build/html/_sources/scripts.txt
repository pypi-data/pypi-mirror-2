.. _scripts:

========================
 Per-User Customization
========================

The end-user customization scripts are either *sourced* (allowing them
to modify your shell environment) or *run* as an external program at
the appropriate trigger time.

.. _scripts-premkproject:

premkproject
===============

  :Global/Local: global
  :Argument(s): name of new project
  :Sourced/Run: run

``$WORKON_HOME/premkproject`` is run as an external program after the
virtual environment is created and after the current environment is
switched to point to the new env, but before the new project directory
is created. The current working directory for the script is
``$PROJECT_HOME`` and the name of the new project is passed as an
argument to the script.

.. _scripts-postmkproject:

postmkproject
================

  :Global/Local: global
  :Argument(s): none
  :Sourced/Run: sourced

``$WORKON_HOME/postmkproject`` is sourced after the new environment
and project directories are created and the virtualenv is activated.
The current working directory is the project directory.
