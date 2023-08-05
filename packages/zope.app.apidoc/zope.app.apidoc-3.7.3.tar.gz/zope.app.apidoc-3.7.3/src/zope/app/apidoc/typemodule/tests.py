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
from zope.app.testing.functional import BrowserTestCase
from zope.app.testing import placelesssetup
from zope.app.apidoc.testing import APIDocLayer


class TypeModuleTests(BrowserTestCase):
    """Just a couple of tests ensuring that the templates render."""

    def testMenu(self):
        response = self.publish(
            '/++apidoc++/Type/@@menu.html',
            basic='mgr:mgrpw')
        self.assertEqual(response.getStatus(), 200)
        body = response.getBody()
        self.assert_(body.find('IBrowserSkinType') > 0)
        self.checkForBrokenLinks(body, '/++apidoc++/Type/@@menu.html',
                                 basic='mgr:mgrpw')


def test_suite():
    TypeModuleTests.layer = APIDocLayer
    return unittest.TestSuite((
        DocTestSuite('zope.app.apidoc.typemodule.type',
                     setUp=placelesssetup.setUp,
                     tearDown=placelesssetup.tearDown),
        unittest.makeSuite(TypeModuleTests),
        ))

if __name__ == '__main__':
    unittest.main(default='test_suite')
