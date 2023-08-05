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
from datetime import datetime

# import Zope3 interfaces

# import local interfaces
from ztfy.blog.defaultskin.interfaces import ISiteManagerPresentationInfo
from ztfy.blog.interfaces.site import ISiteManager

# import Zope3 packages

# import local packages
from ztfy.skin.viewlet import ViewletBase
from ztfy.utils.traversing import getParent


class FooterViewlet(ViewletBase):
    """Footer viewlet"""

    @property
    def presentation(self):
        site = getParent(self.context, ISiteManager)
        return ISiteManagerPresentationInfo(site)

    @property
    def year(self):
        return datetime.now().year
