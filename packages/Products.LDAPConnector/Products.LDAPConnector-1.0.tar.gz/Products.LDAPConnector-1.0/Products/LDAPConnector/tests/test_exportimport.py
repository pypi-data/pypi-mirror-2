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
""" LDAPConnector exporter and importer tests

$Id: test_exportimport.py 1894 2010-02-03 21:00:11Z jens $
"""

import unittest

from Products.GenericSetup.tests.common import BaseRegistryTests
from Products.GenericSetup.tests.common import DummyExportContext
from Products.GenericSetup.tests.common import DummyImportContext
from Products.GenericSetup.tests.conformance \
        import ConformsToIFilesystemExporter
from Products.GenericSetup.tests.conformance \
        import ConformsToIFilesystemImporter


class _TestBase(BaseRegistryTests):

    def _makeOne(self, context, *args, **kw):
        return self._getTargetClass()(context, *args, **kw)

    def _getTargetClass(self):
        from Products.LDAPConnector.exportimport import \
            LDAPConnectorExportImport
        return LDAPConnectorExportImport

    def _makePlugin(self, id='testing', *args, **kw):
        from Products.LDAPConnector.LDAPConnector import LDAPConnector
        return LDAPConnector(id, *args, **kw)

    def _setupDefaultTraversable(self):
        from zope.interface import Interface
        from zope.component import provideAdapter
        from zope.traversing.interfaces import ITraversable
        from zope.traversing.adapters import DefaultTraversable
        provideAdapter(DefaultTraversable, (Interface,), ITraversable)


class LDAPConnectorImportTests(_TestBase, ConformsToIFilesystemImporter):
    
    def test_import_empty(self):
        plugin = self._makePlugin('empty').__of__(self.root)
        adapter = self._makeOne(plugin)
        context = DummyImportContext(plugin)
        context._files['plugins/empty.xml'] = _EMPTY

        adapter.import_(context, 'plugins', False)

        self.assertEquals(plugin.title, 'Test title')
        self.assertEquals(plugin.bind_dn, 'cn=Manager,dc=localhost')
        self.assertEquals(plugin.bind_pwd, 'secret')
        self.failUnless(plugin.read_only)
        self.failIf(plugin.servers)

    def test_import_with_servers(self):
        plugin = self._makePlugin('with_servers').__of__(self.root)
        adapter = self._makeOne(plugin)
        context = DummyImportContext(plugin)
        context._files['plugins/with_servers.xml'] = _WITH_SERVERS

        adapter.import_(context, 'plugins', False)

        self.assertEquals(plugin.title, 'Test title')
        self.assertEquals(plugin.bind_dn, 'cn=Manager,dc=localhost')
        self.assertEquals(plugin.bind_pwd, 'secret')
        self.failUnless(plugin.read_only)

        servers = plugin.servers.values()
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

    def test_import_deformed(self):
        plugin = self._makePlugin('deformed').__of__(self.root)
        adapter = self._makeOne(plugin)
        context = DummyImportContext(plugin)
        context._files['plugins/deformed.xml'] = _DEFORMED

        adapter.import_(context, 'plugins', False)

        self.assertEquals(plugin.title, 'Test title')
        self.assertEquals(plugin.bind_dn, 'cn=Manager,dc=localhost')
        self.assertEquals(plugin.bind_pwd, 'secret')
        self.failIf(plugin.read_only)

        svr = { 'url': 'ldap://server1.dom.com:389'
              , 'op_timeout': -1
              , 'conn_timeout': 5
              , 'start_tls': False
              }
        self.assertEquals(plugin.servers.values(), [svr])

    def test_import_without_purge_leaves_existing_servers(self):
        plugin = self._makePlugin('with_servers').__of__(self.root)
        plugin.addServer( 'server1.dom.com'
                        , '636'
                        , 'ldaps'
                        , conn_timeout=10
                        , op_timeout=5
                        )
        plugin.addServer( 'server2.dom.com'
                        , '1389'
                        , 'ldap'
                        , conn_timeout=1
                        , op_timeout=2
                        )
        adapter = self._makeOne(plugin)
        context = DummyImportContext(plugin, purge=False)
        context._files['plugins/with_servers.xml'] = _EMPTY

        adapter.import_(context, 'plugins', False)

        self.assertEquals(plugin.title, 'Test title')
        self.assertEquals(plugin.bind_dn, 'cn=Manager,dc=localhost')
        self.assertEquals(plugin.bind_pwd, 'secret')
        self.failUnless(plugin.read_only)

        servers = plugin.servers.values()
        svr1 = { 'url': 'ldaps://server1.dom.com:636'
               , 'op_timeout': 5
               , 'conn_timeout': 10
               , 'start_tls': False
               }
        svr2 = { 'url': 'ldap://server2.dom.com:1389'
               , 'op_timeout': 2
               , 'conn_timeout': 1
               , 'start_tls': False
               }

        self.assertEquals(len(servers), 2)
        self.failUnless(svr1 in servers)
        self.failUnless(svr2 in servers)

    def test_import_with_purge_wipes_existing_servers(self):
        plugin = self._makePlugin('with_servers').__of__(self.root)
        plugin.addServer( 'server1.dom.com'
                        , '636'
                        , 'ldaps'
                        , conn_timeout=10
                        , op_timeout=5
                        )
        plugin.addServer( 'server2.dom.com'
                        , '1389'
                        , 'ldap'
                        , conn_timeout=1
                        , op_timeout=2
                        )
        adapter = self._makeOne(plugin)
        context = DummyImportContext(plugin, purge=True)
        context._files['plugins/with_servers.xml'] = _EMPTY

        adapter.import_(context, 'plugins', False)

        self.assertEquals(plugin.title, 'Test title')
        self.assertEquals(plugin.bind_dn, 'cn=Manager,dc=localhost')
        self.assertEquals(plugin.bind_pwd, 'secret')
        self.failUnless(plugin.read_only)
        self.failIf(plugin.servers)


