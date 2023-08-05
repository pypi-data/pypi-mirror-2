# coding=utf-8

"PyEigen is a Python wrapper for the C++ linear algebra library Eigen."

import distutils.ccompiler
import sys
from distutils.core import setup
from distutils.extension import Extension
from glob import glob


EIGEN_PATH = "."


extra_compile_args = []

compiler = distutils.ccompiler.get_default_compiler()
if compiler == "msvc":
    extra_compile_args.append("/EHsc") # Enable C++ exception handling

pyeigen_ext = Extension(
    "pyeigen",
    sources = glob("source/*.cpp") + glob("source/*/*.cpp"),
    include_dirs = [
        "source",               # PyEigen source
        "/usr/include/eigen2",  # Linux include location
        EIGEN_PATH,             # Custom include location
    ],
    extra_compile_args = extra_compile_args,
)

setup(
    name = "PyEigen",
    version = "0.1",
    author = "Jussi Lepistö",
    author_email = "jussi.lepisto@iki.fi",
    url = "http://launchpad.net/pyeigen",
    license = "LICENSE.txt",

    description = __doc__,
    classifiers = [
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: C++",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries",
    ],

    package_dir = {"": "source"},
    ext_modules = [pyeigen_ext],
)
