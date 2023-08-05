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
""" LDAPConnector browser view tests base class

$Id: base.py 1904 2010-02-07 22:14:32Z jens $
"""

import unittest

class ViewTests(unittest.TestCase):

    def _makeOne(self, context, *args, **kw):
        return self._getTargetClass()(context, *args, **kw)

    def _makeConnector(self, id='testing', *args, **kw):
        from dataflake.ldapconnection.tests import fakeldap
        from Products.LDAPConnector.LDAPConnector import LDAPConnector
        conn = LDAPConnector(id, *args, **kw)
        conn.c_factory = fakeldap.FakeLDAPConnection
        return conn

    def setUp(self):
        from dataflake.ldapconnection.tests import fakeldap
        from Products.LDAPConnector.tests.dummy import DummyRequest
        super(ViewTests, self).setUp()
        self.request = DummyRequest()
        self.conn = self._makeConnector()
        self.view = self._makeOne(self.conn, self.request)
        # Add a root item into the fake LDAP database
        fakeldap.addTreeItems('dc=localhost')

    def tearDown(self):
        from dataflake.ldapconnection.tests import fakeldap
        fakeldap.clearTree()
