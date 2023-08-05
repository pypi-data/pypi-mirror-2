String encoding issues
======================

LDAP servers expect values sent to them in specific string encodings.
Standards-compliant LDAP servers use UTF-8. They use the same encoding 
for values returned e.g. by a search. This server-side encoding may not 
be convenient for communicating with the :mod:`Products.LDAPConnector` 
API itself. For this reason the server-side encoding and API encoding 
can be set individually on connection instances using the attributes 
``ldap_encoding`` and ``api_encoding``, respectively. The connection 
instance handles all string encoding transparently.

By default, instances use UTF-8 as ``ldap_encoding`` and ISO-8859-1 
(Latin-1) as ``api_encoding``. You can assign any valid Python codec 
name to these attributes. Assigning an empty value or None means that 
unencoded unicode strings are used.

If you receive error messages and tracebacks for either 
``UnicodeDecodeError`` or ``UnicodeEncodeError`` while searching 
for records on the :term:`ZMI` ``Test`` tab or while displaying 
LDAPConnector search results in your own web application using 
Zope Page Templates, you have several places to look at:

- Make sure the LDAPConnector ``ldap_encoding`` value, visible on 
  the :term:`ZMI` ``Configuration`` tab as *LDAP server string encoding*, 
  is set to the encoding required by your LDAP server. For most servers 
  this will be UTF-8. With :term:`Active Directory` this may differ.

- Check the text encoding used by your web application. It will 
  usually be something like ``iso-8859-1`` or ``utf-8``. Make sure 
  it matches the LDAPConnector ``api_encoding`` value, which is 
  set on the :term:`ZMI` ``Configuration`` tab as *API string encoding*.
  If you leave this field empty unencoded unicode is expected by 
  the API and will be returned by it.

- If your browser does not send along its preferred character 
  encoding when requesting data from your server (request header
  ``HTTP_ACCEPT_CHARSET``) Zope may pick the wrong text encoding. 
  Safari-based browsers like Safari or Omniweb show this behavior. 
  You can influence which encoding gets picked by overriding a 
  :term:`ZCML` registration in your site's configuration. To use 
  the encoding defined as ``management_page_charset`` in your site, 
  add the following to your site configuration::

    <utility
      provides="Products.PageTemplates.interfaces.IUnicodeEncodingConflictResolver"
      component="Products.PageTemplates.unicodeconflictresolver.StrictUnicodeEncodingConflictResolver"
      />

