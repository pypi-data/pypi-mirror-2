Extensions
==========

.. The extensions implementation is not complete at this time, therefore this part of the documentation is excluded from the published documentation.

What is an extension?
---------------------

An extension is a plugin or extension for the API that allows one to add value
to the functionality the API provides without jamming functionality into the
core logic. An example extension might be to display information about the
default view for an object. This information isn't exactly core data to the
object itself, but would be useful to know and be able to change via the API.

Extensions provided with this package
-------------------------------------

.. _contents_extension:

Contents Extension
^^^^^^^^^^^^^^^^^^

.. _collections_criteria_extension:

Collections Criteria Extension
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. _extensions_development:

How to make an extension
------------------------

Extensions are multi-adapters that adapt a service object and a content object.
Extensions are named adapters that are registered via an (IInterface, what is
this called in human?). 
