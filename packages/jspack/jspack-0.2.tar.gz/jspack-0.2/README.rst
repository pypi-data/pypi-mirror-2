jspack
======

``jspack`` is a simple and small tool to aggegate javascript files with optional miminization.

The tool allows also:

  * Create initial configuration files from html files
  * Reemplace in html script tags by minimized ones.

The code is open source.
Similar tool (more powerfull) is `jstools`_

Requirements
-------------
Python 2.6

For javascript minimization you can use  `jsmin`_ or `slimit`_



Install
-------

You can install ``jspack`` like a simple python egg:

  * Using easy_install: ``easy_install jstools``
  * Using pip: ``pip install jstools``
  * If you use buildout, add it to the ``eggs`` list in your ``buildout.cfg``,
    or as a dependency of one of your own packages in ``setup.py``.


Usage
-----

If you have a config file (test.cfg) like::

    [DEFAULT]
    compress = true

    [concatenated.js]
    root = /one/path
    compress = true
    files = file/relative/to/root.js
            /absolute/file.js

    [compressed.js]
    root = /another/path
    compress = false
    files = file/relative/to/root.js
            js/two.js


It generates /one/path/concatenated.js and /another/path/compressed.js

If root option is not specified, the relative files are considered relative to the config parent directory (test.cfg).

You can use the help::

    $ bin/jspack  --help
    Usage: jspack [options] file_or_directory

    Options:
      -h, --help            show this help message and exit
      -w, --write-config    For each FILE.html file write a FILE-jspack.cfg file
                            which later can be used to produce FILE-minimized.js
      -o, --ovewrite-config
                            Overwrite a .cfg file if exists
      -i INCLUDE, --include-only=INCLUDE
                            When parsing html, Include only javascript files which
                            match an expresion. Default (?!http), Use  for no
                            restriction
      -r, --replace-script-tags
                            Replace the script tags in html files
      -q, --quiet           Supress non error output


Roadmap
-------
- More documentation
- Support of yahoo miminizer

Credits
-------

- `Distribute`_
- `Buildout`_
- `modern-package-template`_

.. _jstools: http://pypi.python.org/pypi/JSTools/
.. _jsmin: http://pypi.python.org/pypi/jsmin
.. _slimit: http://pypi.python.org/pypi/slimit
.. _Buildout: http://www.buildout.org/
.. _Distribute: http://pypi.python.org/pypi/distribute
.. _`modern-package-template`: http://pypi.python.org/pypi/modern-package-template
