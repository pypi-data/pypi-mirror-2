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
""" ZMI Configuration view for Products.LDAPConnector

$Id: configuration.py 1894 2010-02-03 21:00:11Z jens $
"""

import codecs

from Products.Five import BrowserView

_marker = ()


class ConfigurationView(BrowserView):
    """ The ZMI Configuration view 
    """

    def __call__(self):
        """ Render the view
        """
        if self.request.get('submitted', _marker) != _marker:
            self.edit()

        super_view = super(ConfigurationView, self)
        if getattr(super_view, '__call__', None) is not None:
            return super_view.__call__()

    def edit(self):
        """ Change LDAPConnector settings
        """
        for key in ('title', 'bind_dn', 'bind_pwd', 'read_only'):
            setattr(self.context, key, self.request.get(key))

        for key in ('ldap_encoding', 'api_encoding'):
            value = self.request.get(key, _marker)
            if value:
                try:
                    codecs.lookup(value)
                    setattr(self.context, key, value)
                except LookupError:
                    msg = 'Unknown encoding "%s"' % value
                    self.request.set('manage_tabs_message', msg)
                    return
            elif value != _marker:
                setattr(self.context, key, value)

        self.request.set('manage_tabs_message', 'Settings changed.')
