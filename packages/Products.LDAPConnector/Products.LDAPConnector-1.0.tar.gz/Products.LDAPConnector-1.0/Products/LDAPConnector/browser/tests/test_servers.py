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
""" LDAPConnector servers browser view tests

$Id: test_servers.py 1904 2010-02-07 22:14:32Z jens $
"""

import unittest

from Products.LDAPConnector.browser.tests.base import ViewTests

class ServersViewTests(ViewTests):

    def _getTargetClass(self):
        from Products.LDAPConnector.browser.servers import \
            ServersView
        return ServersView

    def test_add_remove_server(self):
        self.failIf(self.conn.servers)
        self.failIf(self.view.getServers())

        self.request.method = 'POST'
        self.request.form['host'] = 'server1.dom.com'
        self.request.form['port'] = '636'
        self.request.form['protocol'] = 'ldaps'
        self.request.form['operations_timeout'] = 5
        self.request.form['connection_timeout'] = 10
        self.view()

        self.request.form['host'] = 'server2.dom.com'
        self.request.form['port'] = '1389'
        self.request.form['protocol'] = 'ldaptls'
        self.request.form['operations_timeout'] = 2
        self.request.form['connection_timeout'] = 1
        self.view()

        servers = self.conn.servers.values()
        svr1 = { 'url': 'ldaps://server1.dom.com:636'
               , 'op_timeout': 5
               , 'conn_timeout': 10
               , 'start_tls': False
               }
        svr2 = { 'url': 'ldap://server2.dom.com:1389'
               , 'op_timeout': 2
               , 'conn_timeout': 1
               , 'start_tls': True
               }

        self.assertEquals(len(servers), 2)
        self.failUnless(svr1 in servers)
        self.failUnless(svr2 in servers)

        self.request.form.clear()
        self.request.form['svr_remove'] = True
        self.request.form['identifiers'] = ['ldaps://server1.dom.com:636']
        self.view()
        self.assertEquals(self.conn.servers.values(), [svr2])

        self.request.form['identifiers'] = ['ldapi:///unknown']
        self.view()
        self.assertEquals(self.conn.servers.values(), [svr2])

        self.request.form['identifiers'] = ['ldap://server2.dom.com:1389']
        self.view()
        self.failIf(self.conn.servers)
        self.failIf(self.view.getServers())

    def test_remove_server_noselection(self):
        self.request.method = 'POST'
        self.request.form['svr_remove'] = True
        self.request.form['identifiers'] = []
        self.view()
        self.failUnless(self.request.get('manage_tabs_message'))

    def test_getServers(self):
        self.request.method = 'POST'
        self.request.form['host'] = 'server1.dom.com'
        self.request.form['port'] = '636'
        self.request.form['protocol'] = 'ldaps'
        self.request.form['operations_timeout'] = 1
        self.request.form['connection_timeout'] = 1
        self.view()

        server_info = self.view.getServers()
        self.assertEquals(len(server_info), 1)
        self.failUnless(server_info[0]['status'])

    def test_getServers_error(self):
        import ldap
        from dataflake.ldapconnection.tests import fakeldap
        raising_connection = fakeldap.RaisingFakeLDAPConnection()
        raising_connection.setExceptionAndMethod( 'simple_bind_s'
                                                , ldap.LDAPError('Oops')
                                                )
        def factory(*args, **kw):
            return raising_connection
        self.conn.c_factory = factory
        self.conn.addServer('host', 389, 'ldaptls')

        server_info = self.view.getServers()
        self.assertEquals(len(server_info), 1)
        self.assertEquals(server_info[0]['status'], "LDAPError('Oops',)")
        
    def test_getConnectedServer(self):
        self.assertEquals(self.view.getConnectedServer(), '-- not connected --')


def test_suite():
    return unittest.TestSuite((
        unittest.makeSuite(ServersViewTests),
        ))

