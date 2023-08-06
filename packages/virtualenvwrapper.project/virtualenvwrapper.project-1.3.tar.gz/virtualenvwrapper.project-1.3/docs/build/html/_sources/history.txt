=================
 Release History
=================

1.3

  - Redo the packaging for the documentation.
  - Change the location where hooks are created for new projects to
    use ``VIRTUALENVWRAPPER_HOOK_DIR`` instead of ``WORKON_HOME``.

1.2

  - Add :ref:`command-cdproject`.
  - Convert tests to run under tox.

1.1

  - Use our remembered version of python to generate the help text in
    ``mkproject`` so they only see templates installed
    correctly. (:bbissue:`1`).  Thanks to Damien Lebrun for the patch.
  - Incorporate patch from `pjv <http://bitbucket.org/pjv>`__ for
    :bbissue:`4`.

1.0

  - First public release.
