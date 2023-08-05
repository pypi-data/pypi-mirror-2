### -*- coding: utf-8 -*- ####################################################
##############################################################################
#
# Copyright (c) 2008 Thierry Florac <tflorac AT ulthar.net>
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


# import standard packages

# import Zope3 interfaces
from z3c.form.interfaces import IWidget

# import local interfaces
from ztfy.file.interfaces import IFileField, ICthumbImageField, IThumbnailGeometry

# import Zope3 packages
from z3c.form.converter import FileUploadDataConverter
from zope.component import adapts

# import local packages


class FileFieldDataConverter(FileUploadDataConverter):
    """Data converter for FileField fields"""

    adapts(IFileField, IWidget)

    def toFieldValue(self, value):
        result = super(FileFieldDataConverter,self).toFieldValue(value)
        if not result:
            widget = self.widget
            if widget.deleted:
                return None
            if (widget.field.interface is not None) and widget.field.interface.providedBy(widget.context):
                return widget.field.get(widget.context)
        return result


class CthumbImageFieldDataConverter(FileFieldDataConverter):
    """Data converter for CthumbImageField fields"""

    adapts(ICthumbImageField, IWidget)

    def toFieldValue(self, value):
        result = super(CthumbImageFieldDataConverter,self).toFieldValue(value)
        geometry = IThumbnailGeometry(result, None)
        if geometry is not None:
            position = self.widget.position
            if position != geometry.position:
                geometry.position = position
            size = self.widget.size
            if size != geometry.size:
                geometry.size = size
        return result
