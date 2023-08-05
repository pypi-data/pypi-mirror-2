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
from zope.annotation.interfaces import IAnnotations

# import local interfaces
from interfaces import ISectionPresentationInfo, SECTION_DISPLAY_FIRST
from ztfy.blog.browser.interfaces.skin import ISectionIndexView
from ztfy.blog.interfaces.section import ISection

# import Zope3 packages
from z3c.form import field
from z3c.template.template import getLayoutTemplate, getViewTemplate
from zope.app import zapi
from zope.app.container.contained import Contained
from zope.component import adapts
from zope.interface import implements, Interface
from zope.proxy import ProxyBase, setProxiedObject
from zope.publisher.browser import BrowserView
from zope.schema.fieldproperty import FieldProperty

# import local packages
from menu import DefaultSkinMenuItem
from ztfy.blog.browser.skin import BaseDialogSimpleEditForm
from ztfy.skin.page import TemplateBasedPage
from ztfy.utils.traversing import getParent

from ztfy.blog import _


SECTION_PRESENTATION_KEY = 'ztfy.blog.defaultskin.section.presentation'


class SectionPresentationViewMenuItem(DefaultSkinMenuItem):
    """Section presentation menu item"""

    title = _(" :: Presentation model...")


class SectionPresentation(Persistent, Contained):
    """Section presentation infos"""

    implements(ISectionPresentationInfo)

    header_format = FieldProperty(ISectionPresentationInfo['header_format'])
    header_position = FieldProperty(ISectionPresentationInfo['header_position'])
    presentation_mode = FieldProperty(ISectionPresentationInfo['presentation_mode'])


class SectionPresentationAdapter(ProxyBase):

    adapts(ISection)
    implements(ISectionPresentationInfo)

    def __init__(self, context):
        annotations = IAnnotations(context)
        presentation = annotations.get(SECTION_PRESENTATION_KEY)
        if presentation is None:
            presentation = annotations[SECTION_PRESENTATION_KEY] = SectionPresentation()
        setProxiedObject(self, presentation)


class SectionPresentationEditForm(BaseDialogSimpleEditForm):
    """Section presentation properties edit form"""

    legend = _("Edit section presentation properties")

    fields = field.Fields(ISectionPresentationInfo)
    layout = getLayoutTemplate()
    parent_interface = ISection


class SectionIndexView(TemplateBasedPage):
    """Section index page"""

    implements(ISectionIndexView)

    def update(self):
        super(SectionIndexView, self).update()
        self.presentation = ISectionPresentationInfo(self.context)
        self.topics = self.context.getVisibleTopics()

    def render(self):
        if self.topics and (self.presentation.presentation_mode == SECTION_DISPLAY_FIRST):
            topic = self.topics[0]
            self.request.response.redirect(zapi.absoluteURL(topic, self.request))
            return u''
        return super(SectionIndexView, self).render()


class SectionSectionsView(BrowserView):
    """Section sub-sections view"""

    __call__ = getViewTemplate()

    @property
    def sections(self):
        result = []
        context = None
        parents = zapi.getParents(self.context) + [self.context, ]
        sections = [s for s in zapi.getParents(self.context) if ISection.providedBy(s)]
        if sections:
            context = sections[-1]
        elif ISection.providedBy(self.context):
            context = self.context
        if context is not None:
            for section in (s for s in context.sections if s.visible):
                selected = section in parents
                subsections = ()
                if selected and ISection.providedBy(section):
                    subsections = [s for s in section.sections if s.visible]
                result.append({ 'section': section,
                                'selected': selected,
                                'subsections': subsections,
                                'subselected': set(subsections) & set(parents) })
        return result

