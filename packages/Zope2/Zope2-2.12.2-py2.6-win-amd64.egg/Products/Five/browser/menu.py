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
"""Some menu code

$Id: menu.py 85775 2008-04-26 20:10:16Z hannosch $
"""
import zope.deferredimport

zope.deferredimport.deprecated(
    "The Five specific view has been made obsolete. Please use the " 
    "view from zope.app.publisher directly.",
    MenuAccessView = 'zope.app.publisher.browser.menu.MenuAccessView',
    )