class LDAPConnectorExportTests(_TestBase, ConformsToIFilesystemExporter):
    
    def test_listExportableItems(self):
        plugin = self._makePlugin().__of__(self.root)
        adapter = self._makeOne(plugin)
        self.failIf(adapter.listExportableItems())

        plugin.addServer( 'server1.dom.com'
                        , '636'
                        , 'ldaps'
                        , conn_timeout=10
                        , op_timeout=5
                        )
        self.failIf(adapter.listExportableItems())

    def test_export_default(self):
        self._setupDefaultTraversable()

        plugin = self._makePlugin('default').__of__(self.root)
        adapter = self._makeOne(plugin)
        context = DummyExportContext(plugin)

        adapter.export(context, 'plugins', False)
        self.assertEquals(len(context._wrote), 1)

        filename, text, content_type = context._wrote[0]
        self.assertEqual(filename, 'plugins/default.xml')
        self._compareDOM(text, _DEFAULT)
        self.assertEqual(content_type, 'text/xml')

    def test_export_empty(self):
        self._setupDefaultTraversable()

        plugin = self._makePlugin('empty').__of__(self.root)
        plugin.title = 'Test title'
        plugin.bind_dn = 'cn=Manager,dc=localhost'
        plugin.bind_pwd = 'secret'
        plugin.read_only = True
        adapter = self._makeOne(plugin)
        context = DummyExportContext(plugin)

        adapter.export(context, 'plugins', False)
        self.assertEquals(len(context._wrote), 1)

        filename, text, content_type = context._wrote[0]
        self.assertEqual(filename, 'plugins/empty.xml')
        self._compareDOM(text, _EMPTY)
        self.assertEqual(content_type, 'text/xml')

    def test_export_with_servers(self):
        self._setupDefaultTraversable()

        plugin = self._makePlugin('with_servers').__of__(self.root)
        plugin.title = 'Test title'
        plugin.bind_dn = 'cn=Manager,dc=localhost'
        plugin.bind_pwd = 'secret'
        plugin.read_only = True
        plugin.addServer( 'server1.dom.com'
                        , '636'
                        , 'ldaps'
                        , conn_timeout=10
                        , op_timeout=5
                        )
        plugin.addServer( 'server2.dom.com'
                        , '1389'
                        , 'ldaptls'
                        , conn_timeout=1
                        , op_timeout=2
                        )
        adapter = self._makeOne(plugin)
        context = DummyExportContext(plugin)

        adapter.export(context, 'plugins', False)
        self.assertEquals(len(context._wrote), 1)

        filename, text, content_type = context._wrote[0]
        self.assertEqual(filename, 'plugins/with_servers.xml')
        self._compareDOM(text, _WITH_SERVERS)
        self.assertEqual(content_type, 'text/xml')


def test_suite():
    return unittest.TestSuite((
        unittest.makeSuite(LDAPConnectorImportTests),
        unittest.makeSuite(LDAPConnectorExportTests),
        ))


_DEFAULT = """\
<?xml version="1.0" ?>
<ldapconnector
    bind_dn=""
    bind_pwd=""
    read_only="0"
    title="">
</ldapconnector>
"""

_EMPTY = """\
<?xml version="1.0" ?>
<ldapconnector
    bind_dn="cn=Manager,dc=localhost"
    bind_pwd="secret"
    read_only="1"
    title="Test title">
</ldapconnector>
"""

_WITH_SERVERS = """\
<?xml version="1.0" ?>
<ldapconnector
    bind_dn="cn=Manager,dc=localhost"
    bind_pwd="secret"
    read_only="1"
    title="Test title">
  <server 
    connection_timeout="1" 
    host="server2.dom.com" 
    operations_timeout="2" 
    port="1389" 
    protocol="ldaptls"
    />
  <server 
    connection_timeout="10" 
    host="server1.dom.com" 
    operations_timeout="5" 
    port="636" 
    protocol="ldaps"
    />
</ldapconnector>
"""

_DEFORMED = """\
<?xml version="1.0" ?>
<ldapconnector
    bind_dn="cn=Manager,dc=localhost"
    bind_pwd="secret"
    read_only="No"
    title="Test title">
  <server 
    connection_timeout="1" 
    host="" 
    operations_timeout="2" 
    port="1389" 
    protocol="ldap"
    />
  <server 
    connection_timeout="INVALID" 
    host="server1.dom.com" 
    operations_timeout="INVALID" 
    />
</ldapconnector>
"""
