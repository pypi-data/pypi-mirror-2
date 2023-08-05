#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
    svn:keywords sync tool
    ~~~~~~~~~~~~~~~~~~~~~~

    usefull tools to automatic setup the SVN keywords.

    Used svn_keyword.py from:

    http://code.google.com/p/python-code-snippets/source/browse/CodeSnippets/svn_keywords.py
    or
    http://python-code-snippets.googlecode.com/svn/CodeSnippets/svn_keywords.py

    Last commit info:
    ~~~~~~~~~~~~~~~~~
    $LastChangedDate:2007-09-22 22:21:14 +0200 (Sa, 22 Sep 2007) $
    $Rev:1244 $
    $Author:JensDiemer $

    :copyleft: 2008 by the PyLucid team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""

import sys, os

os.chdir("../") # go into PyLucid App root folder
print os.getcwd()

# Path to the svn_keywords.py file:
sys.path.insert(0,"../../python-code-snippets/CodeSnippets/")

try:
    from svn_keywords import Config, cleanup, print_status, sync_keywords
except ImportError, e:
    print "Error, can't import svn_keywords.py:"
    print e
    print
    print "(More Information in Doc-String)"
    print
    sys.exit()

config = Config
config.repository = "."
config.skip_dirs = (
)
config.skip_file_ext = (".pyc",".gif", ".png")
#config.simulation = False
config.simulation = True


if __name__ == "__main__":
#    cleanup(config)
    sync_keywords(config)
#    print_status(config)
    print
    print "---END---"


