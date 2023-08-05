##############################################################################
#
# Copyright (c) 2002 Zope Corporation and Contributors. All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE
#
##############################################################################
__doc__='''Package wrapper for Document Template

This wrapper allows the (now many) document template modules to be
segregated in a separate package.

$Id: __init__.py 94813 2009-01-17 22:08:04Z shh $'''
__version__='$Revision: 1.18 $'[11:-2]

from DocumentTemplate.DT_String import String, File
from DocumentTemplate.DT_HTML import HTML, HTMLDefault, HTMLFile

# Register the dtml-tree tag
import TreeDisplay
