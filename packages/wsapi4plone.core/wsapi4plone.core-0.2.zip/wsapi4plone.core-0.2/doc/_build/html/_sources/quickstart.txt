Quick Start with the Python Interpreter
=======================================

.. _quickstart_connection_setup:

Set up a connection
-------------------

The Python standard library comes with the :mod:`xmlrpclib` module, which
we can use to connect to the Plone site (e.g. at localhost:8080). We'll say a
user with the following credentials has been setup in the Plone
site:

:site: Plone
:user: monty
:password: python
:role: Manager

And we will use BasicAuth to authenticate.

    >>> from xmlrpclib import ServerProxy
    >>> server = ServerProxy("http://monty:python@localhost:8080/Plone")

.. note:: It is not recommended that you use BasicAuth on a production site.
   Please be aware that using BasicAuth will send the password in clear text.

Basic example
-------------

The API is designed around the HTTP methods. Therefore, the HTTP methods can
in most cases be translated to ``<method>_object`` for the XML-RPC calls.
For example, the HTTP GET method can be translated to ``get_object`` and
works in a similar manor. An example of this in action might look like::

    >>> server.get_object()
    {'/Plone': [{'description': '', 'id': 'Plone', 'title': 'Site'},
                'Plone Site',
                {'contents': {...}
                }]}

And the XML for the above response would look like this::

    <methodResponse>
      <params>
        <param>
          <value><struct>
            <member>
              <name>/Plone</name>
              <value><array><data>
                <value>
                  <struct>
                    <member>
                      <name>title</name>
                      <value><string>Site</string></value>
                    </member>
                    <member>
                      <name>description</name>
                      <value><string></string></value>
                    </member>
                    <member>
                      <name>id</name>
                      <value><string>Plone</string></value>
                    </member>
                  </struct>
                </value>
                <value><string>Plone Site</string></value>
                <value>
                  <struct>
                    <member>
                      <name>content</name>
                      <value><struct>...</struct></value>
                    </member>
                  </struct>
                </value>
              </data></array></value>
            </member>
          </struct></value>
        </param>
      </params>
    </methodResponse>

The contents of the response are in a XML-RPC struct (equivalent to a Python
dictionary). The keys of this struct are the requested paths; and since none
where provided, the calling location is used by default.

The pairing value in the struct is an XML-RPC array. The array has three values:
1) a struct of properities 2) The content-type string 3) A struct of
miscellaneous data for a particular content-type.

More information
----------------

The quick start documentation provided here does not provide a complete
reference for the API, but should give the user, possibly you, a brief look at
the behavior and structure of the API. Have a look at the :doc:`usage`
information for a more in-depth explanation of how the API works.
