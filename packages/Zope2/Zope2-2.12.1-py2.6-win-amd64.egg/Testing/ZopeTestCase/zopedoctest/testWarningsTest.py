##############################################################################
#
# Copyright (c) 2005 Zope Corporation and Contributors. All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""Example doctest

$Id: testWarningsTest.py 97640 2009-03-07 21:48:23Z shh $
"""

from unittest import TestSuite
from Testing.ZopeTestCase import ZopeDocFileSuite


def test_suite():
    return TestSuite((
        ZopeDocFileSuite('WarningsTest.txt'),
    ))

