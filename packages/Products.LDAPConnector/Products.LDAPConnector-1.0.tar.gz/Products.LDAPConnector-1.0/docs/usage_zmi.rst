Usage from the Zope ZMI
=======================

The following screen shots show how to use an LDAPConnector instance 
through the web in the :term:`Zope` :term:`ZMI`. 

To create a new LDAPConnector instance, choose *LDAPConnector* from 
the drop-down list at the top right.

.. image:: screen01.png

On the initial view you can set the ID and title.

.. image:: screen02.png

Once the instance is created you will end up on the ``Configuration`` 
tab where you can refine the configuration:

- The (optional) title can be chosen freely.

- The LDAP login and LDAP password fields allow you to specify LDAP 
  credentials that will be used to authenticate to the LDAP servers 
  set up in the next step. The same credentials will be used for all 
  physical LDAP server connections set up on the ``Servers`` 
  :term:`ZMI` tab.

- LDAP servers store text values in specific text encodings, usually
  UTF-8. You need to specify the encoding name in the LDAP server 
  string encoding field.

- The API string encoding field is used to specify the text encoding 
  applied to values returned by the LDAPConnector instance, as well 
  as the expected encoding for values passed in using the instance's
  API. If you leave this field empty no encoding will be used, which 
  means unencoded unicode.

- If you select the Read-only checkbox no writes to the LDAP server 
  will be allowed.

.. image:: screen03.png

On the ``Servers`` tab you define physical server connections. By 
defining more than one server you can achieve redundancy, which means 
the LDAPConnector will be usable even if one server is no longer 
reachable or returns an error.

To set up a server connection you need to provide the following:

- a hostname, IP of a filesystem path for UNIX domain sockets

- a port number (this field is ignored when using UNIX domain 
  sockets)

- the protocol to use, which can be ``ldap`` for unencrypted data 
  transmission, ``ldaps`` for encrypted traffic using LDAP over 
  SSL, ``ldaptls`` for negotiated encryption through the standard 
  unencrypted port, or ``ldapi`` when using UNIX domain sockets

- a connection timeout value in seconds for the initial connection
  setup, after which a server is considered dead

- an operations timeout value in seconds to set a maximum allowable 
  time for any operation, after which a server is considered dead

.. image:: screen04.png

When you have set up physical server connections you can see their 
status on the ``Server`` tab. 

.. image:: screen05.png

With servers defined and at least one of them showing status OK 
you are ready to run a simple search test. The ``Test`` tab 
requires basic knowledge about your LDAP tree structure so you 
can pick a node for the Search base value. When executing the 
search you will see the results listed at the bottom.

.. image:: screen06.png

By clicking on the plus icon or the DN the records can be examined 
in detail.

.. image:: screen07.png

Search records are cached. On the ``Cache`` tab you can set the
number of seconds each search and its results are cached. You 
can also view what's in the cache. From here, you can delete 
specific cache entries or flush the whole cache.

The cache works as a negative cache as well. Searches that return 
error messages or no results at all will be cached to avoid 
unnecessary work.

.. image:: screen08.png


