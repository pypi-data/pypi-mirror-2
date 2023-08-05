# -*- coding: utf-8 -*-

import martian
from grokcore.view import interfaces
from zope.interface import Interface


class ILayoutFactory(Interface):
    """ A factory that lookup the layout and return it
    """


class ILayout(Interface):
    """Layout view.
    """


class IPage(interfaces.IGrokView):
    """A view using a layout to render itself.
    """

    def content():
        """Give you back the result of your Page to be included inside
        the layout.
        """


class layout(martian.Directive):
    scope = martian.CLASS_OR_MODULE
    store = martian.ONCE
    default = ILayout
