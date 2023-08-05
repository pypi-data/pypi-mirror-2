##############################################################################
#
# Copyright (c) 2006 Zope Foundation and Contributors.
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
"""Unit tests for decode module.

$Id: test_decode.py 110405 2010-04-01 16:13:15Z tseaver $
"""

def test_processInputs():
    """
    Testing processInputs

      >>> from Products.Five.browser.decode import processInputs
      >>> charsets = ['iso-8859-1']
      >>> class DummyRequest:
      ...     form = {}
      >>> request = DummyRequest()

    Strings are converted to unicode::

      >>> request.form['foo'] = u'f\xf6\xf6'.encode('iso-8859-1')
      >>> processInputs(request, charsets)
      >>> request.form['foo'] == u'f\xf6\xf6'
      True

    Strings in lists are converted to unicode::

      >>> request.form['foo'] = [u'f\xf6\xf6'.encode('iso-8859-1')]
      >>> processInputs(request, charsets)
      >>> request.form['foo'] == [u'f\xf6\xf6']
      True

    Strings in tuples are converted to unicode::

      >>> request.form['foo'] = (u'f\xf6\xf6'.encode('iso-8859-1'),)
      >>> processInputs(request, charsets)
      >>> request.form['foo'] == (u'f\xf6\xf6',)
      True
    """

def test_suite():
    from zope.testing.doctest import DocTestSuite
    return DocTestSuite()
