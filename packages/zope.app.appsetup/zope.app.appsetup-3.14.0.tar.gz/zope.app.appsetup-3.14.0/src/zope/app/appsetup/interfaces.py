##############################################################################
#
# Copyright (c) 2004-2009 Zope Corporation and Contributors.
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
"""API for working installing things on startup.

$Id: interfaces.py 99909 2009-05-13 19:26:42Z tseaver $
"""
# BBB imports
from zope.processlifetime import IDatabaseOpened
from zope.processlifetime import DatabaseOpened
from zope.processlifetime import IDatabaseOpenedWithRoot
from zope.processlifetime import DatabaseOpenedWithRoot
from zope.processlifetime import IProcessStarting
from zope.processlifetime import ProcessStarting

# BBB aliases
IDatabaseOpenedEvent = IDatabaseOpened
IDatabaseOpenedWithRootEvent = IDatabaseOpenedWithRoot
IProcessStartingEvent = IProcessStarting
