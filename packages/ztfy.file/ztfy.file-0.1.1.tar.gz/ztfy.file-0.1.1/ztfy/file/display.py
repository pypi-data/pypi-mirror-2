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
from persistent import Persistent
from persistent.dict import PersistentDict

# import Zope3 interfaces
from zope.annotation.interfaces import IAnnotations
from zope.app.file.interfaces import IImage
from zope.lifecycleevent.interfaces import IObjectModifiedEvent

# import local interfaces
from interfaces import DefaultDisplays
from interfaces import IImageDisplay, IThumbnailGeometry, IThumbnailer, IImageModifiedEvent

# import Zope3 packages
from zope.app import zapi
from zope.app.container.contained import ObjectRemovedEvent
from zope.app.file import Image
from zope.component import adapter, adapts
from zope.event import notify
from zope.interface import implements
from zope.lifecycleevent import ObjectCreatedEvent
from zope.location import locate

# import local packages


IMAGE_DISPLAY_ANNOTATIONS_KEY = 'ztfy.file.display'

class ImageDisplayAdapter(object):
    """IImageDisplay adapter"""

    adapts(IImage)
    implements(IImageDisplay)

    def __init__(self, context):
        image = self.image = context
        annotations = IAnnotations(image)
        displays = annotations.get(IMAGE_DISPLAY_ANNOTATIONS_KEY)
        if displays is None:
            displays = annotations[IMAGE_DISPLAY_ANNOTATIONS_KEY] = PersistentDict()
        self.displays = displays

    def getDisplaySize(self, display, forced=False):
        if display == 'cthumb':
            return (DefaultDisplays[display], DefaultDisplays[display])
        width, height = self.image.getImageSize()
        if display in DefaultDisplays:
            h = w = DefaultDisplays[display]
            w_ratio = 1.0 * width / w
            h_ratio = 1.0 * height / h
        elif display.lower().startswith('w'):
            w = int(display[1:])
            w_ratio = 1.0 * width / w
            h_ratio = 0.0
        elif display.lower().startswith('h'):
            h = int(display[1:])
            h_ratio = 1.0 * height / h
            w_ratio = 0.0
        else:
            w, h = tuple([int(x) for x in display.split('x')])
            w_ratio = 1.0 * width / w
            h_ratio = 1.0 * height / h
        if forced:
            ratio = max(w_ratio, h_ratio)
        else:
            ratio = max(1.0, w_ratio, h_ratio)
        return (int(width / ratio), int(height / ratio))

    def getDisplayName(self, display=None, width=None, height=None):
        if display:
            if display == 'cthumb':
                return display
            return 'w%d' % self.getDisplaySize(display)[0]
        return '%dx%d' % (width, height)

    #@PydevCodeAnalysisIgnore
    def createDisplay(self, display):
        # check if display is already here
        display = self.getDisplayName(display)
        if display in self.displays:
            return self.displays[display]
        # check display size with original image size
        width, height = self.getDisplaySize(display)
        if (width, height) == self.image.getImageSize():
            return self.image
        # look for thumbnailer
        thumbnailer = zapi.queryUtility(IThumbnailer)
        if thumbnailer is None:
            thumbnailers = sorted(zapi.getAllUtilitiesRegisteredFor(IThumbnailer), key=lambda x: x.order)
            if thumbnailers:
                thumbnailer = thumbnailers[0]
        # generate thumbnail
        if thumbnailer is not None:
            if display == 'cthumb':
                thumbnail = thumbnailer.createSquareThumbnail(self.image, DefaultDisplays[display])
            else:
                thumbnail = thumbnailer.createThumbnail(self.image, (width, height))
            img = self.displays[display] = Image(thumbnail)
            notify(ObjectCreatedEvent(img))
            locate(img, self.image, '++display++%s' % display)
            return img
        return self.image

    def getDisplay(self, display):
        if display in self.displays:
            return self.displays[display]
        return self.createDisplay(display)

    def clearDisplay(self, display):
        if display in self.displays:
            img = self.displays[display]
            notify(ObjectRemovedEvent(img))
            del self.displays[display]

    def clearDisplays(self):
        [self.clearDisplay(display) for display in self.displays.keys()]


ImageThumbnailAnnotationsKey = 'ztfy.file.thumbnail'

class ThumbnailGeometry(Persistent):

    implements(IThumbnailGeometry)

    position = (None, None)
    size = (None, None)


class ImageThumbnailGeometryAdapter(object):
    """ISquareThumbnail adapter"""

    adapts(IImage)
    implements(IThumbnailGeometry)

    def __init__(self, context):
        self.image = context
        annotations = IAnnotations(context)
        geometry = annotations.get(ImageThumbnailAnnotationsKey)
        if geometry is None:
            geometry = annotations[ImageThumbnailAnnotationsKey] = ThumbnailGeometry()
            self._getGeometry(geometry)
        self.geometry = geometry

    def _getGeometry(self, geometry):
        w, h = IImageDisplay(self.image).getDisplaySize('thumb')
        size = min(w, h)
        geometry.size = (size, size)
        if w > h:
            geometry.position = (int((w - size) / 2), 0)
        else:
            geometry.position = (0, int((h - size) / 2))

    def _getPosition(self):
        return self.geometry.position

    def _setPosition(self, value):
        self.geometry.position = value
        IImageDisplay(self.image).clearDisplay('cthumb')

    position = property(_getPosition, _setPosition)

    def _getSize(self):
        return self.geometry.size

    def _setSize(self, value):
        self.geometry.size = value
        IImageDisplay(self.image).clearDisplay('cthumb')

    size = property(_getSize, _setSize)


@adapter(IImage, IImageModifiedEvent)
def handleModifiedImage(image, event):
    IImageDisplay(image).clearDisplays()


@adapter(IImage, IObjectModifiedEvent)
def handleModifiedImageData(image, event):
    if 'data' in event.descriptions[0].attributes:
        IImageDisplay(image).clearDisplays()
