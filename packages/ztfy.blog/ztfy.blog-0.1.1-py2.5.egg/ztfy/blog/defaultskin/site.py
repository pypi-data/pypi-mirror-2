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

# import local interfaces
from interfaces import ISiteManagerPresentationInfo, ITopicPresentationInfo
from ztfy.blog.browser.interfaces.skin import ISiteManagerIndexView
from ztfy.blog.interfaces.site import ISiteManager

# import Zope3 packages
from z3c.template.template import getLayoutTemplate
from zope.app import zapi
from zope.app.container.contained import Contained
from zope.component import adapts
from zope.event import notify
from zope.interface import implements
from zope.lifecycleevent import ObjectModifiedEvent
from zope.proxy import ProxyBase, setProxiedObject
from zope.schema.fieldproperty import FieldProperty

# import local packages
from menu import DefaultSkinMenuItem
from ztfy.blog.browser.skin import BaseDialogSimpleEditForm
from ztfy.i18n.property import I18nTextProperty
from ztfy.skin.page import TemplateBasedPage
from ztfy.utils.traversing import getParent
from ztfy.workflow.interfaces import IWorkflowContent

from ztfy.blog import _


SITE_MANAGER_PRESENTATION_KEY = 'ztfy.blog.defaultskin.presentation'


class SiteManagerPresentationViewMenuItem(DefaultSkinMenuItem):
    """Site manager presentation menu item"""

    title = _(" :: Presentation model...")


class SiteManagerPresentation(Persistent, Contained):
    """Site manager presentation infos"""

    implements(ISiteManagerPresentationInfo)

    header_format = FieldProperty(ISiteManagerPresentationInfo['header_format'])
    header_position = FieldProperty(ISiteManagerPresentationInfo['header_position'])
    main_blogs = FieldProperty(ISiteManagerPresentationInfo['main_blogs'])
    nb_entries = FieldProperty(ISiteManagerPresentationInfo['nb_entries'])
    owner = FieldProperty(ISiteManagerPresentationInfo['owner'])
    owner_mailto = FieldProperty(ISiteManagerPresentationInfo['owner_mailto'])
    signature = I18nTextProperty(ISiteManagerPresentationInfo['signature'])
    disqus_site_id = FieldProperty(ISiteManagerPresentationInfo['disqus_site_id'])


class SiteManagerPresentationAdapter(ProxyBase):

    adapts(ISiteManager)
    implements(ISiteManagerPresentationInfo)

    def __init__(self, context):
        annotations = IAnnotations(context)
        presentation = annotations.get(SITE_MANAGER_PRESENTATION_KEY)
        if presentation is None:
            presentation = annotations[SITE_MANAGER_PRESENTATION_KEY] = SiteManagerPresentation()
        setProxiedObject(self, presentation)


class SiteManagerPresentationEditForm(BaseDialogSimpleEditForm):
    """Site manager presentation properties edit form"""

    legend = _("Edit site presentation properties")

    fields = field.Fields(ISiteManagerPresentationInfo)
    layout = getLayoutTemplate()
    parent_interface = ISiteManager


class SiteManagerIndexView(TemplateBasedPage):
    """Site manager index page"""

    implements(ISiteManagerIndexView)

    def update(self):
        super(SiteManagerIndexView, self).update()
        self.presentation = ISiteManagerPresentationInfo(self.context)

    @property
    def topics(self):
        blogs = self.presentation.main_blogs
        if not blogs:
            return []
        topics = []
        [topics.extend(blog.getVisibleTopics()) for blog in blogs if blog.visible]
        topics.sort(key=lambda x: IWorkflowContent(x).publication_effective_date, reverse=True)
        return topics[:self.presentation.nb_entries]
