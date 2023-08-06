##############################################################################
#
# Copyright (c) 2006-2007 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""Base classes for Grok application components.

When an application developer builds a Grok-based application, the
classes they define each typically inherit from one of the base classes
provided here.

"""
import simplejson

import zope.location
from zope import component
from zope import interface
from zope.securitypolicy.role import Role as securitypolicy_Role
from zope.publisher.browser import BrowserPage
from zope.publisher.interfaces import NotFound
from zope.publisher.interfaces.browser import IBrowserPublisher
from zope.publisher.interfaces.http import IHTTPRequest
from zope.publisher.publish import mapply
from zope.publisher.defaultview import getDefaultViewName
from zope.container.interfaces import IReadContainer

import grok
import martian.util

import grokcore.view
import grokcore.site
import grokcore.message
from grok import interfaces, util

# BBB this is for import backward compatibility.
from grokcore.content import Model, Container, OrderedContainer


class Application(grokcore.site.Site):
    """Mixin for creating Grok application objects.

    When a `grok.Container` (or a `grok.Model`, though most developers
    use containers) also inherits from `grok.Application`, it not only
    gains the component registration abilities of a `grok.Site`, but
    will also be listed in the Grok admin control panel as one of the
    applications that the admin can install directly at the root of
    their Zope database.

    """
    interface.implements(interfaces.IApplication)


class View(grokcore.view.View):
    """The base class for views with templates in Grok applications.

    Each class that inherits from `grok.View` is designed to "render" a
    category of content objects by reducing them to a document (often an
    HTML document).  Every view has a name, and is invoked when users
    visit the URL of an eligible context object followed by the name of
    the view itself::

        http://example.com/app/folder/object/viewname

    If the view name might conflict with actual content inside of the
    context (in the above URL, the context might already contain an
    attribute or item named ``viewname``), then the URL can be explicit
    that it is asking for a view by preceding its name with ``@@``::

        http://example.com/app/folder/object/@@viewname

    Instead of returning a full document, views are sometimes used to
    provide only a snippet of information for inclusion in some larger
    document; the view can then be called from inside of another view's
    page template::

        <li tal:content="context/@@viewname">snippet goes here</li>

    A view class can specify the category of objects that it can render
    by calling the `grok.context()` directive with either a class or an
    interface.  Otherwise, Grok will attempt to determine the context
    automatically by searching the view's module for exactly one
    `grok.Model` or `grok.Container` class (or some other class
    providing the interface `IContext`) and using that class, if found.

    Grok normally creates a view's name (the name used in URLs) by
    downcasing the name of the view class itself.  The developer can
    override this by supplying the `grok.name()` directive instead.

    The view name ``index`` is special (this works whether the view
    class itself is named ``Index``, or whether ``grok.name('index')``
    is used instead).  A view named ``index`` is used to render an
    object when the user visits its URL without appending a view name.

    Each view needs to generate and return a document. There are two
    ways of doing so: either the view can provide a `render()` method
    that returns a document, or the view can be associated with a page
    template that Grok will.  Page templates can be associated with a
    view in three different ways:

    * Grok will automatically associate a view with a page template
      defined in an accompanying ``templates`` directory.  If a view
      class ``MammothList`` occurs in a module ``<src>/animal.py``, for
      example, then Grok will look for a page template with the name
      ``<src>/animal_templates/mammothlist.pt``, where ``.pt`` can be
      any page-template extension recognized by Grok.

    * Grok will automatically associate a view with a page template
      object in the same module whose name is the downcased name of the
      view class itself.  For example, a view ``MammothList`` might be
      defined in a module alongside an actual template instance named
      ``mammothlist``.

    * The developer can explicitly define the path to the page template
      file by providing the ``grok.template()`` directive.

    Before a page template is rendered, Grok will call the `update()`
    method on the view, if one is supplied, which can pre-compute values
    that the template will need to display.  Both `render()` methods and
    `update()` methods will find the context for which the view is being
    rendered under ``self.context``.

    """
    interface.implements(interfaces.IGrokView)

    def application_url(self, name=None, data=None):
        """Return the URL of the nearest enclosing `grok.Application`."""
        return util.application_url(self.request, self.context, name, data)

    def flash(self, message, type='message'):
        """Send a short message to the user."""
        grokcore.message.send(message, type=type, name='session')


class Form(grokcore.formlib.Form, View):
    """The base class for forms in Grok applications.

    A class that inherits from `grok.Form` is a `grok.View` whose
    template will be given information about the fields in its context,
    and use that information to render an HTML form for adding or
    editing the form.  Generally developers use one of the subclasses:

    * `grok.AddForm`
    * `grok.DisplayForm`
    * `grok.EditForm`

    """
    interface.implements(interfaces.IGrokForm)


class AddForm(grokcore.formlib.AddForm, View):
    """Base class for add forms in Grok applications."""
    interface.implements(interfaces.IGrokForm)


class DisplayForm(grokcore.formlib.DisplayForm, View):
    """Base class for display forms in Grok applications."""
    interface.implements(interfaces.IGrokForm)


class EditForm(grokcore.formlib.EditForm, View):
    """Base class for edit forms in Grok applications."""
    interface.implements(interfaces.IGrokForm)


class ViewishViewSupport(grokcore.view.ViewSupport):

    def application_url(self, name=None, data=None):
        return util.application_url(self.request, self.context, name, data)


class XMLRPC(ViewishViewSupport):
    """Base class for XML-RPC endpoints in Grok applications.

    When an application creates a subclass of `grok.XMLRPC`, it is
    creating an XML-RPC view.  Like other Grok views, each `grok.XMLRPC`
    component can either use an explicit `grok.context()` directive to
    specify the kind of object it wraps, or else Grok will look through
    the same module for exactly one `grok.Model` or `grok.Container` (or
    other `IGrokContext` implementor) and make that class its context
    instead.

    Every object that is an instance of the wrapped class or interface
    becomes a legitimate XML-RPC server URL, offering as available
    procedures whatever methods have been defined inside of that
    `grok.XMLRPC` component.  When a method is called over XML-RPC, any
    parameters are translated into normal Python data types and supplied
    as normal positional arguments.  When the method returns a value or
    raises an exception, the result is converted back into an XML-RPC
    response for the client.  In both directions, values are marshalled
    transparently to and from XML-RPC data structures.

    During the execution of an XML-RPC method, the object whose URL was
    used for the XML-RPC call is available as ``self.context``.

    """


class REST(zope.location.Location, ViewishViewSupport):
    """Base class for REST views in Grok applications."""
    interface.implements(interfaces.IREST)

    def __init__(self, context, request):
        self.context = self.__parent__ = context
        self.request = request


class JSON(BrowserPage, ViewishViewSupport):
    """Base class for JSON views in Grok applications."""
    interface.implements(interfaces.IGrokSecurityView)

    def __call__(self):
        view_name = self.__view_name__
        method = getattr(self, view_name)
        method_result = mapply(method, (), self.request)
        self.request.response.setHeader('Content-Type', 'application/json')
        return simplejson.dumps(method_result)


class Traverser(object):
    """Base class for traversers in Grok applications."""
    interface.implements(IBrowserPublisher)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def browserDefault(self, request):
        # if we have a RESTful request, we will handle
        # GET, POST and HEAD differently (PUT and DELETE are handled already
        # but not on the BrowserRequest layer but the HTTPRequest layer)
        if interfaces.IRESTLayer.providedBy(request):
            rest_view = component.getMultiAdapter(
                (self.context, self.request), name=request.method)
            return rest_view, ()
        view_name = getDefaultViewName(self.context, request)
        view_uri = "@@%s" % view_name
        return self.context, (view_uri,)

    def publishTraverse(self, request, name):
        subob = self.traverse(name)
        if subob is not None:
            return util.safely_locate_maybe(subob, self.context, name)

        traversable_dict = grok.traversable.bind().get(self.context)
        if traversable_dict:
            if name in traversable_dict:
                subob = getattr(self.context, traversable_dict[name])
                if callable(subob):
                    subob = subob()
                return util.safely_locate_maybe(subob, self.context, name)

        # XXX Special logic here to deal with containers.  It would be
        # good if we wouldn't have to do this here. One solution is to
        # rip this out and make you subclass ContainerTraverser if you
        # wanted to override the traversal behaviour of containers.
        if IReadContainer.providedBy(self.context):
            item = self.context.get(name)
            if item is not None:
                return item

        view = component.queryMultiAdapter((self.context, request), name=name)
        if view is not None:
            return view

        raise NotFound(self.context, name, request)

    def traverse(self, name):
        # this will be overridden by subclasses
        pass


class ContextTraverser(Traverser):
    """Base class for context traversers in Grok applications.

    A context traverser is like a normal `grok.Traverser` but, instead
    of supplying its own `traverse()` method, it directs Grok to go call
    the ``traverse()`` method on the context itself in order to process
    the next name in the URL.

    """
    component.adapts(interfaces.IContext, IHTTPRequest)

    def traverse(self, name):
        traverse = getattr(self.context, 'traverse', None)
        if traverse:
            return traverse(name)


class ContainerTraverser(Traverser):
    """Base class for container traversers in Grok applications.

    A container traverser is like a normal `grok.Traverser` but, instead
    of supplying its own ``traverse()`` method, Grok will either call
    the ``traverse()`` method on the context itself, if any, else call
    ``get()`` on the container (a getitem-style lookup) in order to
    resolve the next name in the URL.

    """
    component.adapts(interfaces.IContainer, IHTTPRequest)

    def traverse(self, name):
        traverse = getattr(self.context, 'traverse', None)
        if traverse:
            result = traverse(name)
            if result is not None:
                return result
        # try to get the item from the container
        return self.context.get(name)


class IndexesClass(object):
    """Base class for index collections in a Grok application.

    A `grok.Indexes` utility provides one or more Zope Database content
    indexes for use in a `grok.Site` or `grok.Application`.  The site or
    application that the indexes are intended for should be named with
    the `grok.site()` directive, and the kind of object to index should
    be named with a `grok.context()` directive.

    Inside their class, the developer should specify one or more
    `grok.index.Field` instances naming object attributes that should be
    indexed (and therefore searchable)::

        class ArticleIndex(grok.Indexes):
            grok.site(Newspaper)
            grok.context(Article)
            author = index.Field()
            title = index.Field()
            body = index.Text()

    See the `grok.index` module for more information on field types.

    Note that indexes are persistent: they are stored in the Zope
    database alongside the site or application that they index.  They
    are created when the site or application is first created, and so an
    already-created site will not change just because the definition of
    one of its `grok.Indexes` changes; it will either have to be deleted
    and re-created, or some other operation performed to bring its
    indexes up to date.

    """
    def __init__(self, name, bases=(), attrs=None):
        if attrs is None:
            return
        indexes = {}
        for name, value in attrs.items():
            # Ignore everything that's not an index definition object
            # except for values set by directives
            if '.' in name:
                setattr(self, name, value)
                continue
            if not interfaces.IIndexDefinition.providedBy(value):
                continue
            indexes[name] = value
        self.__grok_indexes__ = indexes
        # __grok_module__ is needed to make defined_locally() return True for
        # inline templates
        self.__grok_module__ = martian.util.caller_module()

Indexes = IndexesClass('Indexes')


class Role(securitypolicy_Role):
    """Base class for roles in Grok applications.

    A role is a description of a class of users that gives them a
    machine-readable name, a human-readable title, and a set of
    permissions which users belong to that role should possess::

        class Editor(grok.Role):
            grok.name('news.Editor')
            grok.title('Editor')
            grok.permissions('news.EditArticle', 'news.PublishArticle')

    """
