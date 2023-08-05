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


# import standard packages

# import Zope3 interfaces
from zope.app.catalog.interfaces import ICatalog
from zope.app.container.interfaces import IObjectAddedEvent, IObjectRemovedEvent
from zope.lifecycleevent.interfaces import IObjectCopiedEvent

# import local interfaces
from interfaces import IFilePropertiesContainer, IFilePropertiesContainerAttributes

# import Zope3 packages
from zope.app import zapi
from zope.app.container.contained import ObjectRemovedEvent
from zope.component import adapter
from zope.event import notify
from zope.location import locate

# import local packages
from ztfy.utils import catalog


@adapter(IFilePropertiesContainer, IObjectCopiedEvent)
def handleCopiedFilePropertiesContainer(object, event):
    """When a file properties container is copied, we have to tag it for indexation
    
    Effective file indexation will be done only after content have been added to it's new parent container"""
    object._v_copied_file = True


@adapter(IFilePropertiesContainer, IObjectAddedEvent)
def handleAddedFilePropertiesContainer(object, event):
    """When a file properties container is added, we must index it's attributes"""
    if not hasattr(object, '_v_copied_file'):
        return
    for _name, catalog_util in zapi.getUtilitiesFor(ICatalog):
        for attr in IFilePropertiesContainerAttributes(object).attributes:
            value = getattr(object, attr, None)
            if value is not None:
                locate(value, object, value.__name__)
                catalog.indexObject(value, catalog_util)
    delattr(object, '_v_copied_file')


@adapter(IFilePropertiesContainer, IObjectRemovedEvent)
def handleRemovedFilePropertiesContainer(object, event):
    """When a file properties container is added, we must index it's attributes"""
    for _name, catalog_util in zapi.getUtilitiesFor(ICatalog):
        for attr in IFilePropertiesContainerAttributes(object).attributes:
            value = getattr(object, attr, None)
            if value is not None:
                notify(ObjectRemovedEvent(value))
                catalog.unindexObject(value, catalog_util)
