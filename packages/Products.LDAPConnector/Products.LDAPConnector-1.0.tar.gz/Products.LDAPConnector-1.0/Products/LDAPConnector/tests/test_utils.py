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
""" utility function tests

$Id: test_utils.py 1882 2010-02-01 12:52:24Z jens $
"""

import ldap
import unittest


class UtilityTests(unittest.TestCase):

    def test_getCache(self):
        from Products.LDAPConnector.utils import getCache
        from dataflake.cache.timeout import LockingTimeoutCache
        
        cache = getCache('testkey', 600)
        self.failUnless(isinstance(cache, LockingTimeoutCache))
        self.assertEquals(cache.getTimeout(), 600)

    def test_cachedSearch_decorator(self):
        dummy = Dummy('hash0')
        self.failIf(dummy.getCacheContents())

        dummy.must_cache('cachekey1')
        self.assertEquals( dummy.getCacheContents()
                         , [{'results': [{'dn': 'DN:cachekey1'}]}]
                         )

        dummy.must_cache('cachekey2')
        cache_contents = dummy.getCacheContents()
        self.assertEquals(len(cache_contents), 2)
        self.failUnless({'results': [{'dn': 'DN:cachekey1'}]} in cache_contents)
        self.failUnless({'results': [{'dn': 'DN:cachekey2'}]} in cache_contents)

    def test_cachedSearch_decorator_error(self):
        dummy = Dummy('hash1')
        self.failIf(dummy.getCacheContents())

        self.assertRaises(ldap.LDAPError, dummy.error_raiser, 'cachekey1')
        self.assertEquals( dummy.getCacheContents()
                         , [ { 'exception': "LDAPError('Ouch!',)"
                             , 'results': []
                             , 'size': 0
                             }
                           ]
                         )

    def test_invalidateCache_decorator(self):
        dummy = Dummy('hash2')
        self.failIf(dummy.getCacheContents())

        dummy.must_cache('cachekey1')
        dummy.must_cache('cachekey2')

        dummy.must_invalidate('DN:cachekey2')
        self.assertEquals( dummy.getCacheContents()
                         , [{'results': [{'dn': 'DN:cachekey1'}]}]
                         )

        dummy.must_invalidate('UNKNOWN KEY')
        self.assertEquals( dummy.getCacheContents()
                         , [{'results': [{'dn': 'DN:cachekey1'}]}]
                         )

        dummy.must_invalidate('DN:cachekey1')
        self.failIf(dummy.getCacheContents())


from Products.LDAPConnector.utils import cachedSearch
from Products.LDAPConnector.utils import getCache
from Products.LDAPConnector.utils import invalidateCache

class Dummy:
    
    def __init__(self, hash):
        self.hash = hash
        self.timeout = 30
        self.bind_dn = 'cn=Manager,dc=localhost'

    def getCacheContents(self):
        return getCache(self.hash, self.timeout).values()

    @cachedSearch
    def must_cache(self, key):
        val = {'results': [{'dn': 'DN:%s' % key}]}
        return val

    @cachedSearch
    def error_raiser(self, key):
        raise ldap.LDAPError('Ouch!')

    @invalidateCache
    def must_invalidate(self, key):
        pass
    

def test_suite():
    return unittest.TestSuite((
        unittest.makeSuite(UtilityTests),
        ))
