Curtain
=======

Curtain is a simple, very small, compiled-to-python templating language with
just about the same characteristics of TAL, METAL and Zope i18n extensions.

Installation
------------

Curtain is based on setuptools. To install it:

$ ./setup.py install

To test it:

$ ./setup.py test

or, if you want to have a full report with coverage too:

$ easy_install nose coverage
$ easy_install -i http://dist.repoze.org/bfg/current/simple repoze.bfg
$ ./setup.py nosetests --with-coverage --cover-package curtain

To produce the documentation (the first step installs Sphinx, skip it if it's
already installed):

$ easy_install Sphinx
$ ./setup.py build_sphinx --source-dir doc/reference/source \
    --build-dir doc/reference/build

After this, the documentation can be found in doc/reference/build/html.

Changelog
---------

All changelog informations can be found in the compiled documentation or in
doc/reference/source/changelog.rst.
