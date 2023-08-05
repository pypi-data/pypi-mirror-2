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
""" Persistent Zope2 LDAP connection

$Id: LDAPConnector.py 1882 2010-02-01 12:52:24Z jens $
"""

import uuid

from dataflake.ldapconnection.connection import LDAPConnection
from dataflake.ldapconnection.interfaces import ILDAPConnection

from AccessControl import ClassSecurityInfo
from Acquisition import aq_base
from App.class_init import default__class_init__ as InitializeClass
from OFS.SimpleItem import SimpleItem
from zope.interface import implements

from Products.LDAPConnector.utils import cachedSearch
from Products.LDAPConnector.utils import invalidateCache


class LDAPConnector(LDAPConnection, SimpleItem):
    """ Persistent representation of the LDAPConnection class
    """
    security = ClassSecurityInfo()
    meta_type = 'LDAPConnector'
    implements(ILDAPConnection)

    manage_options = (
        ( {'label': 'Configuration', 'action': 'manage_main'}
        , {'label': 'Servers', 'action': 'manage_servers'}
        , {'label': 'Cache', 'action': 'manage_cache'}
        , {'label': 'Test', 'action': 'manage_search'}
        ) + SimpleItem.manage_options
    )

    # Security overrides for methods inherited from the LDAPConnection class
    security.declarePrivate( 'addServer'
                           , 'logger'
                           , 'removeServer'
                           , 'connect'
                           , 'search'
                           , 'delete'
                           , 'insert'
                           , 'modify'
                           )

    def __init__(self, id, title=''):
        super(LDAPConnector, self).__init__()
        self.id = id
        self.title = title
        self.hash = uuid.uuid4()
        self.timeout = 600

    search = cachedSearch(LDAPConnection.search)
    modify = invalidateCache(LDAPConnection.modify)
    delete = invalidateCache(LDAPConnection.delete)

InitializeClass(LDAPConnector)


def manage_addLDAPConnector(self, id, title='', REQUEST=None):
    """ Called when adding an instance in the Zope2 ZMI
    """
    container = self.this()
    container_url = container.absolute_url()

    if getattr(aq_base(container), id, None) is not None:
        msg = 'Duplicate ID, please choose another.'
        goto = container_url
    else:
        container._setObject(id, LDAPConnector(id, title))
        msg = 'Created LDAPConnector instance %s.' % id
        goto = '%s/%s' % (container_url, id)

    if REQUEST is not None:
        qs = 'manage_tabs_message=%s' % msg
        REQUEST.RESPONSE.redirect('%s/manage_main?%s' % (goto, qs))

