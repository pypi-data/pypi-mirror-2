Web Services API
================

.. _post_object_def:

post_object
-----------

    :Usage: ``post_object(params)``
    :Input: ``{ path: [{ attr: value, ...}, type_name], ...}``
    :Returns: ``[path, ...]``
    :Example: :ref:`post_object_example`

.. _put_object_def:

put_object
----------

    :Usage: ``put_object(params)``
    :Input: ``{ path: [{ attr: value, ...}, type_name], ...}``
    :Returns: ``[path, ...]``
    :Example: :ref:`put_object_example`

.. _get_object_def:

get_object
----------

    :Usage: ``get_object(path=[])``
    :Input: ``None | [path, ...]``
    :Returns: ``{ path: [{ attr: value, ...}, type_name, {misc_info: value}], ...}``
    :Example: :ref:`get_object_example`

.. _delete_object_def:

delete_object
-------------

    :Usage: ``delete_object(path=[])``
    :Input: ``None | [path, ...]``
    :Returns: ``None``
    :Example: :ref:`delete_object_example`

.. _query_def:

query
-----

    :Usage: ``query(filtr={})``
    :Returns: ``{ path: {index_id: value, ...}, ...}``
    :Example: :ref:`query_example`

.. _get_schema_def:

get_schema
----------

    :Usage: ``get_schema(type_name, path='')``
    :Returns: ``{ attr: {required: True | False, type: type_string, ...}, ...}``
    :Example: :ref:`get_schema_example`

.. _get_types_def:

get_types
---------

    :Usage: ``get_types(path='')``
    :Returns: ``[[type_id, type_title], ...]``
    :Example: :ref:`get_types_example`

.. _get_workflow_def:

get_workflow
------------

    :Usage: ``get_workflow(path='')``
    :Returns: ``{ state: current_state, transitions: [transition_name, ...], ...}``
    :Example: :ref:`get_workflow_example`

.. set_workflow_def:

set_workflow
------------

    :Usage: ``set_workflow(transition, path='')``
    :Returns: ``None``
    :Example: :ref:`set_workflow_example`

.. _get_discussion_def:

get_discussion
--------------

    :Usage: ``get_discussion(path='')``
    :Returns:

    ::

        {'id': {'in_reply_to': 'another_id',
                'title': '',
                'text': '',
                'cooked_text': '',
                'created': '2009-11-03 12:12:59',
                'creators': ()
                }, ...
         }

    :Example: :ref:`get_discussion_example`
