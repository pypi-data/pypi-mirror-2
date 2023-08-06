#!/usr/bin/env python
# coding: utf-8


"""
    run all unittests
    ~~~~~~~~~~~~~~~~~

    :copyleft: 2008-2011 by python-creole team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""


import unittest

from tests.utils.utils import MarkupTest
from tests.test_cross_compare_all import CrossCompareTests
from tests.test_cross_compare_creole import CrossCompareCreoleTests
from tests.test_cross_compare_textile import CrossCompareTextileTests
from tests.test_creole2html import TestCreole2html, TestCreole2htmlMarkup
from tests.test_html2creole import TestHtml2Creole, TestHtml2CreoleMarkup


if __name__ == '__main__':
    unittest.main()
