##############################################################################
#
# Copyright (c) Zope Corporation and Contributors.
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

from zope.testing import doctest
import os
import unittest
import zope.app.testing.functional

class Test(zope.app.testing.functional.ZCMLLayer):

    def __init__(self):
        pass # Circumvent inherited constructior :)

    allow_teardown = False
    config_file = os.path.join(os.path.dirname(__file__), 'tests.zcml')
    __name__ = config_file
    product_config = None

    def __call__(self, *args, **kw):
        test = doctest.DocFileSuite(*args, **kw)
        test.layer = self
        return test

def test_suite():
    return unittest.TestSuite((
        Test()(
            'application.txt', 'session.txt', 'form.test', 'widgets.txt',
            optionflags=doctest.ELLIPSIS),
        ))

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')

