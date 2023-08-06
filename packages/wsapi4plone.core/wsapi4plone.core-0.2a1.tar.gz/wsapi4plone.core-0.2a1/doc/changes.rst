Changelog
=========

0.2a1 (2011-05-24)
------------------

- Use z3c.autoinclude to load ZCML *(cah190)*
- Rewrote the extensions (previously known as miscellaneous information)
  implementation to better support the collection's criteria use case.
  [ticket #2150] *(pumazi)*
- Refactored the tests. Created a number of base test cases classes to help
  modularize the tests. *(pumazi)*
- Fixed an logging error, where binary data was being output into the logs.
  *(pumazi)*

0.1.1 (2010-03-29)
------------------

- Transplanted the current documentation into Sphinx built documentation. And
  added more material. *(pumazi)*

0.1 (2009-12-01)
----------------

- Added the get_discussion call that gets all the Plone comments for the
  specified path. *(ramonski)*
- Fixed an issue with binary data where files ~> 2MB could not be Marshaled by
  the ZPublisher. *(pumazi)*
- Wrote a few more tests. *(pumazi)*
- Modified the get_types call to provide both the Id and Title, since some of
  the information that comes out of other calls could be using the Title rather
  than the Id. *(pumazi)*
- Patch submitted to convert the incoming xmlrpclib.DataTime object to a Zope
  DateTime object. *(Kevin Teague)*
- Added event notification for ObjectInitializedEvent and at_post_create_script
  calls. *(hans-peter.locher)*

0.1a3 (2009-08-24)
------------------

- Wrote some documentation. More will follow in the next release.
- Removed the Plone egg dependency, because it causes complications with
  Plone < 3.2.
- Rewrote the tests for the WSAPI calls.
- Fixed the get_workflow call to return only the transitions the current
  authenticated users can perform.
- Fixed a bug in the Plone service adapter's set_properties method, where the
  ISO 8601 format wasn't being parsed correctly.
- Removed a few lines that assume CMF type factories and management of objects.
  This part can be handled by the serviced container object's api, which
  abstracts the process of creation and deletion.
- The post_object call now derives the to-be-created object's id from the path.
- Modified the get_schema method to fix the Not Found? error. I'm not sure why
  it wasn't finding the object, but something tells me it has to do with it the
  transaction not completing.

0.1a2 (2009-07-29)
------------------

- Package name change from wsapi4plone to wsapi4plone.core.

0.1a1 (2009-07-08)
------------------

- Initial release.

