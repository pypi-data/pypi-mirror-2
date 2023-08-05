##############################################################################
#
# Copyright (c) 2003 Zope Corporation and Contributors.
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
"""An adapter from zope.security.interfaces.IPrincipal to
zope.publisher.interfaces.logginginfo.ILoggingInfo.

$Id: principallogging.py 106689 2009-12-17 08:26:28Z ctheune $
"""
from zope.component import adapts
from zope.interface import implements
from zope.publisher.interfaces.logginginfo import ILoggingInfo
from zope.security.interfaces import IPrincipal

class PrincipalLogging(object):

    adapts(IPrincipal)
    implements(ILoggingInfo)

    def __init__(self, principal):
        self.principal = principal

    def getLogMessage(self):
        return str(self.principal.id)
