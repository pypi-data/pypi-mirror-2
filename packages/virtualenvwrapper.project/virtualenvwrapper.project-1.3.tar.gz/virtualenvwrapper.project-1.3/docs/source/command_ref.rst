.. _command:

===================
 Command Reference
===================

Managing Project Directories
============================

.. _command-mkproject:

mkproject
---------

Create a new virtualenv in the WORKON_HOME and project directory in
PROJECT_HOME.

Syntax::

    mkproject [-t template] [virtualenv_options] ENVNAME

The template option may be repeated to have several templates used to
create a new project.  The templates are applied in the order named on
the command line.  All other options are passed to ``mkvirtualenv`` to
create a virtual environment with the same name as the project.

::

    $ mkproject myproj
    New python executable in myproj/bin/python
    Installing distribute.............................................
    ..................................................................
    ..................................................................
    done.
    Creating /Users/dhellmann/Devel/myproj
    (myproj)$ pwd
    /Users/dhellmann/Devel/myproj
    (myproj)$ echo $VIRTUAL_ENV
    /Users/dhellmann/Envs/myproj
    (myproj)$ 

.. seealso::

  * :ref:`scripts-premkproject`
  * :ref:`scripts-postmkproject`

setvirtualenvproject
--------------------

Bind an existing virtualenv to an existing project.

Syntax::

  setvirtualenvproject [virtualenv_path project_path]

The arguments to ``setvirtualenvproject`` are the full paths to the
virtualenv and project directory.  An association is made so that when
``workon`` activates the virtualenv the project is also activated.

::

    $ mkproject myproj
    New python executable in myproj/bin/python
    Installing distribute.............................................
    ..................................................................
    ..................................................................
    done.
    Creating /Users/dhellmann/Devel/myproj
    (myproj)$ mkvirtualenv myproj_new_libs
    New python executable in myproj/bin/python
    Installing distribute.............................................
    ..................................................................
    ..................................................................
    done.
    Creating /Users/dhellmann/Devel/myproj
    (myproj_new_libs)$ setvirtualenvproject $VIRTUAL_ENV $(pwd)

When no arguments are given, the current virtualenv and current
directory are assumed.

Any number of virtualenvs can refer to the same project directory,
making it easy to switch between versions of Python or other
dependencies for testing.

.. _command-cdproject:

cdproject
---------

Change the current working directory to the one specified as the
project directory for the active virtualenv.

Syntax::

  cdproject

