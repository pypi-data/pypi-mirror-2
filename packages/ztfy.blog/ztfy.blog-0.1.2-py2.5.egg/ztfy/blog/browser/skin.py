### -*- coding: utf-8 -*- ####################################################
##############################################################################
#
# Copyright (c) 2008-2009 Thierry Florac <tflorac AT ulthar.net>
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
import copy

# import Zope3 interfaces
from z3c.json.interfaces import IJSONWriter
from z3c.language.switch.interfaces import II18n
from zope.app.container.interfaces import IContainer
from zope.app.publication.interfaces import IBeforeTraverseEvent
from zope.publisher.interfaces.browser import IBrowserRequest, IBrowserSkinType
from zope.schema.interfaces import IText

# import local interfaces
from interfaces.skin import IBaseForm, IDialogAddFormButtons, IDialogEditFormButtons
from ztfy.blog.interfaces import ISkinnable
from ztfy.blog.interfaces.resource import IResourceContainerTarget
from ztfy.blog.layer import IZTFYBlogLayer, IZTFYBlogFrontLayer
from ztfy.file.browser.widget.interfaces import IHTMLWidgetSettings

# import Zope3 packages
from z3c.form import widget, button
from z3c.form.browser.select import SelectWidget
from z3c.formjs import ajax, jsaction
from zope.app import zapi
from zope.component import adapter, adapts
from zope.event import notify
from zope.interface import implements, implementer, Interface
from zope.lifecycleevent import ObjectModifiedEvent
from zope.proxy import ProxyBase, setProxiedObject
from zope.publisher.browser import applySkin
from zope.security.management import checkPermission

# import local packages
from ztfy.skin.form import AddForm, EditForm, DialogAddForm, DialogEditForm
from ztfy.skin.page import TemplateBasedPage
from ztfy.utils.traversing import getParent

from ztfy.blog import _


class BaseTemplateBackView(TemplateBasedPage):

    implements(IBaseForm)

    def update(self):
        skin = zapi.queryUtility(IBrowserSkinType, 'ZMI')
        if (skin is None) or ((skin is not None) and not skin.providedBy(self.request)):
            applySkin(self.request, zapi.getUtility(IBrowserSkinType, 'ZBlog.BO'))
        super(BaseTemplateBackView, self).update()


class BaseAddForm(AddForm):

    implements(IBaseForm)

    def update(self):
        skin = zapi.queryUtility(IBrowserSkinType, 'ZMI')
        if (skin is None) or ((skin is not None) and not skin.providedBy(self.request)):
            applySkin(self.request, zapi.getUtility(IBrowserSkinType, 'ZBlog.BO'))
        super(BaseAddForm, self).update()


class BaseDialogAddForm(ajax.AJAXRequestHandler, BaseAddForm, DialogAddForm):
    """Base dialog add form"""

    buttons = button.Buttons(IDialogAddFormButtons)
    layout = None
    parent_interface = IContainer
    parent_view = None
    handle_upload = False

    @jsaction.handler(buttons['add'])
    def add_handler(self, event, selector):
        return '$.ZBlog.form.add(this.form);'

    @jsaction.handler(buttons['cancel'])
    def cancel_handler(self, event, selector):
        return '$.ZBlog.dialog.close();'

    @ajax.handler
    def ajaxCreate(self):
        # Create resources through AJAX request
        # JSON results have to be included in a textarea to handle JQuery.Form plugin file uploads
        writer = zapi.getUtility(IJSONWriter)
        self.updateWidgets()
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            self.update()
            if self.handle_upload:
                return '<textarea>%s</textarea>' % writer.write({ 'output': self.layout() })
            else:
                return writer.write({ 'output': self.layout() })
        self.createAndAdd(data)
        parent = getParent(self.context, self.parent_interface)
        notify(ObjectModifiedEvent(parent))
        view = self.parent_view(parent, self.request)
        view.update()
        if self.handle_upload:
            return '<textarea>%s</textarea>' % writer.write({ 'output': u"<!-- OK -->\n" + view.output() })
        else:
            return writer.write({ 'output': u"<!-- OK -->\n" + view.output() })


class BaseEditForm(EditForm):

    implements(IBaseForm)

    def update(self):
        skin = zapi.queryUtility(IBrowserSkinType, 'ZMI')
        if (skin is None) or ((skin is not None) and not skin.providedBy(self.request)):
            applySkin(self.request, zapi.getUtility(IBrowserSkinType, 'ZBlog.BO'))
        super(BaseEditForm, self).update()


