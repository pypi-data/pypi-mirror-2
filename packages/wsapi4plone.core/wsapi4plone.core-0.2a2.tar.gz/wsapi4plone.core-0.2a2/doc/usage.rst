Python Usage Examples (via the interpreter)
===========================================

Setup the client connection using :mod:`xmlrpclib` with basic authorization.

    >>> from xmlrpclib import ServerProxy
    >>> client = ServerProxy('http://user:password@localhost:8888/plone')

.. note:: The above URI is an example. The terms within it will likely
   need changed to suit ones needs. The url scheme is like so::

       (http|https)://[<username>:<password>@]<hostname>[:80|:<port>]/<site_name>

.. note:: Please take a look at the `wsapi4plone.client
   <http://pypi.python.org/pypi/wsapi4plone.client>`_ package if you are
   interested in cookie based authentication.

.. _query_example:

Finding what you're looking for
-------------------------------

We can use the ``query`` call to search for content in the site. This will also
allow us to get a full index of all the content objects in the site if we do not
provide any parameters.

    >>> q = client.query()
    >>> len(q)
    7
    >>> q
    {'/plone/front-page': {'CreationDate': '2007-04-02 15:28:30',
                           'Creator': 'admin',
                           'Date': '2009-08-19 09:56:50',
                           'Description': 'Congratulations! You have successfully installed Plone.',
                           'EffectiveDate': 'None',
                           'ExpirationDate': 'None',
                           'ModificationDate': '2009-08-19 09:56:50',
                           'Subject': [],
                           'Title': 'Welcome to Plone',
                           'Type': 'Page',
                           'UID': '07f20e423b6ca478eb8691ff816b83a3',
                           'container': False,
                           'created': <DateTime ...>,
                           'effective': <DateTime ...>,
                           'expires': <DateTime ...>,
                           'id': 'front-page',
                           'listCreators': ['admin'],
                           'modified': <DateTime ...>,
                           'review_state': 'published',
                           'size': '4.9 kB'}, ... }

We can also pass criteria to the query call in the form of a dictionary. The
``query`` call is simply an abstraction of the Plone portal_catalog's search
method. Therefore, you can look at the `Plone Manual's Querying section
<http://plone.org/documentation/manual/plone-community-developer-documentation/searching-and-indexing/query>`_
for more information on the possible calls to the portal_catalog. The query call uses a dictionary of keyword arguments. A basic example would look like::

    >>> q = client.query({'Title': "Users"})
    >>> q.keys()
    ['/plone/Members']

.. note:: Where Title in the above case would normally be a keyword argument
   like ``search(Title="Users")`` it needs to be a dictionary of keyword
   arguments to pass through the XML-RPC parts of the Zope2 Publisher.

.. _get_object_example:

Get a content object
--------------------

