##############################################################################
#
# Copyright (c) 2001, 2002 Zope Corporation and Contributors.
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
"""Placeless Test Setup

$Id: testing.py 109324 2010-02-22 22:48:31Z sidnei $
"""

# HACK to make sure basicmost event subscriber is installed
import zope.component.event

# we really don't need special setup now:
from zope.testing.cleanup import CleanUp as PlacelessSetup

def setUp(test=None):
    PlacelessSetup().setUp()

def tearDown(test=None):
    PlacelessSetup().tearDown()
