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
""" Products.LDAPConnector initialization code

$Id: __init__.py 1882 2010-02-01 12:52:24Z jens $
"""

import os

def initialize(context):
    from App.Common import package_home
    from Products.LDAPConnector.LDAPConnector import LDAPConnector
    from Products.LDAPConnector.LDAPConnector import manage_addLDAPConnector
    from Products.PageTemplates.PageTemplateFile import PageTemplateFile

    _wwwdir = os.path.join(package_home(globals()), 'www')

    context.registerClass( LDAPConnector
                         , permission='LDAPConnector: add'
                         , constructors=( PageTemplateFile('add.pt', _wwwdir)
                                        , manage_addLDAPConnector
                                        )
                         , icon='www/ldapconnector.gif'
                         )

