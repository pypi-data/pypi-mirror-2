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
""" ZMI Server configuration view for Products.LDAPConnector

$Id: servers.py 1899 2010-02-07 13:00:29Z jens $
"""

import copy
import ldap
import ldapurl

from Products.Five import BrowserView

_marker = ()


class ServersView(BrowserView):
    """ The ZMI Configuration view 
    """

    def __call__(self):
        """ Render the view
        """
        submitted = self.request.method.lower() == 'post'
        if submitted:
            if 'host' in self.request.form.keys():
                self.add()
            elif 'svr_remove' in self.request.form.keys():
                self.remove()

        super_view = super(ServersView, self)
        if getattr(super_view, '__call__', None) is not None:
            return super_view.__call__()

    def getServers(self):
        """ Get the server definitions for display
        """
        servers = copy.copy(self.context.servers.values())

        for server in servers:
            try:
                test_conn = self.context._connect(server['url'])
                test_conn.simple_bind_s( self.context.bind_dn
                                       , self.context.bind_pwd
                                       )
                test_conn.unbind()
                server['status'] = 'OK'
            except ldap.LDAPError, e:
                server['status'] = repr(e)

        return servers

    def getConnectedServer(self):
        """ Return the URL for the currently connected LDAP server
        """
        conn = self.context._getConnection()
        return getattr(conn, '_uri', '-- not connected --')

    def add(self):
        """ Add a server definition
        """
        req = self.request
        self.context.addServer( req.get('host')
                              , req.get('port', '389')
                              , req.get('protocol', 'ldap')
                              , req.get('connection_timeout', 5)
                              , req.get('operations_timeout', -1)
                              )
        self.context._p_changed = True
        req.set('manage_tabs_message', 'LDAP server definition added.')

    def remove(self):
        """ Remove a server definition
        """
        identifiers = self.request.get('identifiers', _marker)
        if not identifiers:
            self.request.set( 'manage_tabs_message'
                            , 'No server definition selected.'
                            )
            return

        for identifier in identifiers:
            ldap_url = ldapurl.LDAPUrl(identifier)
            if ':' in ldap_url.hostport:
                host, port = ldap_url.hostport.split(':')
            else:
                host = ldap_url.hostport
                port = '389'
            self.context.removeServer(host, port, ldap_url.urlscheme)
        self.context._p_changed = True

        self.request.set( 'manage_tabs_message'
                        , 'LDAP server definitions removed.'
                        )

