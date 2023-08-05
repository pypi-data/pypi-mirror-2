=============
infrae.layout
=============

``infrae.layout`` defines a way to write view that can reuse an
existing defined layout in Zope 2. It is similar to `megrok.layout`_,
and work the same way, with some additions.

API
===

You can define a *Layout* that will be used by a *Page*. A *Page* is
a view and behave the same way. A page will look for Layout and will
render inside it.

Both *Page* and *Layout* can be rendered by either a ``render``
method, or by an associated template, exactly like a Grok view.

A *Layout* is found by adapting the request and the content:
you can register layouts for your skin, then for a specific content.

If this is not sufficient, a page can use the Grok directive
``layout`` to directly specify its type of Layout to use. While
defining your layout, you can use the same directive to declare which
layout a type belongs to. For instance if you have a skin
``ICorpSkin``::


  from infae.layout import layout, Layout, ILayout, Page
  from five import grok

  from corp.skin import ICorpSkin

  grok.skin(ICorpSkin)


  class ViewLayout(Layout):

     def render(self):
         return u'View %s' % self.view.content()

  class Index(Page):

     def render(self):
         return self.context.title()


Now if on the same content you want an edition layout for instance::

   class IEditionLayout(ILayout)
       """Layout to edit content
       """

   class EditionLayout(Layout):
       layout(IEditionLayout)

       def render(self):
           return u'Edit %s' % self.view.content()

   class Edit(Page):
      layout(IEditionLayout)

      def render(self):
           return self.context.title()


If the above mecanism is not flexible enough for your application, you can
write an adapter on the request and your content that provides
``ILayoutFactory``.
The adapter will allow you to code the logic to select any layout you want.


.. _megrok.layout: http://pypi.python.org/pypi/megrok.layout
