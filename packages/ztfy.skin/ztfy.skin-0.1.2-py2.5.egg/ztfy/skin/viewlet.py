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

# import local interfaces

# import Zope3 packages
from z3c.template.template import getViewTemplate
from zope.viewlet.viewlet import ViewletBase as Viewlet
from zope.viewlet.manager import ViewletManagerBase as ViewletManager, WeightOrderedViewletManager

# import local packages

from ztfy.skin import _


class ViewletManagerBase(ViewletManager):

    template = getViewTemplate()


class WeightViewletManagerBase(WeightOrderedViewletManager):

    template = getViewTemplate()


class ViewletBase(Viewlet):

    render = getViewTemplate()
