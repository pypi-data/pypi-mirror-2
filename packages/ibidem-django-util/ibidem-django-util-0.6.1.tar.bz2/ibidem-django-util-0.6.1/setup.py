#!/usr/bin/env python

from distribute_setup import use_setuptools
use_setuptools()
from setuptools import setup

def read(filename):
    f = open(filename)
    contents = f.read()
    f.close()
    return contents

classifiers = """
Development Status :: 4 - Beta
Framework :: Django
Intended Audience :: Developers
License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)
Operating System :: OS Independent
Programming Language :: Python
Topic :: Software Development :: Libraries :: Python Modules
"""

setup(
    name = "ibidem-django-util",
    version = "0.6.1",
    packages = ["ibidem", "ibidem.django"],
    py_modules = ["ibidem.django.util"],
    namespace_packages = ["ibidem", "ibidem.django"],
    zip_safe = True,
    include_package_data = True,

    # Metadata
    author = "Morten Lied Johansen",
    author_email = "mortenjo@ifi.uio.no",
    description = "Ibidem Django utilities",
    long_description = read("README.txt"),
    license = "LGPL",
    keywords = "ibidem django util",
    classifiers = filter(None, classifiers.split("\n")),
    url = "http://ibidem.homeip.net/Misc/wiki/Django/Utils"
)
