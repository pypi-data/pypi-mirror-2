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
""" ZMI search view for Products.LDAPConnector

$Id: search.py 1904 2010-02-07 22:14:32Z jens $
"""

from dataflake.ldapconnection.utils import BINARY_ATTRIBUTES
import ldap

from Products.Five import BrowserView


class SearchView(BrowserView):
    """ The ZMI search view 
    """

    def __init__(self, context, request):
        super(SearchView, self).__init__(context, request)
        self.results = []
        self.status = ''

    def __call__(self):
        """ Render the view
        """
        self._do_search()
        super_view = super(SearchView, self)
        if getattr(super_view, '__call__', None) is not None:
            return super_view.__call__()
    
    def _do_search(self):
        """ Run a LDAP search against the active connection

        This method drives the ZMI `Test` tab. To prevent blowups 
        it will catch LDAP exceptions
        """
        searchbase = self.request.get('searchbase')
        searchscope = self.request.get('scope', 2)
        searchfilter = self.request.get('fltr')

        if searchbase and searchfilter:
            try:
                data = self.context.search( searchbase
                                          , searchscope
                                          , searchfilter
                                          )
                self.results = self._format_results(data['results'])

                if data.get('exception', None):
                    self.status = data['exception']
                elif data['size'] == 0:
                    self.status = 'No matching results.'
            except ldap.LDAPError, e:
                self.status = repr(e)
        else:
            self.status = 'Not enough search criteria provided'

    def _format_results(self, data):
        """ Helper to make the result output easier to display
        """
        for i in range(len(data)):
            record = data[i]
            for key, value in record.items():

                if key.lower() in BINARY_ATTRIBUTES:
                    if isinstance(value, (list, tuple)):
                        data_len = sum([len(x) for x in value])
                    else:
                        data_len = len(value)
                    record[key] = '(binary data, %i bytes)' % data_len
                    continue

                if isinstance(value, (list, tuple)):
                    record[key] = ', '.join(value)
                else:
                    record[key] = value

            non_dn_keys = [x for x in record.keys() if 
                                        x not in ('dn', 'attributes')]
            non_dn_keys.sort()
            record['attributes'] = non_dn_keys
            data[i] = record

        def tree_sort(item):
            dn_elements = ldap.dn.explode_dn(item['dn'])
            dn_elements.reverse()
            return dn_elements
        data.sort(key=tree_sort)

        return data

