### -*- coding: utf-8 -*- ####################################################
##############################################################################
#
# Copyright (c) 2008-2010 Thierry Florac <tflorac AT ulthar.net>
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

__docformat__ = "restructuredtext"

# import standard packages
from persistent import Persistent

# import Zope3 interfaces
from z3c.form import field, button
from z3c.formjs import ajax, jsaction
from z3c.json.interfaces import IJSONWriter
from z3c.language.switch.interfaces import II18n
from zope.annotation.interfaces import IAnnotations
from zope.dublincore.interfaces import IZopeDublinCore

# import local interfaces
from interfaces import ITopicPresentationInfo
from ztfy.blog.browser.interfaces.paragraph import IParagraphRenderer
from ztfy.blog.browser.interfaces.skin import ITopicIndexView
from ztfy.blog.defaultskin.interfaces import ISiteManagerPresentationInfo, IBlogPresentationInfo
from ztfy.blog.interfaces import IUniqueID
from ztfy.blog.interfaces.blog import IBlog
from ztfy.blog.interfaces.category import ICategorizedContent
from ztfy.blog.interfaces.link import ILinkContainer
from ztfy.blog.interfaces.resource import IResourceContainer
from ztfy.blog.interfaces.topic import ITopic
from ztfy.blog.interfaces.site import ISiteManager

# import Zope3 packages
from z3c.template.template import getLayoutTemplate, getViewTemplate
from zope.app import zapi
from zope.app.container.contained import Contained
from zope.component import adapts
from zope.event import notify
from zope.interface import implements
from zope.lifecycleevent import ObjectModifiedEvent
from zope.proxy import ProxyBase, setProxiedObject
from zope.publisher.browser import BrowserView, NotFound
from zope.schema.fieldproperty import FieldProperty

# import local packages
from menu import DefaultSkinMenuItem
from ztfy.blog.browser.skin import BaseDialogSimpleEditForm
from ztfy.skin.page import TemplateBasedPage
from ztfy.utils.security import getPrincipal
from ztfy.utils.traversing import getParent
from ztfy.workflow.interfaces import IWorkflowContent

from ztfy.blog import _


TOPIC_PRESENTATION_KEY = 'ztfy.blog.defaultskin.topic.presentation'


class TopicPresentationViewMenuItem(DefaultSkinMenuItem):
    """Site manager presentation menu item"""

    title = _(" :: Presentation model...")


class TopicPresentation(Persistent, Contained):
    """Site manager presentation infos"""

    implements(ITopicPresentationInfo)

    header_format = FieldProperty(ITopicPresentationInfo['header_format'])
    header_position = FieldProperty(ITopicPresentationInfo['header_position'])
    illustration_position = FieldProperty(ITopicPresentationInfo['illustration_position'])
    linked_resources = FieldProperty(ITopicPresentationInfo['linked_resources'])


class TopicPresentationAdapter(ProxyBase):

    adapts(ITopic)
    implements(ITopicPresentationInfo)

    def __init__(self, context):
        annotations = IAnnotations(context)
        presentation = annotations.get(TOPIC_PRESENTATION_KEY)
        if presentation is None:
            presentation = annotations[TOPIC_PRESENTATION_KEY] = TopicPresentation()
        setProxiedObject(self, presentation)


class TopicPresentationEditForm(BaseDialogSimpleEditForm):
    """Topic presentation properties edit form"""

    legend = _("Edit topic presentation properties")

    fields = field.Fields(ITopicPresentationInfo).omit('header_position')
    layout = getLayoutTemplate()
    parent_interface = ITopic


class TopicIndexList(BrowserView):
    """Topic list item"""

    __call__ = getViewTemplate()

    @property
    def presentation(self):
        return ITopicPresentationInfo(self.context)


class TopicIndexPreview(TopicIndexList):
    """Topic index preview"""

    __call__ = getViewTemplate()

    @property
    def author(self):
        return getPrincipal(IZopeDublinCore(self.context).creators[0])

    @property
    def date(self):
        return IWorkflowContent(self.context).publication_effective_date


class TopicIndexView(TemplateBasedPage):
    """Topic index page"""

    implements(ITopicIndexView)

    def update(self):
        if not IWorkflowContent(self.context).isVisible():
            raise NotFound(self.context, self.__name__, self.request)
        super(TopicIndexView, self).update()
        self.presentation = ITopicPresentationInfo(self.context)
        self.renderers = [renderer for renderer in [zapi.queryMultiAdapter((paragraph, self, self.request), IParagraphRenderer) for paragraph in self.context.getVisibleParagraphs(self.request)]
                                                if renderer is not None]
        [renderer.update() for renderer in self.renderers]

    @property
    def author(self):
        return getPrincipal(IZopeDublinCore(self.context).creators[0])

    @property
    def date(self):
        return IWorkflowContent(self.context).publication_effective_date


class TopicResourcesView(BrowserView):
    """Topic resources view"""

    __call__ = getViewTemplate()

    @property
    def resources(self):
        return ITopicPresentationInfo(self.context).linked_resources


class TopicLinksView(BrowserView):
    """Topic links view"""

    __call__ = getViewTemplate()

    @property
    def links(self):
        return ILinkContainer(self.context).getVisibleLinks()


class TopicTagsView(BrowserView):
    """Topic tags view"""

    __call__ = getViewTemplate()

    @property
    def tags(self):
        return ICategorizedContent(self.context).categories


class TopicCommentsView(BrowserView):
    """Topic comments view"""

    __call__ = getViewTemplate()

    @property
    def oid(self):
        return IUniqueID(self.context).oid

    @property
    def presentation(self):
        if not self.context.commentable:
            return None
        site = getParent(self.context, ISiteManager)
        if site is not None:
            return ISiteManagerPresentationInfo(site)
        blog = getParent(self.context, IBlog)
        if blog is not None:
            return IBlogPresentationInfo(blog)
        return None
