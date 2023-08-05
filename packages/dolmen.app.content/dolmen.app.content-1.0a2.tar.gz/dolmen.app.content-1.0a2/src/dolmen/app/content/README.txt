==================
dolmen.app.content
==================

`dolmen.app.content` provides out-of-the-box utilities for Dolmen
applications content.

Getting started
===============

We import Grok and grok the package::

  >>> import grok
  >>> from grokcore.component import testing
  >>> from zope.component.hooks import getSite

We create a `dolmen.content` content::

  >>> import dolmen.content
  >>> class Mammoth(dolmen.content.Content):
  ...    grok.name('A furry thing')

  >>> testing.grok_component("mammoth", Mammoth)
  True

  >>> manfred = Mammoth()
  >>> manfred.title = u'A nice mammoth'

  >>> site = getSite()
  >>> site['manfred'] = manfred

Indexes
=======

`dolmen.app.content` registers two indexes to catalog the
`dolmen.content.IBaseContent` created inside a Dolmen application::

  >>> from dolmen.app.content import indexes


Base indexes
------------

The `dolmen.app.content.indexes.BaseIndexes` handles the title and the content type of an IBaseContent content::

  >>> indexes.BaseIndexes.__grok_indexes__
  {'content_type': <grok.index.Field object at ...>, 'title': <grok.index.Text object at ...>}

  >>> indexes.BaseIndexes.__grok_indexes__['content_type']._attribute
  '__content_type__'


Searchable text
---------------

`dolmen.app.content` provides a simple 'ISearchableText'
implementation, allowing full text searches. It comes in two parts.

The index::

  >>> indexes.SearchableIndex.__grok_indexes__
  {'searchabletext': <grok.index.Text object at ...>}

The adapter::

  >>> from zope.index.text.interfaces import ISearchableText
  >>> adapter = ISearchableText(manfred)
  >>> adapter.getSearchableText()
  u'A nice mammoth'


Thumbnailing
============

Thanks to `dolmen.thumbnailer`, `dolmen.app.content` provides a base
thumbnailing policy, using ZODB blobs as storage and introducing a new
scale.

Scales
------

Let's introspect our Miniaturizer component::

  >>> from dolmen.app.content import thumbnails

  >>> thumbnails.BlobMiniaturizer.factory
  <class 'dolmen.blob.file.BlobValue'>

  >>> print thumbnails.BlobMiniaturizer.scales
  {'mini': (250, 250), 'square': (64, 64), 'thumb': (150, 150), 'large': (700, 700), 'small': (128, 128), 'preview': (400, 400)}

The new scale, 'square', scales down and crops the original image to
provide a square thumbnail. This is done using a IThumbnailer adapter::

  >>> from dolmen.thumbnailer import IThumbnailer	
  >>> thumbnails.SquareThumbnailer
  <class 'dolmen.app.content.thumbnails.SquareThumbnailer'>
  >>> IThumbnailer.implementedBy(thumbnails.SquareThumbnailer)
  True


Icon registration
=================

``dolmen.app.content`` allows you to register an icon for your content type.

The default value
-----------------

  >>> from dolmen.app.content import icon
  >>> icon.bind().get(manfred)
  '...content.png'


Retrieving the icon
-------------------

  >>> from zope.publisher.browser import TestRequest
  >>> from zope.component import getMultiAdapter

  >>> request = TestRequest()
  >>> icon_view = getMultiAdapter((manfred, request), name="icon")
  >>> icon_view()
  '<img src="http://127.0.0.1/dolmen-content-interfaces-IContent-icon.png" alt="Content" width="16" height="16" border="0" />'


Defining a content icon
-----------------------

Let's demonstrate the icon registration with a simple test::

  >>> from zope import schema

  >>> class IContentSchema(dolmen.content.IBaseContent):
  ...    text = schema.Text(title=u"A body text", default=u"N/A")

  >>> class MyContent(dolmen.content.Content):
  ...  """A simple content with an icon
  ...  """
  ...  dolmen.content.schema(IContentSchema)
  ...  dolmen.content.name("a simple content type")
  ...  icon('container.png')

  >>> testing.grok_component("mycontent", MyContent)
  True

Now, we check if our content has a given icon::

  >>> elephant = site['elephant'] = MyContent()
  >>> icon_view = getMultiAdapter((elephant, request), name="icon")
  >>> icon_view()
  '<img src="http://127.0.0.1/dolmen-app-content-IContentSchema-icon.png" alt="ContentSchema" width="16" height="16" border="0" />'

Trying to register an icon file that doesn't exist or cannot resolve
will lead to an error::

  >>> class AnotherContent(dolmen.content.Content):
  ...  """Another content with an icon
  ...  """
  ...  dolmen.content.schema(IContentSchema)
  ...  dolmen.content.name("a simple content type")
  ...  icon('someimaginary thing.png')
  Traceback (most recent call last):
  ...
  GrokImportError: Directive 'icon' cannot resolve the file 'someimaginary thing.png'.


Credits
=======

All Dolmen packages are sponsorised by NPAI (http://www.npai.fr)
