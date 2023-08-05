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
"""Tests for the ZCML Documentation Module

$Id: tests.py 115384 2010-08-02 19:21:24Z menesis $
"""
import os
import unittest
import doctest

from zope.configuration import xmlconfig
from zope.traversing.interfaces import IPhysicallyLocatable
from zope.location.traversing import LocationPhysicallyLocatable

import zope.app.appsetup.appsetup
from zope.app.tree.interfaces import IUniqueId
from zope.app.tree.adapters import LocationUniqueId
from zope.app.testing import setup, ztapi
from zope.app.testing.functional import BrowserTestCase

from zope.app.apidoc.testing import APIDocLayer
from zope.app.apidoc.tests import Root
from zope.app.apidoc.apidoc import APIDocumentation
from zope.app.apidoc.interfaces import IDocumentationModule
from zope.app.apidoc.zcmlmodule import Namespace, Directive
from zope.app.apidoc.zcmlmodule import ZCMLModule
from zope.app.apidoc.tests import Root
import zope.app.zcmlfiles


def setUp(test):
    root_folder = setup.placefulSetUp(True)

    ztapi.provideAdapter(None, IUniqueId, LocationUniqueId)
    ztapi.provideAdapter(None, IPhysicallyLocatable,
                         LocationPhysicallyLocatable)

    # Set up apidoc module
    test.globs['apidoc'] = APIDocumentation(root_folder, '++apidoc++')

    # Register documentation modules
    ztapi.provideUtility(IDocumentationModule, ZCMLModule(), 'ZCML')

    config_file = os.path.join(
        os.path.dirname(zope.app.zcmlfiles.__file__), 'meta.zcml')

    # Fix up path for tests.
    global old_context
    old_context = zope.app.appsetup.appsetup.getConfigContext()
    zope.app.appsetup.appsetup.__config_context = xmlconfig.file(
        config_file, zope.app.zcmlfiles, execute=False)

def tearDown(test):
    setup.placefulTearDown()
    zope.app.appsetup.appsetup.__config_context = old_context
    from zope.app.apidoc import zcmlmodule
    zcmlmodule.namespaces = None
    zcmlmodule.subdirs = None

def getDirective():
    module = ZCMLModule()
    module.__parent__ = Root()
    module.__name__ = 'ZCML'

    def foo(): pass

    ns = Namespace(module, 'http://namespaces.zope.org/browser')
    return Directive(ns, 'page', None, foo, None, ())


class ZCMLModuleTests(BrowserTestCase):
    """Just a couple of tests ensuring that the templates render."""

    def testMenu(self):
        response = self.publish(
            '/++apidoc++/ZCML/menu.html',
            basic='mgr:mgrpw')
        self.assertEqual(response.getStatus(), 200)
        body = response.getBody()
        self.assert_(body.find('All Namespaces') > 0)
        self.checkForBrokenLinks(body, '/++apidoc++/ZCML/menu.html',
                                 basic='mgr:mgrpw')

    def testDirectiveDetailsView(self):
        response = self.publish('/++apidoc++/ZCML/ALL/configure/index.html',
                                basic='mgr:mgrpw')
        self.assertEqual(response.getStatus(), 200)
        body = response.getBody()
        self.assert_(body.find('<i>all namespaces</i>') > 0)
        self.checkForBrokenLinks(body,
                                 '/++apidoc++/ZCML/ALL/configure/index.html',
                                 basic='mgr:mgrpw')


def test_suite():
    ZCMLModuleTests.layer = APIDocLayer
    return unittest.TestSuite((
        doctest.DocFileSuite('README.txt',
                             setUp=setUp, tearDown=tearDown,
                             optionflags=doctest.NORMALIZE_WHITESPACE),
        doctest.DocFileSuite('browser.txt',
                             setUp=setUp, tearDown=tearDown,
                             optionflags=doctest.NORMALIZE_WHITESPACE),
        unittest.makeSuite(ZCMLModuleTests),
        ))

if __name__ == '__main__':
    unittest.main(default='test_suite')
