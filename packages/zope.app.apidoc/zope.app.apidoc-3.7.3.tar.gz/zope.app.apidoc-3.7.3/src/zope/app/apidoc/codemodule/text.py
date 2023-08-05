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
"""Function representation for code browser

$Id: text.py 113308 2010-06-10 01:09:36Z srichter $
"""
__docformat__ = 'restructuredtext'
from zope.interface import implements
from zope.location.interfaces import ILocation

from zope.app.apidoc.codemodule.interfaces import ITextFile

class TextFile(object):
    """This class represents a function declared in the module."""
    implements(ILocation, ITextFile)

    def __init__(self, path, name, package):
        self.path = path
        self.__parent__ = package
        self.__name__ = name

    def getContent(self):
        file = open(self.path, 'rU')
        content = file.read()
        file.close()
        return content.decode('utf-8')
