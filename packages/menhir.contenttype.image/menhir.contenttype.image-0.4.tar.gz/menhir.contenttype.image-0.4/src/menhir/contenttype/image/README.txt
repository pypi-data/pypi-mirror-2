************************
menhir.contenttype.image
************************

``menhir.contenttype.image`` provides an image-centered content type
for `Dolmen` based `Grok` applications.

Schema
======

The ``menhir.contenttype.image`` `Image` content provides a custom schema,
extending the `IDescriptiveSchema` interface, from ``dolmen.app.content``::

  >>> from dolmen.app.content import IDescriptiveSchema
  >>> from menhir.contenttype.image import IImage

  >>> IImage.isOrExtends(IDescriptiveSchema)
  True

The `IImage` interface describes the image field, that is to store the
uploaded image data. The field comes from ``dolmen.file``::

  >>> for attr, doc in IImage.namesAndDescriptions():
  ...   print attr, ':', doc
  image : <dolmen.file.field.ImageField object at ...>


Factory
=======

The ``menhir.contenttype.image`` `Image` content uses a ZODB Blob to
store the data. The `image` attribute of the factory class, `Image`,
is a blob property from ``dolmen.blob``::

  >>> from menhir.contenttype.image import Image
  >>> Image.image
  <dolmen.blob.property.BlobProperty object at ...>

The instanciation is fairly straightforward::

  >>> import os.path
  >>> path = os.path.join(os.path.dirname(__file__), 'image.png')

  >>> imagefile = open(path)
  >>> image = Image(title=u"My Image", image=imagefile)
  >>> imagefile.close()

The factory is protected by a common ``dolmen.app.security`` right::

  >>> from dolmen.content import require
  >>> print require.bind().get(image)
  dolmen.content.Add


Icon
====

The content registers an icon, thanks to the ``dolmen.app.content``
package::

  >>> from zope.component import getMultiAdapter
  >>> from zope.publisher.browser import TestRequest

  >>> request = TestRequest()
  >>> icon = getMultiAdapter((image, request), name="icon")
  >>> print icon
  <zope.browserresource.icon.IconView object at ...>


View
====

The content registers its own index view. It displays the image and a
download link. To be able to display the content, we need it persisted
in a locatable tree, as the links depend on the urls::

  >>> from zope.component.hooks import getSite
  >>> site = getSite()
  >>> site['image'] = image

We can now summon the view and render it. The view is a
``dolmen.app.layout`` `Page`::

  >>> from dolmen.app.layout import Page
  >>> index = getMultiAdapter((image, request), name="index")
  >>> isinstance(index, Page)
  True

  >>> index.update()
  >>> print index.content()
  <h1>My Image</h1>
  <div class="content">
    <p class="download">
      <a href="http://127.0.0.1/image/++download++image"
         title="Download">Download</a>
      &mdash;
      <span>1 KB</span>
    </p>
    <div class="image">
      <a href="http://127.0.0.1/image/++thumbnail++image.large"
         class="image-link" title="My Image">
        <img src="http://127.0.0.1/image/++thumbnail++image.preview" />
      </a>
    </div>
  </div>
