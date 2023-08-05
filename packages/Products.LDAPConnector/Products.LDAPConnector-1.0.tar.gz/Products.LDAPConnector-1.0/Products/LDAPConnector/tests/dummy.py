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
""" LDAPConnector test dummy implementations

$Id: dummy.py 1882 2010-02-01 12:52:24Z jens $
"""

class DummyRequest:

    def __init__(self):
        self.form = {}
        self.RESPONSE = DummyResponse()

    def get(self, key, default=None):
        if key in self.form.keys():
            return self.form[key]

        return getattr(self, key, default)

    def set(self, key, value):
        setattr(self, key, value)

class DummyResponse:

    def __init__(self, *args, **kw):
        self.redirected = ''
    
    def redirect(self, url):
        self.redirected = url

