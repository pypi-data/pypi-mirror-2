### -*- coding: utf-8 -*- ####################################################
##############################################################################
#
# Copyright (c) 2008-2009 Thierry Florac <tflorac AT ulthar.net>
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


# import Zope3 interfaces
from zope.schema.interfaces import ITextLine, IList

# import local interfaces

# import Zope3 packages
from zope.interface import implements
from zope.schema import TextLine, Iterable

# import local packages


class IPrincipal(ITextLine):
    """Marker interface to define principal ID field"""


class IPrincipalList(IList):
    """Marker interface to define a list of principal IDs"""



class Principal(TextLine):
    """Schema field to store a principal ID"""

    implements(IPrincipal)


class PrincipalList(Iterable):
    """Schema field to store a list of principal IDs"""

    implements(IPrincipalList)
