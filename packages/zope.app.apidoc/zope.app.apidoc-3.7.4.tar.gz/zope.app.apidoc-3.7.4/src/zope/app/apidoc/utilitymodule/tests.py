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
"""Tests for the Utility Documentation Module

$Id: tests.py 115384 2010-08-02 19:21:24Z menesis $
"""
import unittest
import doctest

import zope.deprecation
from zope.traversing.interfaces import IPhysicallyLocatable
from zope.location.traversing import LocationPhysicallyLocatable

from zope.app.apidoc.utilitymodule.utilitymodule import UtilityModule
from zope.app.apidoc.interfaces import IDocumentationModule
from zope.app.apidoc.apidoc import APIDocumentation
from zope.app.apidoc.testing import APIDocLayer
from zope.app.testing import setup, ztapi
from zope.app.testing.functional import BrowserTestCase
from zope.app.tree.interfaces import IUniqueId
from zope.app.tree.adapters import LocationUniqueId


def setUp(test):
    root_folder = setup.placefulSetUp(True)
    ztapi.provideAdapter(None, IUniqueId, LocationUniqueId)
    ztapi.provideAdapter(None, IPhysicallyLocatable,
                         LocationPhysicallyLocatable)

    # Set up apidoc module
    test.globs['apidoc'] = APIDocumentation(root_folder, '++apidoc++')

    # Register documentation modules
    ztapi.provideUtility(IDocumentationModule, UtilityModule(), 'Utility')


def tearDown(test):
    setup.placefulTearDown()


class UtilityModuleTests(BrowserTestCase):
    """Just a couple of tests ensuring that the templates render."""

    def testMenu(self):
        response = self.publish(
            '/++apidoc++/Utility/menu.html',
            basic='mgr:mgrpw')
        self.assertEqual(response.getStatus(), 200)
        body = response.getBody()
        self.assert_(body.find('IDocumentationModule') > 0)

        # BBB 2006/02/18, to be removed after 12 months
        # this avoids the deprecation warning for the deprecated
        # zope.publisher.interfaces.ILayer interface which get traversed
        # as a utility in this test
        zope.deprecation.__show__.off()
        self.checkForBrokenLinks(body, '/++apidoc++/Utility/menu.html',
                                 basic='mgr:mgrpw')
        zope.deprecation.__show__.on()

    def testUtilityDetailsView(self):
        response = self.publish(
            '/++apidoc++/Utility/'
            'zope.app.apidoc.interfaces.IDocumentationModule/'
            'Utility/index.html',
            basic='mgr:mgrpw')
        self.assertEqual(response.getStatus(), 200)
        body = response.getBody()
        self.assert_(
            body.find(
               'zope.app.apidoc.utilitymodule.utilitymodule.UtilityModule') > 0)
        self.checkForBrokenLinks(
            body,
            '/++apidoc++/Utility/'
            'zope.app.apidoc.interfaces.IDocumentationModule/'
            'Utility/index.html',
            basic='mgr:mgrpw')


def test_suite():
    UtilityModuleTests.layer = APIDocLayer
    return unittest.TestSuite((
        doctest.DocFileSuite('README.txt',
                             setUp=setUp,
                             tearDown=tearDown,
                             optionflags=doctest.NORMALIZE_WHITESPACE|
                                         doctest.ELLIPSIS),
        doctest.DocFileSuite('browser.txt',
                             setUp=setUp,
                             tearDown=tearDown,
                             optionflags=doctest.NORMALIZE_WHITESPACE),
        unittest.makeSuite(UtilityModuleTests),
        ))

if __name__ == '__main__':
    unittest.main(default="test_suite")
