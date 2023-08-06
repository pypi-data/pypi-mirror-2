##############################################################################
#
# Copyright (c) 2004 Zope Corporation and Contributors.
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
"""Schema-generation tests

$Id: tests.py 115808 2010-08-19 19:23:02Z icemac $
"""

from zope.app.testing import placelesssetup
import doctest
import unittest


def tearDownREADME(test):
    placelesssetup.tearDown(test)
    test.globs['db'].close()


def test_suite():
    return unittest.TestSuite((
        doctest.DocFileSuite(
            'README.txt',
            setUp=placelesssetup.setUp, tearDown=tearDownREADME,
            ),
        doctest.DocTestSuite('zope.app.generations.generations'),
        doctest.DocTestSuite('zope.app.generations.utility'),
        ))
