
==========
qvikconfig
==========

qvikconfig is a parser of a simple config file syntax called the
qvikconfig format. The basic syntax is 'property = value'. qvikconfig
works with both Python 2.6+ and Python 3.x.


License
=======
qvikconfig is free software under the terms of the GNU General Public
License version 3 (or any later version). The author of qvikconfig is
Niels Serup, contactable at ns@metanohi.org. This is version 0.1.1 of
the program.

Installing
==========
If you have python-setuptools installed, you can just do this::

  $ sudo easy_install qvikconfig

Alternatively, download and extract the gzipped tarball found on this
very page, and then run this::

  $ sudo python setup.py install

The newest version of ``qvikconfig`` is always available at
http://metanohi.org/projects/qvikconfig/ and at the Python
Package Index.

Using
=====
This module has two functions: ``parse`` and ``dump``. ``parse`` is
used to read config files, while ``dump`` is used to write config
files. The basic syntax of config files is ``property = value``. The
complete documentation is included within the qvikconfig library and
can be accessed by executing ``pydoc qvikconfig``.

Tests of qvikconfig config files are located in the ``tests/``
directory of the distribution.