To get information about the site (or the current calling location based on the
URL used to instantiate the client) use the ``get_object`` call without any
parameters.

    >>> site_object = client.get_object()
    >>> site_object
    {'/plone': [{'description': '', 'id': 'plone', 'title': 'Site'},
                'Plone Site',
                {'contents': {'/plone/Members': {'CreationDate': '2009-08-19 09:56:50',
                                                 'Creator': 'admin',
                                                 'Date': '2009-08-19 09:56:51',
                                                 'Description': "Container for users' home directories",
                                                 'EffectiveDate': 'None',
                                                 'ExpirationDate': 'None',
                                                 'ModificationDate': '2009-08-19 09:56:51',
                                                 'Subject': [],
                                                 'Title': 'Users',
                                                 'Type': 'Large Folder',
                                                 'UID': '6e22e44bbe5581e10e3ff4913cebf83a',
                                                 'container': True,
                                                 'created': <DateTime ...>,
                                                 'effective': <DateTime ...>,
                                                 'expires': <DateTime ...>,
                                                 'id': 'Members',
                                                 'listCreators': ['admin'],
                                                 'modified': <DateTime ...>,
                                                 'review_state': 'published',
                                                 'size': '1 kB'}, ... }]}

Analyzing the results
~~~~~~~~~~~~~~~~~~~~~

The ``get_object`` call will return data in a dictionary that is keyed by
absolute path within the Zope2 instance. The value of each key is a list of
three items. The items are loosely referred as the following and will appear
in a Python list in the specified order.

:schema:  The schema isn't exactly a schema, but for lack of a better term has
          been called such. The data is a dictionary of the content object's
          attribute name and value. Further information about the schema can be
          determined by using the :ref:`get_schema_def` call
          and the content's type name.

:type: The type is a string that represents the content-type of the object. The
       type name is derived from the name that has been registered in `Plone's
       portal_types tool
       <http://plone.org/documentation/manual/plone-community-developer-documentation/content/types>`_.

:extensions: This third value will always be available, but may return an empty
             dictionary when there are no extensions for the object that has
             been requested. When an extension is available, it will appear in
             the dictionary, keyed by its registered name. You will need to
             consult the particular extension's documentation to understand the
             out/input structure. Extensions can be written to provide support
             for information that is secondary to the object's true purpose
             (e.g. getting/setting the default page view). Extensions are
             usually content-type specific, but can be global in scope.  See the
             :ref:`contents_extension` for a more in-depth explanation of how
             extensions work. If you are interested in extending the WSAPI, take
             a look at :ref:`extensions_development`.

Get specific content objects by path
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To be more specific about which objects you want returned, you can provide a
list of paths to ``get_object``. The path can be relative to the xmlrpclib
initialization location or absolute. However, everything will always be returned
with the absolute path, no matter if you use relative paths or not.

In the following example we use both relative and absolute URLs to get the
*Members* container object and the *front-page* document object.

    >>> objs = client.get_object(['Members', '/plone/front-page'])
    >>> len(objs)
    2
    >>> objs.keys()
    ['/plone/front-page', '/plone/Members']

.. _put_object_example:

Put or update information on a content object
---------------------------------------------

To put (as in the HTTP PUT method) or update information in an existing content
object, we pass the ``put_object`` call. A dictionary of keyed paths that are
valued with a list of schema and type information is provided as a single
parameter. In short, you can do a :ref:`get_object_def` call and change/update the results, then simply pass those results back into ``put_object``. Let's take a look at an example that changes the text body of the *front-page* object using the :ref:`get_object_def` shortcut.

    >>> frontpage = client.get_object(['/plone/front-page'])
    >>> schema = frontpage['/plone/front-page'][0]

At this point we have the schema of the object. We could drop everything except the fields that have been modified, but in this case we will just send back the entire object.

    >>> schema['text'] = "Once a new technology starts rolling, \
    ... if you're not part of the steamroller, you're part of the road. \
    ... --Stewart Brand"
    >>> frontpage['/plone/front-page'][0] = schema
    >>> updated_objects = client.put_object(frontpage)
    >>> updated_objects
    ['/plone/front-page']

And now let's check the *front-page* has been updated.

    >>> updated_frontpage = client.get_object(updated_objects)
    >>> updated_frontpage['/plone/front-page'][0]['text']
    "Once a new technology starts rolling, if you're not part of the steamroller, you're part of the road. --Stewart Brand"

.. _post_object_example:

Post a new content object
-------------------------

To create or post (as in HTTP POST method) a piece of content to a Plone site
you would use ``post_object``, which is almost the same as
:ref:`put_object_def`. The only difference between the two calls is that the
type (a.k.a. content-type) is optional with :ref:`put_object_def`, but not with
``post_object``. Also, it should be noted that it is your responsibility to
provide any required attributes, as ``post_object`` does not verify you have
providing values for required attributes.

Knowing what content-types are available
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Since ``post_object`` requires you to provide a type, where do you find out what
types are available? The :ref:`get_types_def` call is for this very purpose.
Here is a quick example:

    >>> client.get_types()
    [['Document', 'Page'],
     ['Event', 'Event'],
     ['Favorite', 'Favorite'],
     ['File', 'File'],
     ['Folder', 'Folder'],
     ['Image', 'Image'],
     ['Link', 'Link'],
     ['News Item', 'News Item'],
     ['Topic', 'Collection'],
     ['MyFolder', 'MyFolder']]

.. seealso:: Look at :ref:`get_types_example` for more information about
   :ref`get_types_def`.

.. _required_fields_inspection_example:

Getting the required fields of a content-type
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Before you create new content object it is helpful to know what attributes the
content-type has. To do that we can use ``get_schema``, which will return the
attributes and meta-data about those attributes for the requested content-type.
Here is a quick example for the *Link* schema and how to determine its required
attributes:

    >>> link_schema = client.get_schema('Link')
    >>> [ x for x in link_schema if link_schema[x]['required'] ]
    ['remoteUrl', 'title']

.. seealso:: Look at :ref:`get_schema_example` for more information about
   :ref:`get_schema_def`.

.. _post_object_example_create:

Creating the content
~~~~~~~~~~~~~~~~~~~~

To create objects we need to give ``post_object`` the same data structure you
give to :ref:`put_object_def` and receive from :ref:`get_object_def`. Recall
from the :ref:`get_object_example`, objects are keyed by absolute path, which
means that our ``post_object`` parameter data structure is a dictionary of path
keys and object values. The key of the dictionary will be the to-be-created
object identifier or ID. Everything else is relatively straight forward, since
it is so similar to :ref:`put_object_def`. Let's take a look at an example where
we create a *Link* content object to the PSU WebLion website.

    >>> weblion = {'/plone/weblion': [
    ...    {'title': 'PSU WebLion',
    ...     'remoteUrl': 'http://weblion.psu.edu/'},
    ...    'Link']
    ...    }
    >>> object_path = client.post_object(weblion)

.. note:: We could have used the relative path ``weblion`` as the key rather
   than the absolute path. 

Now if we retrieve the object, we will find that it has a bunch of other attributes that we did not set that are automatically set by Plone and Zope.

    >>> weblion = client.get_object(object_path)
    >>> weblion
    {'/plone/weblion': [{'allowDiscussion': False,
                         'contributors': [],
                         'creation_date': <DateTime ...>,
                         'creators': ['admin'],
                         'description': '',
                         'effectiveDate': None,
                         'excludeFromNav': False,
                         'expirationDate': None,
                         'id': 'weblion',
                         'language': '',
                         'location': '',
                         'modification_date': <DateTime ...>,
                         'relatedItems': [],
                         'remoteUrl': 'http://weblion.psu.edu/',
                         'rights': '',
                         'subject': [],
                         'title': 'PSU WebLion'},
                        'Link',
                        None]}

.. _delete_object_example:

Delete a content object
-----------------------

The ``delete_object`` does exactly as the name would suggest, deletes objects.
To use ``delete_object``, you pass it a list of paths, much like the list of
paths used with :ref:`get_object_def`. Like the other calls, the paths can be
absolute or relative to the client instantiation URL. Let's try
``delete_object`` by deleting the *Members* folder and the *events* collection.

    >>> client.delete_object(['Members','/plone/events'])

.. _get_types_example:

Get the available content-types
-------------------------------

Plone comes with a nice variety of content-types; and this is one of the reasons
it is such a powerful system. To list all the content-types available in a Plone site we can use ``get_types``. In addition, you can provide the call with a path to a container object, which will allow you to discover the addible content-types for that container. Let's take a look at the types that can be added to the current call location (the site root) and the ``news`` object (a *Large Plone Folder*).

    >>> client.get_types()
    [['Document', 'Page'],
     ['Event', 'Event'],
     ['Favorite', 'Favorite'],
     ['File', 'File'],
     ['Folder', 'Folder'],
     ['Image', 'Image'],
     ['Link', 'Link'],
     ['News Item', 'News Item'],
     ['Topic', 'Collection'],
     ['MyFolder', 'MyFolder']]
    >>> client.get_types('/plone/news')
    [['News Item', 'News Item']]

.. _get_schema_example:

Get a content object's structure
--------------------------------

You usually want a blue print or schematic before trying to start an engineering
project. The same usually holds true for content objects, because not all
content has the same shape or function. The ``get_schema`` call helps to
determine the schema of a content-type. The schema is basically a blue print for
the object. The call returns a dictionary of object attributes and there
meta-data for the requested content-type.

.. note:: The current implementation provides a dictionary of two key value
   pairs (required and type) as the attribute meta-data. Future versions of this
   package may also provide default values, permission information and
   vocabularies and/or sources.

Let's take a look at the schema for an *Image* content-type.

    >>> image_schema = client.get_schema('Image')
    >>> image_schema
    {'allowDiscussion': {'required': False, 'type': 'boolean'},
     'contributors': {'required': False, 'type': 'lines'},
     'creation_date': {'required': False, 'type': 'datetime'},
     'creators': {'required': False, 'type': 'lines'},
     'description': {'required': False, 'type': 'text'},
     'effectiveDate': {'required': False, 'type': 'datetime'},
     'excludeFromNav': {'required': False, 'type': 'boolean'},
     'expirationDate': {'required': False, 'type': 'datetime'},
     'id': {'required': 0, 'type': 'string'},
     'image': {'required': True, 'type': 'image'},
     'language': {'required': False, 'type': 'string'},
     'location': {'required': False, 'type': 'string'},
     'modification_date': {'required': False, 'type': 'datetime'},
     'relatedItems': {'required': False, 'type': 'reference'},
     'rights': {'required': False, 'type': 'text'},
     'subject': {'required': False, 'type': 'lines'},
     'title': {'required': False, 'type': 'string'}}

.. note:: ``get_schema`` takes a path parameter in addition to the content-type
   name, because sometimes there are type constraints on content and content
   containers.

.. _get_workflow_example:

Get a content object's workflow state
-------------------------------------

You can only go so far with creating and updating content before, for instance,
you need to transition the content object from a private state to a public
state. To obtain the transition information, you use``get_workflow``, which
returns a dictionary with two bits of information:

#. The current workflow *state* of the content
#. The available *transition(s)* the authenticated user can perform

Let's take a look at the *weblion* object we created in
:ref:`post_object_example_create`.

    >>> client.get_workflow('weblion')
    {'state': 'private', 'transitions': ['submit', 'publish']}

.. _set_workflow_example:

Transition a content object's workflow state
--------------------------------------------

Using :ref:`get_workflow_def` has provided you with available transitions that
can be perform on the requested content object. We can now use ``set_workflow``
to transition the workflow state of the object. Let's *publish* the *weblion*
object that was create in :ref:`post_object_example_create`. In this example the
second parameterーa pathーis optional and will default to the client call
location.

    >>> client.set_workflow('publish', 'weblion')
    >>> client.get_workflow('weblion')
    {'state': 'published', 'transitions': ['retract', 'reject']}

.. _get_discussion_example:

Get a content object's discussion container
-------------------------------------------

Use ``get_discussion`` to get the discussion container (a.k.a. comments
container) of a content object with the full or relative path to the object.

    >>> client.get_discussion('weblion')
    {'1257246779': {'in_reply_to': '1257246760',
                    'cooked_text': 'a comment on comment 1',
                    'title': 'comment 1.1',
                    'created': '2009-11-03 12:12:59',
                    'text': 'a comment on comment 1',
                    'creators': ('admin',)},
     '1257246760': {'in_reply_to': '',
                    'cooked_text': 'the first comment!',
                    'title': 'comment 1',
                    'created': '2009-11-03 12:12:40',
                    'text': 'the first comment!',
                    'creators': ('admin',)},
     '1257246799': {'in_reply_to': '',
                    'cooked_text': 'another comment',
                    'title': 'comment 2',
                    'created': '2009-11-03 12:13:19',
                    'text': 'another comment',
                    'creators': ('admin',)}
     }

.. _binary_data_example:

Working with binary data
------------------------

Receiving binary data through the Web Services API is typically marshalled to
a binary object. In Python, XML-RPC binary data is marshaled to
a :class:`xmlrpclib.Binary` object (see :mod:`xmlrpclib`). 

To illustrate how this works, we'll use the `get_object` call on an Image
object at ``/plone/images/an-image``.
::

    >>> client.get_object(['images/an-image'])
    {'/Plone/images/an-image': [{'allowDiscussion': False,
                                 'contributors': [],
                                 'creation_date': <DateTime ...>,
                                 'creators': ['admin'],
                                 'description': '',
                                 'effectiveDate': None,
                                 'excludeFromNav': False,
                                 'expirationDate': None,
                                 'id': 'an-image',
                                 'image': {'alt': 'An Image',
                                           'content_type': 'image/jpeg',
                                           'data': <xmlrpclib.Binary ...>,
                                           'height': 464,
                                           'size': 31503,
                                           'title': 'An Image',
                                           'width': 600},

                                 'language': 'en',
                                 'location': '',
                                 'modification_date': <DateTime ...>,
                                 'relatedItems': [],
                                 'rights': '',
                                 'subject': [],
                                 'title': 'An Image'},
                                'Image',
                                {}]}

Sending binary data has similar needs to receiving it. The XML-RPC library
needs to know how to marshall the content to a XML-RPC Binary type (see the
`XML-RPC specification <http://www.xmlrpc.com/spec>`_ for details about
the base64/binary type). In Python, :mod:`xmlrpclib` will marshall
:class:`xmlrpclib.Binary` to the appropriate request format. Here is an
example of how to add a PDF to Plone using the web services API::

    >>> from xmlrpclib import Binary
    >>> f = open('example.pdf', 'r')
    >>> binary_data = Binary(f.read())
    >>> f.close()
    >>> pdf_object = {'file': binary_data, 'title': "Example PDF"}
    >>> example_pdf = client.post_object({'example-pdf': [pdf_object, 'File']})
    >>> client.get_object(example_pdf)
    {'/plone/example-pdf': [{'allowDiscussion': False,
                             'contributors': [],
                             'creation_date': <DateTime ...>,
                             'creators': ['admin'],
                             'description': '',
                             'effectiveDate': None,
                             'excludeFromNav': False,
                             'expirationDate': None,
                             'file': {'content_type': 'application/pdf',
                                      'data': <xmlrpclib.Binary ...>,
                                      'height': 0,
                                      'size': 269894,
                                      'title': 'Example PDF',
                                      'width': 0},
                             'id': 'example-pdf',
                             'language': 'en',
                             'location': '',
                             'modification_date': <DateTime ...>,
                             'relatedItems': [],
                             'rights': '',
                             'subject': [],
                             'title': 'Example PDF'},
                            'File',
                            {}]}

Common gotcha
~~~~~~~~~~~~~

Notice in the above example, that the file key in the
creation dictionary (``pdf_object``) does not contain a dictionary
like the response from the :ref:`get_object_def` call.

The web services API will not except a dictionary
for binary data fields.
This is a common gotcha, because in most cases
the results of a :ref:`get_object_def` can
be passed directly into a :ref:`put_object_def`
or :ref:`post_object_def` call without issue.

.. note:: The handling of binary data will likely change in future versions of
   wsapi4plone.core.

To inspect an object for binary data fields,
use the :ref:`get_schema_def` call
and evaluating the field's type value
(see also :ref:`required_fields_inspection_example`).

Working with dates and times
----------------------------

Similar to :ref:`binary_data_example`, XML-RPC supports a date and time type.
In Python, :mod:`xmlrpclib` marshalls dates and times to
:class:`xmlrpclib.DateTime`
(or Python's :mod:`datetime` type depending
on whether :class:`xmlrpclib.ServerProxy` is instantiated
with ``use_datetime=True``).

.. note:: It is easier to use Python's :mod:`datetime` type rather than
   the :mod:`xmlrpclib` datetime type.

To inspect an object for datetime fields,
use the :ref:`get_schema_def` call
and evaluating the field's type value
(see also :ref:`required_fields_inspection_example`).
For example, a Link content-type has a few datetime fields::

    >>> link_schema = client.get_schema('Link')
    >>> [f for f in link_schema if link_schema[f]['type'] == 'datetime']
    ['modification_date', 'creation_date', 'effectiveDate', 'expirationDate']

Here is an example Link (at ``example-link``) output. Notice that
:mod:`xmlrpclib` has marshalled the datetime field result
to a :class:`xmlrpclib.DateTime` object.

::

    >>> client.get_object(['example-link'])
    {'/plone/example-link': [{'allowDiscussion': False,
                              'contributors': [],
                              'creation_date': <DateTime '2010-05-27T11:23:14-04:00' at ...>,
                              ...
                              'title': 'example.come'},
                             'Link',
                             {}]}

To update a datetime field simply send it in a format
that the XML-RPC library can marshall.
In Python, an example for updating the creation date would look like this::

    >>> from xmlrpclib import DateTime
    >>> creation_date = DateTime('20110527T11:30:26')
    >>> link_object = {'creation_date': creation_date}
    >>> example_link = client.put_object({'example-link': [link_object, 'Link']})
    >>> client.get_object(example_link)
    {'/plone/example-link': [{'allowDiscussion': False,
                              'contributors': [],
                              'creation_date': <DateTime '2011-05-27T11:30:26' at ...>,
                              ...
                              'title': 'example.come'},
                             'Link',
                             {}]}

.. note:: You may notice fields that have a datetime string. These fields
   have not marshalled to an XML-RPC DateTime object because Plone stores them
   as strings.
