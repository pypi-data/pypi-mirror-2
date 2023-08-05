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

# import Zope3 interfaces
from z3c.form import button
from z3c.formjs import jsaction

# import local interfaces

# import Zope3 packages
from zope.interface import Interface

# import local packages

from ztfy.blog import _


class IBaseForm(Interface):
    """Marker interface for any form"""


class IEditFormButtons(Interface):
    """Default edit form buttons"""

    submit = button.Button(title=_("Submit"))
    reset = jsaction.JSButton(title=_("Reset"))


class IDialogAddFormButtons(Interface):
    """Default dialog add form buttons"""

    add = jsaction.JSButton(title=_("Add"))
    cancel = jsaction.JSButton(title=_("Cancel"))


class IDialogEditFormButtons(Interface):
    """Default dialog edit form buttons"""

    dialog_submit = jsaction.JSButton(title=_("Submit"))
    dialog_cancel = jsaction.JSButton(title=_("Cancel"))


# Base front-office views

class ISiteManagerIndexView(Interface):
    """Site manager index view marker interface"""


class IBlogIndexView(Interface):
    """Blog index view marker interface"""


class IBlogFolderIndexView(Interface):
    """Blog folder index view marker interface"""


class ISectionIndexView(Interface):
    """Section index view marker interface"""


class ITopicIndexView(Interface):
    """Topic index view marker interface"""


class ICategoryIndexView(Interface):
    """Category index view marker interface"""
