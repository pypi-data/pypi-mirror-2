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
""" Products.LDAPConnector utility functions and definitions

$Id: utils.py 1904 2010-02-07 22:14:32Z jens $
"""

import ldap

from dataflake.cache.timeout import LockingTimeoutCache

# This mapping holds the search results cache
_CACHES = {}

def getCache(key, timeout):
    """ Get or create a cache object for the given key
    """
    if key not in _CACHES:
        _CACHES[key] = LockingTimeoutCache()
        _CACHES[key].setTimeout(timeout)
    return _CACHES[key]

def cachedSearch(func):
    """ Decorator to get results from the cache or cache new results
    """
    def _cached(*args, **kw):
        cache = getCache(args[0].hash, args[0].timeout)
        num_args = len(args)
        base = num_args > 1 and args[1] or kw.get('base')
        scope = num_args > 2 and args[2] or kw.get('scope')
        fltr = num_args > 3 and args[3] or kw.get('fltr')
        bound_as = ( num_args > 7 and args[8] or 
                     kw.get('bind_dn') or 
                     args[0].bind_dn )
        cache_key = '%s:::%s:::%s:::%s' % (base, scope, fltr, bound_as)

        result = cache.get(cache_key, default=None)
        if result is None:
            try:
                result = func(*args, **kw)
            except ldap.LDAPError, e:
                cache.set( cache_key
                         , { 'size': 0, 'results': [], 'exception': repr(e)}
                         )
                raise
            else:
                cache.set(cache_key, result)

        return result

    return _cached

def invalidateCache(func):
    """ Decorator to invalidate cache entries if they are changed
    """
    def _invalidate(*args, **kw):
        func(*args, **kw)

        cache = getCache(args[0].hash, args[0].timeout)
        dn = args[1]

        for key, value in cache.items():
            if dn in [x['dn'] for x in value['results']]:
                cache.invalidate(key)

        func(*args, **kw)

    return _invalidate

