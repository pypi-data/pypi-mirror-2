jspack
======

``jspack`` is a simple and small tool to aggegate javascript files with optional miminization.

The tool allows also:

  * Create initial configuration files from html files
  * Reemplace in html script tags by minimized ones.

The project is open source.

A similar tool is `jstools`_ which do recursive search for the javascript files and also support dependencies.

Requirements
-------------
Python 2.6

For javascript minimization you can use:

  * `jsmin`_ or `slimit`_  (you must install the egg first)
  * Any program which reads the code from stdin and writes to stdout like `yui compressor`_
    or `UglifyJS`_




Install
-------

You can install ``jspack`` like a simple python egg:

  * Using easy_install: ``easy_install jstools``
  * Using pip: ``pip install jstools``
  * If you use buildout, add it to the ``eggs`` list in your ``buildout.cfg``,
    or as a dependency of one of your own packages in ``setup.py``.

The code is available in the `jspack github repo`_

Usage
-----

If you have a config file (test.cfg) like::

    [DEFAULT]
    minimizer = jsmin

    [concatenated.js]
    # yui compressor
    minimizer = inout: java -jar compressor.jar --type js
    # Can be used to replace the js tags
    html = test.html
    files = file/relative/to/root.js
            /absolute/file.js

    [compressed.js]
    minimizer = slimit
    files = file/relative/to/root.js
            js/two.js

    [css/all.css]
    root = css
    minimizer = none
    files = one.css
            two.css


And generates concatenated.js, compressed.js and css/all.css

If root option is not specified, the relative files are considered relative to the config parent directory (test.cfg).

You can use the help::

    $ bin/jspack  --help
    Usage:
    jspack [options] file_or_directory

    Typical Usage:

    1. First create cfg files:
       $ jspack -w htmlfile_or_directory
    2. Now we can edit the jspack.cfg files and customize
    3. Then generate minimized:
       $ jspack cfgfile_or_directory
    4. Last, replace script tags:
       $ jspack -rn cfgfile_or_directory

    Note: 3 and 4 can be summarized which: $ jspack -r cfgfile_or_directory


    Options:
      -h, --help            show this help message and exit
      -w, --write-config    For each FILE.html file write a FILE.jspack.cfg file
                            which later can be used to produce FILE-minimized.js
      -o, --ovewrite-config
                            Overwrite a jspack.cfg file if exists. Use which -w
                            option
      -i INCLUDE, --include-only=INCLUDE
                            When parsing html (to generate a .jspack.cfg file) ,
                            include only javascript files which match this regular
                            expression. Default (?!http), Use  for no restriction
      -s, --allow-strict-mode
                            When concatenate js files, dont't drop 'use strict'
                            lines. Default is remove strip mode
      -n, --no-pack         no packing when using the jspack.cfg. Only usefull
                            with -r option for only replace
      -r, --replace-script-tags
                            Replace the script tags in html files
      -q, --quiet           Supress non error output
      -v, --verbose         Vebose output (debug mode)




Roadmap
-------
- CSS links replacement in html files
- Better documentation
- Tests

Credits
-------
- `Yaco Sistemas`_
- `Distribute`_
- `Buildout`_
- `modern-package-template`_
- `zest.releaser`_

.. _jspack github repo: http://github.com/pcaro/jspack
.. _jstools: http://pypi.python.org/pypi/JSTools/
.. _jsmin: http://pypi.python.org/pypi/jsmin
.. _slimit: http://pypi.python.org/pypi/slimit
.. _yui compressor: http://developer.yahoo.com/yui/compressor/
.. _UglifyJS: http://github.com/mishoo/UglifyJS
.. _Yaco Sistemas: http://www.yaco.es
.. _Buildout: http://www.buildout.org/
.. _Distribute: http://pypi.python.org/pypi/distribute
.. _`modern-package-template`: http://pypi.python.org/pypi/modern-package-template
.. _zest.releaser: http://pypi.python.org/pypi/zest.releaser
