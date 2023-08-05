=======
PyEigen
=======

PyEigen is a Python wrapper for the C++ linear algebra library Eigen.

PyEigen is currently considered PRE-ALPHA quality software and has not been
widely tested outside the unit tests. The API is not stable yet and might
change between releases without warning. Testing and all kinds of feedback are
welcome however! Compatibility reports with different operating systems,
compilers and Python versions are especially welcome.

Launchpad project page: 
http://launchpad.net/pyeigen

Development blog:
http://www.brainfold.org/blog


Requirements
============

PyEigen has been tested with Python 2.4, 2.5 and 2.6, although it might work
on even older versions, up to 2.2. Python 3.0 support is coming in a later
release.

Building PyEigen from source requires the `Eigen 2.0 C++ library
<http://eigen.tuxfamily.org/>`_. Tested with 2.0.12.

PyEigen has been tested on the following platforms and compilers:
* Ubuntu Linux 64-bit with GCC 4.4.1
* Windows 7 64-bit with Visual C++ 2008 SP1

PyEigen has been tested with both 32- and 64-bit versions of Python.


Installing
==========

Windows binary releases are available on the `SourceForge.net project
page <http://sourceforge.net/projects/pyeigen/>`_.

The C++ compiler has to find the Eigen headers, so they should be placed on
the include path. You will also need the Python headers to build
any Python extensions.

On Unix-like systems, it's probably enough to install the Eigen and Python
packages using your package manager. For example, on Ubuntu you need the
libeigen2-dev and python-dev packages. 

On Windows, you can either place the Eigen directory (the
one with the Core header) under the PyEigen root directory or point EIGEN_PATH
in setup.py to your eigen directory (the one with Eigen/Core). For example,
if you unpacked eigen to C:\eigen-2.0.12, set EIGEN_PATH = "C:\\eigen-2.0.12".
The Python headers come with your Python installation and are found
automatically.

To build and install PyEigen from source::

  python setup.py install

To build the extension in place without installing::

  python setup.py build_ext -i
  
If you do this, you can use PyEigen by adding pyeigen/source to your
PYTHON_PATH.


Using
=====

PyEigen has no proper documentation yet. For now, to get started:
* See the examples in the examples directory.
* See the tests in the test directory.
* Read docstrings by typing help(pyeigen) or eg. help(pyeigen.Vector3f) in the
  interactive Python prompt.
* See the `Eigen documentation <http://eigen.tuxfamily.org/dox/>`_.


Benchmarks
==========

There are some basic benchmarks in test/benchmark comparing PyEigen with
cgkit 1, cgkit 2, euclid, NumPy and vectypes. Running the benchmarks runs them
for all the available libraries. euclid and vectypes are included, the rest
must be installed separately for the tests to run.

If you know of any other solutions PyEigen could/should be tested against,
please let me know.


Support
=======

If you find a bug, please fill a bug report at
http://bugs.launchpad.net/pyeigen/

If you have any questions, problems or suggestions, you can send email at
jussi.lepisto@iki.fi.


Credits
=======

Jussi Lepistö
    Primary developer and maintainer

Thanks to all Eigen developers and contributors for the excellent library!


License
-------

PyEigen is licensed under a BSD-style license. See LICENSE.txt.

Eigen is licensed under the LGPL3+. See LICENSE-Eigen.txt.
 
Also see the `Eigen Licensing FAQ
<http://eigen.tuxfamily.org/index.php?title=Licensing_FAQ>`_ for more info.

euclid is Copyright (c) 2006 Alex Holkner
See test/benchmark/euclid.py for license.

vectypes is Copyright (c) 2009 Alex Holkner
See test/benchmark/vectypes.py for license.
