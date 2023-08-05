##############################################################################
#
# Copyright (c) 2010 Jens Vagelpohl and Contributors. All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
""" LDAPConnector class tests

$Id: test_LDAPConnector.py 1882 2010-02-01 12:52:24Z jens $
"""

import unittest
import uuid

from Products.LDAPConnector.tests.dummy import DummyRequest


class LDAPConnectorTests(unittest.TestCase):

    def _makeOne(self, *args, **kw):
        from Products.LDAPConnector.LDAPConnector import LDAPConnector
        return LDAPConnector(*args, **kw)

    def test_conformance(self):
        from dataflake.ldapconnection.interfaces import ILDAPConnection
        from Products.LDAPConnector.LDAPConnector import LDAPConnector
        from zope.interface.verify import verifyClass
        verifyClass(ILDAPConnection, LDAPConnector)

    def test_constructor_defaults(self):
        from dataflake.cache.timeout import LockingTimeoutCache
        conn = self._makeOne('test_id')
        self.assertEquals(conn.getId(), 'test_id')
        self.assertEquals(conn.title, '')
        self.assertEquals(conn.timeout, 600)
        self.assertEquals(conn.bind_dn, '')
        self.assertEquals(conn.bind_pwd, '')
        self.failIf(conn.read_only)
        self.failIf(conn.servers)
        self.failUnless(isinstance(conn.hash, uuid.UUID))

    def test_zope_factory(self):
        from dataflake.cache.timeout import LockingTimeoutCache
        from OFS.Folder import Folder
        from Products.LDAPConnector.LDAPConnector import manage_addLDAPConnector

        container = Folder('container')
        request = DummyRequest()
        manage_addLDAPConnector( container
                               , 'test_id'
                               , title='Test Title'
                               , REQUEST=request
                               )
        conn = container.test_id

        self.failUnless(request.RESPONSE.redirected)
        self.assertEquals(conn.getId(), 'test_id')
        self.assertEquals(conn.title, 'Test Title')
        self.assertEquals(conn.timeout, 600)
        self.assertEquals(conn.bind_dn, '')
        self.assertEquals(conn.bind_pwd, '')
        self.failIf(conn.read_only)
        self.failIf(conn.servers)
        self.failUnless(isinstance(conn.hash, uuid.UUID))

    def test_zope_factory_duplicate(self):
        from OFS.Folder import Folder
        from Products.LDAPConnector.LDAPConnector import manage_addLDAPConnector

        container = Folder('container')
        setattr(container, 'test_id', 'FAKE')
        manage_addLDAPConnector(container, 'test_id', title='Test Title')

        self.assertEquals(container.test_id, 'FAKE')


def test_suite():
    return unittest.TestSuite((
        unittest.makeSuite(LDAPConnectorTests),
        ))
