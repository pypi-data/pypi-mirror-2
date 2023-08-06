Kurzfile
========

A Python package for handling Kurzweil K-series synthesizer object files.

Currently this provides classes and functions to parse and represent ``.KRZ``,
``.K25`` and ``.K26`` files and a script to list all objects contained in such
files.


Requirements
------------

Python >= 2.6 and the setuptools_ package.


Installation
------------

If you have setuptools installed::

    easy_install kurzfile

or, download the source distribution_, unpack the Zip/TGZ archive, change
into the kurzfile-X.Y directory and run::

    python setup.py


Usage
-----

Run ``"k2list -h"`` to get a command line syntax summary and a list of supported
options.

To create a CSV listing of all objects in all KRZ/K25/K26 files in a directory,
use the following shell command line::

   k2list --csv --output mylisting.csv /path/to/files/*.[Kk]??

If you are using Windows (poor soul!), you have to specify each file separately
on the command line, since the CMD interpreter does not support wildcards.


Limitations
-----------

The 'k2list" script currently works correctly for most K25 and K26 files but
generates errors for some old KRZ files. Remember this is still alpha-quality
software. **Use at your own risk** and run it only on KRZ files for which you
have proper backups!


Share & Enjoy,

Christopher Arndt <chris@chrisarndt.de>


.. _distribution: http://www.python.org/pypi/kurzfile
.. _setuptools: http://www.python.org/pypi/setuptools
