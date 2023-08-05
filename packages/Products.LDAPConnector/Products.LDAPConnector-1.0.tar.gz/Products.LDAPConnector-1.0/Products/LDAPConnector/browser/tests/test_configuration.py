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
""" LDAPConnector configuration browser view tests

$Id: test_configuration.py 1894 2010-02-03 21:00:11Z jens $
"""

import unittest

from Products.LDAPConnector.browser.tests.base import ViewTests

class ConfigurationViewTests(ViewTests):

    def _getTargetClass(self):
        from Products.LDAPConnector.browser.configuration import \
            ConfigurationView
        return ConfigurationView

    def test_editing(self):
        self.request.form['title'] = 'New Title'
        self.request.form['bind_dn'] = 'cn=Manager,dc=localhost'
        self.request.form['bind_pwd'] = 'secret'
        self.request.form['read_only'] = 'on'
        self.request.form['ldap_encoding'] = 'iso-8859-7'
        self.request.form['api_encoding'] = ''
        self.request.form['submitted'] = 'submitted'

        self.view()

        self.failUnless(self.request.get('manage_tabs_message'))
        self.assertEquals(self.conn.title, 'New Title')
        self.assertEquals(self.conn.bind_dn, 'cn=Manager,dc=localhost')
        self.assertEquals(self.conn.bind_pwd, 'secret')
        self.assertEquals(self.conn.ldap_encoding, 'iso-8859-7')
        self.failIf(self.conn.api_encoding)
        self.failUnless(self.conn.read_only)

    def test_editing_bad_encoding(self):
        self.request.form['ldap_encoding'] = 'UNKNOWN'
        self.request.form['submitted'] = 'submitted'

        self.view()

        self.assertNotEquals(self.conn.ldap_encoding, 'UNKNOWN')
        self.assertEquals( self.request.get('manage_tabs_message')
                         , 'Unknown encoding "UNKNOWN"'
                         )


def test_suite():
    return unittest.TestSuite((
        unittest.makeSuite(ConfigurationViewTests),
        ))

