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
""" ZMI caching configuration view for Products.LDAPConnector

$Id: cache.py 1882 2010-02-01 12:52:24Z jens $
"""

from Products.Five import BrowserView
from Products.LDAPConnector.utils import getCache

_marker = ()


class CacheView(BrowserView):
    """ The ZMI Cache view 
    """

    def __call__(self):
        """ Render the view
        """
        timeout = self.request.get('cache_timeout', _marker)
        if timeout != _marker:
            self.setCacheTimeout(timeout)

        invalidation = self.request.get('invalidate_selected', _marker)
        if invalidation != _marker:
            self.invalidateItems(self.request.get('identifiers', []))

        invalidation = self.request.get('invalidate_all', _marker)
        if invalidation != _marker:
            self.invalidateAll()

        super_view = super(CacheView, self)
        if getattr(super_view, '__call__', None) is not None:
            return super_view.__call__()

    def setCacheTimeout(self, timeout):
        """ Change the lifetime for cached records
        """
        try:
            timeout = int(timeout)
        except ValueError:
            self.request.set('manage_tabs_message', 'Invalid timeout value.')
            return

        self.context.timeout = timeout
        cache = getCache(self.context.hash, timeout)
        cache.setTimeout(timeout)

        self.request.set('manage_tabs_message', 'Cache timeout changed.')

    def getCacheTimeout(self):
        """ Get the current cache timeout value
        """
        return getCache(self.context.hash, self.context.timeout).getTimeout()

    def getCacheItems(self):
        """ Get the cache contents
        """
        results = []
        raw_data = getCache(self.context.hash, self.context.timeout).items()

        for key, values in raw_data:
            base, scope, fltr, bound_as = key.split(':::')
            results.append( { 'key': key
                            , 'base': base
                            , 'scope': scope
                            , 'fltr': fltr
                            , 'bound_as': bound_as
                            , 'dns': [x['dn'] for x in values['results']]
                            , 'size': values['size']
                            , 'exception': values.get('exception', '')
                            } )
        return results

    def invalidateItems(self, identifiers):
        """ Invalidate specific cache values
        """
        if not identifiers:
            self.request.set('manage_tabs_message', 'No records selected.')
            return

        for key in identifiers:
            getCache(self.context.hash, self.context.timeout).invalidate(key)

        self.request.set('manage_tabs_message', 'Records removed from cache.')

    def invalidateAll(self):
        """ Clear out the cache
        """
        getCache(self.context.hash, self.context.timeout).invalidate()

        self.request.set('manage_tabs_message', 'Cache cleared.')

