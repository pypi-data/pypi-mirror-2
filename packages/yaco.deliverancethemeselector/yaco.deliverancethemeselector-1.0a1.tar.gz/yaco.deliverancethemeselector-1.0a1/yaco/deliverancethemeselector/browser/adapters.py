# -*- coding: utf-8 -*-
"""
   This module provides an adapter for a store and manage the theme settings
"""

from persistent.dict import PersistentDict
from zope.annotation.interfaces import IAnnotations
from zope.interface import implements

from yaco.deliverancethemeselector.config import ANNOTATION_KEY
from yaco.deliverancethemeselector.config import XHEADER
from yaco.deliverancethemeselector.interfaces import IDTSSettingsAnnotations


class DTSSettingsAnnotations(object):
    """
    """
    implements(IDTSSettingsAnnotations)

    key = ANNOTATION_KEY
    xheader = XHEADER

    def __init__(self, context):
        self.context = context
        annotations = IAnnotations(self.context)

        self._metadata = annotations.get(self.key, None)
        if self._metadata is None:
            self._metadata = PersistentDict()
            annotations[self.key] = self._metadata

    def setTheme(self, theme):
        self._metadata['theme'] = theme

    def getTheme(self):
        return self._metadata.get('theme', '')

    def getHeader(self):
        return self.xheader

    def remove(self):
        annotations = IAnnotations(self.context)
        annotations.__delitem__(self.key)
