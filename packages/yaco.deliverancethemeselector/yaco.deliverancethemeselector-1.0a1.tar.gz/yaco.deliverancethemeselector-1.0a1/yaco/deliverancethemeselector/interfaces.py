# -*- coding: utf-8 -*-

from zope.interface import Interface
from zope.interface import Attribute
from zope import schema

from yaco.deliverancethemeselector import DTSMessageFactory as _

class IDeliveranceThemeSelectorSettings(Interface):
    """Global settings. This describes records stored in the
       configuration registry and obtainable via plone.registry.
    """

    availableThemes = schema.List(
        title = _(u"Available Themes"),
        description = _(u"List of available themes to use with deliverance. "
                         "Format is 'ThemerName:ClassName'"),
        value_type = schema.BytesLine(title = _(u'Item')),
    )

class IDTSSupport(Interface):
    """Marker Interface for content objects with a special theme
    """

class IDTSSettingsAnnotations(Interface):
    """Annotation to store the theme settings.
    """
    key = Attribute("The name of the annotate key")
    xheader = Attribute("The custom X-Header")

    def setTheme(self):
        """Set the theme to the X-Header
        """
        pass

    def getTheme(self):
        """Get the theme
        """
        pass

    def getHeader(self):
        """Get the X-Header
        """
        pass

    def remove(self):
        """Remove the annotation from the context
        """
        pass

class IThemeSelector(Interface):
    """base form settings
    """

    theme = schema.Choice(
        title = _(u"Theme"),
        description =_(u"Select the deliverance theme."),
        vocabulary = "yaco.deliverancethemeselector.vocabularies.themes",
        required = True)
