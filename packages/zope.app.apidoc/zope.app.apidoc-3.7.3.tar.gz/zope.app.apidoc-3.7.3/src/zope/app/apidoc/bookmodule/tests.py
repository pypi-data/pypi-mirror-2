##############################################################################
#
# Copyright (c) 2004 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""Tests for the Book Documentation Module

$Id: tests.py 113308 2010-06-10 01:09:36Z srichter $
"""
import unittest
from zope.testing.doctest import DocTestSuite

def test_suite():
    return unittest.TestSuite((
        DocTestSuite('zope.app.apidoc.bookmodule.browser'),
        ))

if __name__ == '__main__':
    unittest.main(default='test_suite')
