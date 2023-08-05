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
""" LDAPConnector cache browser view tests

$Id: test_cache.py 1904 2010-02-07 22:14:32Z jens $
"""

import unittest

from Products.LDAPConnector.browser.tests.base import ViewTests

class CacheViewTests(ViewTests):

    def _getTargetClass(self):
        from Products.LDAPConnector.browser.cache import CacheView
        return CacheView

    def test_timeout_default(self):
        self.view()

        self.assertEquals(self.conn.timeout, 600)
        self.assertEquals(self.view.getCacheTimeout(), 600)

    def test_set_timeout(self):
        self.request.form['cache_timeout'] = '999'

        self.view()

        self.assertEquals(self.conn.timeout, 999)
        self.assertEquals(self.view.getCacheTimeout(), 999)

    def test_set_timeout_invalid(self):
        self.request.form['cache_timeout'] = 'INVALID'

        self.view()

        self.assertEquals(self.conn.timeout, 600)
        self.assertEquals(self.view.getCacheTimeout(), 600)
        self.failUnless(self.request.get('manage_tabs_message'))

    def test_invalidateItems_noneselected(self):
        self.request.form['invalidate_selected'] = 'on'

        self.view()

        self.assertEquals( self.request.get('manage_tabs_message')
                         , 'No records selected.'
                         )

    def test_invalidateItems(self):
        self.request.form['invalidate_selected'] = 'on'
        self.request.form['identifiers'] = ['1','2','3']

        self.view()

        self.assertEquals( self.request.get('manage_tabs_message')
                         , 'Records removed from cache.'
                         )

    def test_invalidateAll(self):
        self.request.form['invalidate_all'] = 'on'

        self.view()

        self.assertEquals( self.request.get('manage_tabs_message')
                         , 'Cache cleared.'
                         )

    def test_getCacheItems(self):
        import ldap
        self.conn.addServer('host', 389, 'ldap')
        self.failIf(self.view.getCacheItems())

        # Fill the cache by performing a search
        self.conn.search( 'dc=localhost'
                        , scope=ldap.SCOPE_BASE
                        , fltr='(objectClass=*)'
                        , bind_dn='cn=Manager,dc=localhost'
                        , bind_pwd='secret'
                        )

        cache_items = self.view.getCacheItems()
        self.assertEquals(len(cache_items), 1)
        cache_record = cache_items[0]
        self.assertEquals(cache_record['size'], 1)
        self.assertEquals(cache_record['exception'], '')
        self.assertEquals(cache_record['dns'], ['dc=localhost'])
        self.assertEquals(cache_record['bound_as'], 'cn=manager,dc=localhost')
        self.assertEquals(cache_record['base'], u'dc=localhost')
        self.assertEquals(cache_record['fltr'], u'(objectclass=*)')
        key = u'dc=localhost:::0:::(objectclass=*):::cn=manager,dc=localhost'
        self.assertEquals(cache_record['key'], key)


def test_suite():
    return unittest.TestSuite((
        unittest.makeSuite(CacheViewTests),
        ))

