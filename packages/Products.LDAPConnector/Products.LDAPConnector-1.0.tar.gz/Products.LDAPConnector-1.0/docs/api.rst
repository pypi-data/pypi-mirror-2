.. _api_interfaces_section:

Interfaces
----------

Instances of ``Products.LDAPConnector`` derive from the 
:mod:`dataflake.ldapconnection.connection` module's 
``LDAPConnection`` class and implement the interface 
``dataflake.ldapconnection.interfaces.ILDAConnection``.
They mix in :term:`Zope` persistence to allow storage in 
the :term:`ZODB` object database.

.. autointerface:: dataflake.ldapconnection.interfaces.ILDAPConnection
