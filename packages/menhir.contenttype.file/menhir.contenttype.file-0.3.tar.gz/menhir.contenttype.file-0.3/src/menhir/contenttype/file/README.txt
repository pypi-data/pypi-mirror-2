***********************
menhir.contenttype.file
***********************

``menhir.contenttype.file`` provides a content type for `Dolmen` based
`Grok` applications.


Schema
======

The ``menhir.contenttype.file`` provides a very simple schema,
extending the `IDescriptiveSchema` interface, from ``dolmen.app.content``::

  >>> from dolmen.app.content import IDescriptiveSchema
  >>> from menhir.contenttype.file import IFile

  >>> IFile.isOrExtends(IDescriptiveSchema)
  True

The `IFile` interface describes the data field, that is to hold the
uploaded file or given bytes::

  >>> for attr, doc in IFile.namesAndDescriptions():
  ...   print attr, ':', doc
  data : <dolmen.file.field.FileField object at ...>

This `IFile` is directly provided by the `File` object, as defines it as
its schema::

  >>> from menhir.contenttype.file import File
  >>> from dolmen.content import Content

  >>> somefile = File(title=u"My nice file", data="Some file data")
  >>> IFile.providedBy(somefile)
  True

  >>> from dolmen.content import schema
  >>> IFile in schema.bind().get(somefile)
  True

  >>> somefile.title
  u'My nice file'


Storage
=======

The file uses a Blob storage for the data::

  >>> somefile.data
  <dolmen.blob.file.BlobValue object at ...>

  >>> print somefile.data.data
  Some file data


Icon
====

The content registers an icon, thanks to the ``dolmen.app.content``
package::

  >>> from zope.component import getMultiAdapter
  >>> from zope.publisher.browser import TestRequest

  >>> request = TestRequest()
  >>> icon = getMultiAdapter((somefile, request), name="icon")
  >>> print icon
  <zope.browserresource.icon.IconView object at ...>
