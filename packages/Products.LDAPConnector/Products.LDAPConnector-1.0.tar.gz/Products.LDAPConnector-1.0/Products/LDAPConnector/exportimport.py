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
""" GenericSetup support for LDAPConnector instances

$Id: exportimport.py 1894 2010-02-03 21:00:11Z jens $
"""

import ldapurl
from xml.dom.minidom import parseString

from Acquisition import Implicit
from zope.interface import implements

from Products.GenericSetup.interfaces import IFilesystemExporter
from Products.GenericSetup.interfaces import IFilesystemImporter
from Products.PageTemplates.PageTemplateFile import PageTemplateFile


class LDAPConnectorExportImport(Implicit):
    """ Exporter/Importer for LDAPConnector instances
    """
    implements(IFilesystemExporter, IFilesystemImporter)

    encoding = None

    def __init__(self, context):
        self.context = context

    def export(self, export_context, subdir, root=False):
        """ See IFilesystemExporter.
        """
        template = PageTemplateFile( 'xml/ldapconnector.xml'
                                   ,  globals()
                                   ).__of__(self.context)
        info = { 'title': self.context.title
               , 'bind_dn': self.context.bind_dn
               , 'bind_pwd': self.context.bind_pwd
               , 'read_only': int(bool(self.context.read_only))
               }
        servers = []
        for svr in self.context.servers.values():
            ldap_url = ldapurl.LDAPUrl(svr['url'])
            protocol = ldap_url.urlscheme

            if ':' in ldap_url.hostport:
                host, port = ldap_url.hostport.split(':')
            else:
                host = ldap_url.hostport
                port = '389'

            if protocol == 'ldap' and svr['start_tls']:
                protocol = 'ldaptls'

            servers.append( { 'host': host
                            , 'port': port
                            , 'protocol': protocol
                            , 'connection_timeout': svr['conn_timeout']
                            , 'operations_timeout': svr['op_timeout']
                            }
                          )

        info['servers'] = servers

        export_context.writeDataFile( '%s.xml' % self.context.getId()
                                    , template(info=info)
                                    , 'text/xml'
                                    , subdir
                                    )

    def listExportableItems(self):
        """ See IFilesystemExporter.
        """
        return ()

    def import_(self, import_context, subdir, root=False):
        """ See IFilesystemImporter
        """
        self.encoding = import_context.getEncoding()

        if import_context.shouldPurge():
            self.context.__init__(self.context.id, self.context.title)

        data = import_context.readDataFile( '%s.xml' % self.context.getId()
                                          , subdir
                                          )

        if data is not None:
            dom = parseString(data)
            root = dom.firstChild

            self.context.title = self._getNodeAttr(root, 'title', '')
            self.context.bind_dn = self._getNodeAttr(root, 'bind_dn', '')
            self.context.bind_pwd = self._getNodeAttr(root, 'bind_pwd', '')
            self.context.read_only = self._getNodeAttr(root, 'read_only', False)

            for server in root.getElementsByTagName('server'):
                host = self._getNodeAttr(server, 'host')

                if not host:
                    continue

                port = self._getNodeAttr(server, 'port', 389)
                protocol = self._getNodeAttr(server, 'protocol', 'ldap')
                try:
                    ct = int(self._getNodeAttr(server, 'connection_timeout', 5))
                except ValueError:
                    ct = 5
                try:
                    ot = int(self._getNodeAttr(server, 'operations_timeout', -1))
                except ValueError:
                    ot = -1

                self.context.addServer( host
                                      , port
                                      , protocol
                                      , conn_timeout=ct
                                      , op_timeout=ot
                                      )

    def _getNodeAttr(self, node, attrname, default=None):
        attr = node.attributes.get(attrname)
        if attr is None:
            return default
        value = attr.value
        if isinstance(value, unicode) and self.encoding is not None:
            value = value.encode(self.encoding)

        # boolean?
        lower_value = value.lower()
        if lower_value in ('false', 'no', '0'):
            value = False
        elif lower_value in ('true', 'yes', '1'):
            value = True

        return value