class BaseDialogSimpleEditForm(ajax.AJAXRequestHandler, BaseEditForm, DialogEditForm):
    """Base dialog simple edit form"""

    buttons = button.Buttons(IDialogEditFormButtons)
    layout = None
    parent_interface = IContainer

    @property
    def title(self):
        result = II18n(self.context).queryAttribute('title', request=self.request)
        if not result:
            result = '{{ %s }}' % zapi.getName(self.context)
        return result

    @jsaction.handler(buttons['dialog_submit'])
    def submit_handler(self, event, selector):
        return '''$.ZBlog.form.edit(this.form);'''

    @jsaction.handler(buttons['dialog_cancel'])
    def cancel_handler(self, event, selector):
        return '$.ZBlog.dialog.close();'

    @ajax.handler
    def ajaxEdit(self):
        writer = zapi.getUtility(IJSONWriter)
        self.updateWidgets()
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            self.update()
            return writer.write({ 'output': self.layout() })
        if self.applyChanges(data):
            parent = getParent(self.context, self.parent_interface)
            notify(ObjectModifiedEvent(parent))
            return writer.write({ 'output': u'OK' })
        else:
            return writer.write({ 'output': u'NONE' })


class BaseDialogEditForm(BaseDialogSimpleEditForm):
    """Base dialog edit form"""

    parent_view = None
    handle_upload = False

    @ajax.handler
    def ajaxEdit(self):
        # Update resource throught AJAX request
        # JSON results have to be included in a textarea to handle JQuery.Form plugin file uploads
        writer = zapi.getUtility(IJSONWriter)
        self.updateWidgets()
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            self.update()
            if self.handle_upload:
                return '<textarea>%s</textarea>' % writer.write({ 'output': self.layout() })
            else:
                return writer.write({ 'output': self.layout() })
        self.applyChanges(data)
        parent = getParent(self.context, self.parent_interface)
        notify(ObjectModifiedEvent(parent))
        view = self.parent_view(parent, self.request)
        view.update()
        if self.handle_upload:
            return '<textarea>%s</textarea>' % writer.write({ 'output': u"<!-- OK -->\n" + view.output() })
        else:
            return writer.write({ 'output': u"<!-- OK -->\n" + view.output() })


class SkinSelectWidget(SelectWidget):
    noValueMessage = _("(inherit parent skin)")

def SkinSelectWidgetFactory(field, request):
    return widget.FieldWidget(field, SkinSelectWidget(request))


@adapter(ISkinnable, IBeforeTraverseEvent)
def handleSkinTraversal(object, event):
    if IBrowserRequest.providedBy(event.request):
        path = event.request.get('PATH_INFO', '')
        if (path.find('++skin++') < 0):
            skin_name = ISkinnable(object).getSkin()
            if not skin_name:
                skin_name = 'ZBlog'
            skin = zapi.queryUtility(IBrowserSkinType, skin_name)
            if skin is not None:
                applySkin(event.request, skin)


@adapter(IText, IBaseForm, IZTFYBlogLayer)
@implementer(IHTMLWidgetSettings)
def  HTMLWidgetAdapterFactory(field, form, request):
    """Create widget adapter matching content's applied skin"""
    settings = None
    target = getParent(form.context, ISkinnable)
    if target is not None:
        skin_name = ISkinnable(target).getSkin()
        if not skin_name:
            skin_name = 'ZBlog'
        skin = zapi.queryUtility(IBrowserSkinType, skin_name)
        if skin is not None:
            fake = copy.copy(request)
            applySkin(fake, skin)
            settings = zapi.queryMultiAdapter((field, form, fake), IHTMLWidgetSettings)
    return settings


class HTMLWidgetAdapter(object):
    """HTML widget settings adapter"""

    adapts(IText, IBaseForm, IZTFYBlogFrontLayer)
    implements(IHTMLWidgetSettings)

    def __init__(self, field, form, request):
        self.field = field
        self.form = form
        self.request = request

    mce_invalid_elements = 'h1,h2'

    @property
    def mce_external_image_list_url(self):
        target = getParent(self.form.context, IResourceContainerTarget)
        if target is not None:
            return '%s/@@getImagesList.js' % zapi.absoluteURL(target, self.request)
        return None

    @property
    def mce_external_link_list_url(self):
        target = getParent(self.form.context, IResourceContainerTarget)
        if target is not None:
            return '%s/@@getLinksList.js' % zapi.absoluteURL(target, self.request)
        return None
