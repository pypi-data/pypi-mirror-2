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
"""Grok
"""
from zope.interface import implements
from zope.component import adapts

from martian import ClassGrokker, InstanceGrokker, GlobalGrokker
from martian import baseclass
from martian.error import GrokError, GrokImportError

from grokcore.component import Context
from grokcore.component import GlobalUtility
from grokcore.component import Adapter, MultiAdapter, GlobalUtility, Context
from grokcore.component import Subscription, MultiSubscription
from grokcore.component.decorators import subscribe, adapter, implementer
from grokcore.component.directive import context, name, title, description
from grokcore.component.directive import provides, direct
from grokcore.component.directive import global_utility, global_adapter

from grokcore.content import Model, Container, OrderedContainer

from grokcore.security import Permission
from grokcore.security import Public
from grokcore.security import require

from grokcore.view import PageTemplate
from grokcore.view import PageTemplateFile
from grokcore.view import DirectoryResource
from grokcore.view import layer
from grokcore.view import template
from grokcore.view import templatedir
from grokcore.view import skin
from grokcore.view import url
from grokcore.view import path

from grokcore.viewlet import Viewlet
from grokcore.viewlet import ViewletManager
from grokcore.viewlet import view
from grokcore.viewlet import viewletmanager
from grokcore.viewlet import order

from grokcore.formlib import action
from grokcore.formlib import AutoFields
from grokcore.formlib import Fields

from grokcore.annotation import Annotation

from grokcore.site.interfaces import IApplication
from grokcore.site import LocalUtility
from grokcore.site import Site
from grokcore.site import getApplication
from grokcore.site import local_utility

from zope.event import notify
from zope.site.hooks import getSite
from zope.lifecycleevent import (
    IObjectCreatedEvent, ObjectCreatedEvent,
    IObjectModifiedEvent, ObjectModifiedEvent,
    IObjectCopiedEvent, ObjectCopiedEvent)
from zope.app.publication.interfaces import IBeforeTraverseEvent

from zope.publisher.interfaces.browser import IBrowserRequest
from zope.publisher.interfaces.browser import IDefaultBrowserLayer

from zope.container.interfaces import (
    IObjectAddedEvent,
    IObjectMovedEvent,
    IObjectRemovedEvent,
    IContainerModifiedEvent)
from zope.container.contained import (
    ObjectAddedEvent,
    ObjectMovedEvent,
    ObjectRemovedEvent,
    ContainerModifiedEvent)

from grok.events import ApplicationInitializedEvent

from grok.components import Application
from grok.components import View, Form, AddForm, EditForm, DisplayForm
from grok.components import ExceptionView, NotFoundView, UnauthorizedView
from grok.components import XMLRPC, REST, JSON
from grok.components import Indexes
from grok.components import Role

from grokcore.traverser import Traverser

from grok.interfaces import IRESTSkinType, IRESTLayer
from grok.interfaces import IApplicationInitializedEvent

from grokcore.traverser import traversable
from grok.directive import (
    permissions, site, restskin)

# BBB These two functions are meant for test fixtures and should be
# imported from grok.testing, not from grok.
from grok.testing import grok, grok_component

# Our __init__ provides the grok API directly so using 'import grok' is enough.
from grok.interfaces import IGrokAPI
from zope.interface import moduleProvides
moduleProvides(IGrokAPI)
__all__ = list(IGrokAPI)
