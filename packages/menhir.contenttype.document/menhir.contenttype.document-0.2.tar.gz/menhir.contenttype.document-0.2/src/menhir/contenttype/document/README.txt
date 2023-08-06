===========================
menhir.contenttype.document
===========================

``menhir.contenttype.document`` provides a text-centered content for
`Dolmen` based `Grok` applications. This document type has a field
allowing a WYSIWYG edition and indexes itself for full-text searches.


Schema
======

A `Document` has a dedicated schema defining a text field, in addition
of the base `IDescriptiveSchema`::

    >>> from dolmen.app.content import IDescriptiveSchema
    >>> from menhir.contenttype.document import IDocument

    >>> IDocument.isOrExtends(IDescriptiveSchema)
    True

    >>> from dolmen.content import schema
    >>> from menhir.contenttype.document import Document

    >>> IDocument in schema.bind().get(Document)
    True

The text field is called "body", as it is the document's body text::

    >>> for attr, doc in IDocument.namesAndDescriptions():
    ...   print attr, ':', doc
    body : <zope.schema...Text object at ...>


Factory
=======

In order to create a `Document` content, the current user will have to
be granted the `dolmen.content.Add` permission, from the
``dolmen.app.security`` package::

    >>> from dolmen.content import require
    >>> require.bind().get(Document)
    'dolmen.content.Add'


Forms
=====

The WYSIWYG widget is provided by ``dolmen.widget.tinymce``, using the
javascript library TinyMCE and jQuery. The Add form and the Edit form
will display the widget, since ``menhir.contenttype.document``
provides a `FieldsCustomizer` adapter (see ``dolmen.forms.crud``
documentation)::

    >>> from dolmen.forms.crud import Edit
    >>> mydoc = Document(title=u'Some title', body=u"Some body")

    >>> from zope.publisher.browser import TestRequest
    >>> request = TestRequest()

    >>> editform = Edit(mydoc, request)
    >>> editform.update()

    >>> editform.fields['body'].mode
    <Marker TINYMCE.INPUT>


Indexation
==========

A `Document` is indexed in full-text, using an `ISearchableText`
adapter::

    >>> from zope.index.text.interfaces import ISearchableText
    >>> indexer = ISearchableText(mydoc)
    >>> indexer.getSearchableText()
    (u'Some title', u'', u'Some body\n\n')

    >>> mydoc.body = u'<p>Rich content comes in <strong>HTML</strong></p>'
    >>> indexer.getSearchableText()
    (u'Some title', u'', u'Rich content comes in **HTML**\n\n')

    >>> mydoc.description = u"I'm described"
    >>> indexer.getSearchableText()
    (u'Some title', u"I'm described", u'Rich content comes in **HTML**\n\n')


View
====

A `Document` has its very own index view, allowing it to render in a
simple way, without the default field names (see
``dolmen.forms.crud``)::

    >>> from zope.component import getMultiAdapter
    >>> view = getMultiAdapter((mydoc, request), name='index')

    >>> from dolmen.app.layout import Page
    >>> isinstance(view, Page)
    True

    >>> print view.content()
    <div class="document">
      <h1>Some title</h1>
      <p>Rich content comes in <strong>HTML</strong></p>
    </div>
