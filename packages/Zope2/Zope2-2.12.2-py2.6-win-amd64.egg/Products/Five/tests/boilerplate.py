##############################################################################
#
# Copyright (c) 2005 Zope Corporation and Contributors.
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
"""Boiler plate test module

$Id: boilerplate.py 99527 2009-04-26 16:33:20Z hannosch $
"""

def test_boilerplate():
    """
      >>> from zope.component.testing import setUp, tearDown
      >>> setUp()

      >>> import Products.Five.tests
      >>> from Products.Five import zcml
      >>> zcml.load_config('boilerplate.zcml', Products.Five.tests)

      >>> from Products.Five.tests.testing import manage_addFiveTraversableFolder
      >>> from Products.Five.tests.testing.simplecontent import manage_addSimpleContent
      >>> from Products.Five.tests.testing.fancycontent import manage_addFancyContent

      >>> tearDown()
    """

def test_suite():
    from Testing.ZopeTestCase import ZopeDocTestSuite
    return ZopeDocTestSuite()
