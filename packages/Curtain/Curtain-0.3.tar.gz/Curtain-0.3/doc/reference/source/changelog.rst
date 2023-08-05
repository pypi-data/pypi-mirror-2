.. _changelog:

Changelog
-------------------

.. _release_0.3:

0.3
^^^

This release includes 100% coverage by unit testing. In the process, the
following bugs/enhancements have been fixed/produced:

    * version bump
    * documented Location object
    * new _AttributesImpl implementation which uses xmlreader and supports
      namespaces
    * new processors system, implemented through entry points and thus
      extensible
    * processor's static methods are no longer such
    * fixed extra_attrs => _extra_attrs in the Attributes processor and added
      tag() call to fix his working
    * documentation update
    * test system now uses nose

curtain.bfg:
    * now expects cStringIO to be present
    * fixed a bug in module-relative paths
    * added more properties to the TemplateError

.. _release_0.2:

0.2
^^^

Substantially, no new code has been produced/changed during this release; it
has been a release of reorganization for the documentation and general "makeup"
of the project.

    * New XML namespace.
    * New logo.
    * Lots of documentation/layout reorganization and completion.
    * First version uploaded to pypi.

.. _release_0.1:

0.1
^^^

    * Initial release.
