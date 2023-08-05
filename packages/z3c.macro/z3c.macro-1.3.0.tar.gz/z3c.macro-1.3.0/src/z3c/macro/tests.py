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
"""Viewlet tests

$Id: tests.py 114189 2010-07-05 06:43:33Z icemac $
"""
__docformat__ = 'restructuredtext'

from zope import component
from zope.app.testing import setup
from zope.configuration import xmlconfig
import doctest
import itertools
import unittest
import z3c.pt
import z3c.ptcompat


def setUp(test):
    root = setup.placefulSetUp(site=True)
    test.globs['root'] = root

def setUpZPT(test):
    z3c.ptcompat.config.disable()
    setUp(test)

    from zope.browserpage import metaconfigure
    from z3c.macro import tales
    metaconfigure.registerType('macro', tales.MacroExpression)

def setUpZ3CPT(suite):
    z3c.ptcompat.config.enable()
    setUp(suite)
    xmlconfig.XMLConfig('configure.zcml', z3c.pt)()

    from z3c.macro import tales
    component.provideUtility(
        tales.z3cpt_macro_expression, name='macro')

def tearDown(test):
    setup.placefulTearDown()

def test_suite():
    tests = ((
        doctest.DocFileSuite('README.txt',
            setUp=setUp, tearDown=tearDown,
            optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS,
            ),
        doctest.DocFileSuite('zcml.txt', setUp=setUp, tearDown=tearDown,
            optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS,),
        ) for setUp in (setUpZ3CPT, setUpZPT))

    return unittest.TestSuite(itertools.chain(*tests))

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
