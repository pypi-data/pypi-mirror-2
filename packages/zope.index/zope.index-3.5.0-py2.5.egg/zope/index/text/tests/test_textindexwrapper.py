##############################################################################
#
# Copyright (c) 2002 Zope Corporation and Contributors.
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
"""Unit tests for TextIndexWrapper.

$Id: test_textindexwrapper.py 93532 2008-12-02 12:08:17Z nadako $
"""
import unittest
from zope.testing import doctest

def test_suite():
    return doctest.DocFileSuite("../textindex.txt")

if __name__=='__main__':
    unittest.main(defaultTest='test_suite')
