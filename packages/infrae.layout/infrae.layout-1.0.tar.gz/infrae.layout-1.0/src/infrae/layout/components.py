# -*- coding: utf-8 -*-

from five import grok

from zope import component
from zope.interface import Interface
from zope.publisher.publish import mapply
from infrae.layout.interfaces import IPage, ILayout, ILayoutFactory, layout
from infrae.wsgi.log import ErrorSupplement


class LayoutFactory(grok.MultiAdapter):
    grok.adapts(Interface, Interface)
    grok.implements(ILayoutFactory)
    grok.provides(ILayoutFactory)

    def __init__(self, request, context):
        self.request = request
        self.context = context

    def __call__(self, view):
        wanted_layout = layout.bind().get(view)
        return component.getMultiAdapter(
            (self.request, self.context), wanted_layout)


class Layout(object):
    """A layout object.
    """
    grok.baseclass()
    grok.implements(ILayout)

    def __init__(self, request, context):
        self.context = context
        self.request = request
        self.view = None

        if getattr(self, 'module_info', None) is not None:
            self.static = component.queryAdapter(
                self.request, Interface,
                name=self.module_info.package_dotted_name)
            if self.static is not None:
                self.static.__parent__ = self.context
        else:
            self.static = None

    def default_namespace(self):
        namespace = {}
        namespace['view'] = self.view
        namespace['layout'] = self
        namespace['static'] = self.static
        namespace['context'] = self.context
        namespace['request'] = self.request
        return namespace

    def namespace(self):
        return {}

    def update(self):
        pass

    @property
    def response(self):
        return self.request.response

    def _render_template(self):
        return self.template.render(self)

    def render(self):
        return self._render_template()

    render.base_method = True

    def __call__(self, view):
        self.view = view
        self.update()
        return self.render()


class Page(grok.View):
    """A view class.
    """
    grok.baseclass()
    grok.implements(IPage)
    layout(ILayout)

    def __init__(self, context, request):
        super(Page, self).__init__(context, request)
        self.layout = None

    def __call__(self):
        __traceback_supplement__ = (ErrorSupplement, self)

        layout_factory = component.getMultiAdapter(
            (self.request, self.context,), ILayoutFactory)
        self.layout = layout_factory(self)

        mapply(self.update, (), self.request)

        if self.request.response.getStatus() in (302, 303):
            # A redirect was triggered somewhere in update().  Don't
            # continue rendering the template or doing anything else.
            return

        return self.layout(self)

    def default_namespace(self):
        namespace = super(Page, self).default_namespace()
        namespace['layout'] = self.layout
        return namespace

    def content(self):
        template = getattr(self, 'template', None)
        if template is not None:
            return self._render_template()
        return mapply(self.render, (), self.request)


