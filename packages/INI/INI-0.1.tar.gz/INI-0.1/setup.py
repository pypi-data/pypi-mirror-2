#!/usr/bin/env python
# coding: utf-8
"""
    setup
    ~~~~~

    :copyright: 2010 by the INI Team, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""
from setuptools import setup

import ini

long_description = """\
INI provides simple and easy parsing and creating of flat and nested ini files.

It's as simple as ``ini.load("your.ini")`` or
``ini.dump(open("your.ini", "wb"), {"foo": {"spam": "eggs"}})``.

INI is completely tested and documented, if you run into any problems contact
the maintainer or `create a new issue on bitbucket
<http://bitbucket.org/DasIch/ini/issues/new/>`_."""

setup(
    name="INI",
    version=".".join(map(str, ini.__version__)),
    url="http://packages.python.org/INI/",
    license="MIT",
    maintainer="Daniel Neuhäuser",
    maintainer_email="dasdasich@gmail.com",
    description="Simple json/pickle like ini-file parsing.",
    long_description=long_description,
    py_modules=["ini"],
)
