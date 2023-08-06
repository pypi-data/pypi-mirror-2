#!/usr/bin/env python
# coding: utf-8

"""
    distutils setup
    ~~~~~~~~~~~~~~~

    :copyleft: 2009-2010 by the python-creole team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""

import os

from setuptools import setup, find_packages

from creole import VERSION_STRING


PACKAGE_ROOT = os.path.dirname(os.path.abspath(__file__))


def get_authors():
    try:
        f = file(os.path.join(PACKAGE_ROOT, "AUTHORS"), "r")
        authors = [l.strip(" *\r\n") for l in f if l.strip().startswith("*")]
        f.close()
    except Exception, err:
        authors = "[Error: %s]" % err
    return authors


def get_long_description():
    try:
        f = file(os.path.join(PACKAGE_ROOT, "README"), "r")
        long_description = f.read().strip()
        f.close()
    except Exception, err:
        long_description = "[Error: %s]" % err
    return long_description


setup(
    name='python-creole',
    version=VERSION_STRING,
    description='python-creole is an open-source creole2html and html2creole converter in pure Python.',
    long_description=get_long_description(),
    author=get_authors(),
    maintainer="Jens Diemer",
    url='http://code.google.com/p/python-creole/',
    packages=find_packages(),
    include_package_data=True, # include package data under svn source control
    zip_safe=True,
    classifiers=[
#        "Development Status :: 4 - Beta",
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Programming Language :: Python",
        "Topic :: Documentation",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Operating System :: OS Independent",
    ],
    test_suite="tests.run_all_tests",
)
