##############################################################################
#
# Copyright (c) 2009 Zope Foundation and Contributors.
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
"""Password manager interface

$Id: interfaces.py 112030 2010-05-05 18:53:49Z tseaver $
"""
import zope.interface

class IPasswordManager(zope.interface.Interface):
    """Password manager"""

    def encodePassword(password):
        """Return encoded data for the given password"""

    def checkPassword(encoded_password, password):
        """Return whether the given encoded data coincide with the given password"""
