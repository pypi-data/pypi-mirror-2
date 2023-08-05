##############################################################################
#
# Copyright (c) 2008 Zope Corporation and Contributors.
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
"""
$Id: tests.py 90851 2008-09-04 23:42:08Z mgedmin $
"""
import unittest

import transaction
from zope.testing import doctest
from zope.app.testing import setup
from zope.component import provideUtility
from zope.interface.verify import verifyObject

from keas.kmi.testing import TestingKeyManagementFacility
from keas.kmi.keyholder import KeyHolder
from keas.kmi.interfaces import IKeyManagementFacility
from keas.kmi.interfaces import IKeyHolder


def setUpPersistent(test):
    setup.setUpTestAsModule(test, name='keas.kmi.tests.doctestfile')
    setup.placelessSetUp()
    provideUtility(TestingKeyManagementFacility(),
                   provides=IKeyManagementFacility)


def tearDownPersistent(test):
    transaction.abort()
    setup.placelessTearDown()
    setup.tearDownTestAsModule(test)


def doctest_KeyHolder():
    """Smoke test for the KeyHolder class.

        >>> holder = KeyHolder(__file__)
        >>> verifyObject(IKeyHolder, holder)
        True

    """


def test_suite():
    return unittest.TestSuite([
        doctest.DocFileSuite(
            'README.txt',
            setUp=setup.placelessSetUp, tearDown=setup.placelessTearDown,
            optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS),
        doctest.DocFileSuite(
            'persistent.txt',
            setUp=setUpPersistent, tearDown=tearDownPersistent,
            optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS),
        doctest.DocTestSuite(),
    ])
