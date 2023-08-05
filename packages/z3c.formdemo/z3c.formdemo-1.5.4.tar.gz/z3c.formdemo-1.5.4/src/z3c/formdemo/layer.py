##############################################################################
#
# Copyright (c) 2007 Zope Foundation and Contributors.
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
"""
$Id: layer.py 77305 2007-07-02 13:19:02Z srichter $
"""
__docformat__ = "reStructuredText"

from z3c.form.interfaces import IFormLayer
from z3c.layer.pagelet import IPageletBrowserLayer


class IDemoBrowserLayer(IFormLayer, IPageletBrowserLayer):
    """Demo browser layer using div-form layout template."""
