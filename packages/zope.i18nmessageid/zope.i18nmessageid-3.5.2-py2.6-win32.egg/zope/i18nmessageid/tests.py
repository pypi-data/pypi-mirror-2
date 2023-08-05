##############################################################################
#
# Copyright (c) 2003 Zope Foundation and Contributors.
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
"""Message ID tests.

$Id: tests.py 110993 2010-04-16 18:53:41Z tseaver $
"""
import unittest
from doctest import DocFileSuite
from doctest import DocTestSuite

def test_suite():
    return unittest.TestSuite((
	    DocTestSuite('zope.i18nmessageid.message'),
	    DocFileSuite('messages.txt', package='zope.i18nmessageid'),
	    ))

if __name__ == '__main__':
    unittest.main(defaultTest="test_suite")
