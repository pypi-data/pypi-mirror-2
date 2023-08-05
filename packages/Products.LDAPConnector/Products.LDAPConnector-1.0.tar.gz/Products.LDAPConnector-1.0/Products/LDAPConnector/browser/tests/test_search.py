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
""" LDAPConnector search browser view tests

$Id: test_search.py 1904 2010-02-07 22:14:32Z jens $
"""

import unittest

from Products.LDAPConnector.browser.tests.base import ViewTests

class SearchViewTests(ViewTests):

    def _getTargetClass(self):
        from Products.LDAPConnector.browser.search import \
            SearchView
        return SearchView

    def test_defaults(self):
        self.failIf(self.view.status)
        self.failIf(self.view.results)

    def test_missing_input(self):
        self.conn.addServer('host', 389, 'ldap')

        self.view()

        self.assertEquals( self.view.status
                         , 'Not enough search criteria provided'
                         )

    def test_search_error(self):
        self.conn.addServer('host', 389, 'ldap')
        self.request.method = 'POST'
        self.request.form['searchbase'] = 'o=base'
        self.request.form['fltr'] = '(objectClass=*)'

        self.view()

        self.assertEquals(self.view.status, "NO_SUCH_OBJECT('o=base',)")

    def test_search_nomatch(self):
        self.conn.addServer('host', 389, 'ldap')
        self.request.method = 'POST'
        self.request.form['searchbase'] = 'dc=localhost'
        self.request.form['fltr'] = '(objectClass=*)'

        self.view()

        self.assertEquals(self.view.status, 'No matching results.')

    def test_search_success(self):
        self.conn.addServer('host', 389, 'ldap')
        foo_attrs = { 'cn': 'foo'
                    , 'objectClass': ['top', 'person']
                    }
        self.conn.insert('dc=localhost', 'cn=foo', attrs=foo_attrs)
        self.request.method = 'POST'
        self.request.form['searchbase'] = 'dc=localhost'
        self.request.form['fltr'] = '(cn=foo)'

        self.view()

        self.assertEquals(len(self.view.results), 1)
        res = self.view.results[0]
        self.assertEquals(res['dn'], 'cn=foo,dc=localhost')
        self.assertEquals(res['cn'], 'foo')
        self.assertEquals(res['objectClass'], 'top, person')
        self.assertEquals(set(res['attributes']), set(['cn', 'objectClass']))
       
    def test_search_binaryvalues(self):
        self.conn.addServer('host', 389, 'ldap')
        foo_attrs = { 'cn': 'foo'
                    , 'objectGUID;binary': 'guid'
                    , 'jpegPhoto;binary': ['photo1', 'photo2']
                    }
        self.conn.insert('dc=localhost', 'cn=foo', attrs=foo_attrs)
        self.request.method = 'POST'
        self.request.form['searchbase'] = 'dc=localhost'
        self.request.form['fltr'] = '(cn=foo)'

        self.view()

        self.assertEquals(len(self.view.results), 1)
        res = self.view.results[0]
        self.assertEquals(res['dn'], 'cn=foo,dc=localhost')
        self.assertEquals(res['cn'], 'foo')
        self.assertEquals(res['objectGUID'], '(binary data, 4 bytes)')
        self.assertEquals(res['jpegPhoto'], '(binary data, 12 bytes)')
        self.assertEquals( set(res['attributes'])
                         , set(['cn', 'objectGUID', 'jpegPhoto'])
                         )

    def test_search_stringencoding(self):
        from dataflake.ldapconnection.tests.dummy import ISO_8859_7_ENCODED
        self.conn.addServer('host', 389, 'ldap')
        self.conn.api_encoding = 'iso-8859-7'
        foo_attrs = { 'cn': 'foo'
                    , 'sn': ISO_8859_7_ENCODED
                    , 'gn': [ISO_8859_7_ENCODED, ISO_8859_7_ENCODED]
                    }
        self.conn.insert('dc=localhost', 'cn=foo', attrs=foo_attrs)
        self.request.method = 'POST'
        self.request.form['searchbase'] = 'dc=localhost'
        self.request.form['fltr'] = '(cn=foo)'

        self.view()

        self.assertEquals(len(self.view.results), 1)
        res = self.view.results[0]
        self.assertEquals(res['dn'], 'cn=foo,dc=localhost')
        self.assertEquals(res['cn'], 'foo')
        self.assertEquals(res['sn'], ISO_8859_7_ENCODED)
        self.assertEquals( res['gn']
                         , '%s, %s' % (ISO_8859_7_ENCODED, ISO_8859_7_ENCODED)
                         )
        self.assertEquals(set(res['attributes']), set(['cn', 'gn', 'sn']))


def test_suite():
    return unittest.TestSuite((
        unittest.makeSuite(SearchViewTests),
        ))

