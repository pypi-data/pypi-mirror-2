# -*- coding: utf-8 -*-
from zope.interface import implements
from zope.interface import alsoProvides
from zope.interface import noLongerProvides

from z3c.form import form
from z3c.form import button
from z3c.form import field

from plone.app.z3cform.layout import wrap_form
from Products.Five.browser import BrowserView

from plone.folder.interfaces import IOrderableFolder
from yaco.deliverancethemeselector.interfaces import IThemeSelector
from yaco.deliverancethemeselector.interfaces import IDTSSupport
from yaco.deliverancethemeselector.interfaces import IDTSSettingsAnnotations
from yaco.deliverancethemeselector.interfaces \
    import IDeliveranceThemeSelectorSettings

from yaco.deliverancethemeselector import DTSMessageFactory as _

from Products.CMFCore.utils import getToolByName

class ContentControl( BrowserView ):
    """ conditions for presenting various actions
    """

    __allow_access_to_unprotected_subobjects__ = 1

    def __init__( self, context, request ):
        self.context = context
        self.request = request

    def allowEnableThemeSelector( self ):
        """
        """
        return IOrderableFolder.providedBy( self.context ) \
               and not IDTSSupport.providedBy( self.context )

    allowEnableThemeSelector.__roles__ = None

    def allowDisableThemeSelector( self ):
        """
        """
        return IDTSSupport.providedBy( self.context )

    allowDisableThemeSelector.__roles__ = None

    def allowDTSSettings( self ):
        """
        """
        return IDTSSupport.providedBy( self.context )

    allowDTSSettings.__roles__ = None


class ThemeSelectorForm( form.Form ):
    fields = field.Fields(IThemeSelector)
    label = _(u"Select the deliverance theme to be apply in this section")
    description = _(u"Select one item from the drop down menu and press on 'Save' to save your selection")
    ignoreContext = True # don't use context to get widget data

    @button.buttonAndHandler(_(u'Save'))
    def handleApply(self, action):
        data, errors = self.extractData()
        theme = data.get('theme', None)
        plone_utils = getToolByName(self.context, 'plone_utils')

        if not IDTSSupport.providedBy(self.context):
            plone_utils.addPortalMessage(
                _("This object don't have the Deliverance theme selector enable"),
                  "warning")
            self.request.response.redirect(self.context.absolute_url())
            return

        annotation = IDTSSettingsAnnotations(self.context)
        annotation.setTheme(theme)
        plone_utils.addPortalMessage(_("Changes saved"))
        self.request.response.redirect(self.context.absolute_url())

    @button.buttonAndHandler(_(u'Cancel'))
    def handleCancel(self, action):
        plone_utils = getToolByName(self.context, 'plone_utils')
        plone_utils.addPortalMessage(_("Edit cancelled"))
        self.request.response.redirect(self.context.absolute_url())

ThemeSelectorView = wrap_form(ThemeSelectorForm)


class EnableThemeSelectorForm( form.Form ):
    label = _(u"Enable Deliverance Theme Selector for this section")
    description = _(u"To enable a specific theme for this section press 'Save'. "
                     "If you are not sure about this action press 'Cancel'.")

    @button.buttonAndHandler(_(u'Save'))
    def handleApply(self, action):
        alsoProvides(self.context, IDTSSupport)
        self.context.reindexObject(idxs=['object_provides'])
        plone_utils = getToolByName(self.context, 'plone_utils')
        plone_utils.addPortalMessage(_("Deliverance theme selector enable"))
        self.request.response.redirect(
            '%s/%s' % (self.context.absolute_url(), '@@dts-settings'))

    @button.buttonAndHandler(_(u'Cancel'))
    def handleCancel(self, action):
        plone_utils = getToolByName(self.context, 'plone_utils')
        plone_utils.addPortalMessage(_("Accion cancelled"))
        self.request.response.redirect(self.context.absolute_url())

EnableThemeSelectorView = wrap_form(EnableThemeSelectorForm)


class DisableThemeSelectorForm( form.Form ):
    label = _(u"Disable Deliverance Theme Selector for this section")
    description = _(u"You are about to disable the specific theme for this section. "
                     "If you are not sure about this action press 'Cancel' or on 'Save' to make the changes.")

    @button.buttonAndHandler(_(u'Save'))
    def handleApply(self, action):

        plone_utils = getToolByName(self.context, 'plone_utils')
        if not IDTSSupport.providedBy(self.context):
            plone_utils.addPortalMessage(
                _("This object don't have the Deliverance theme selector enable"),
                  "warning")
            self.request.response.redirect(self.context.absolute_url())
            return

        annotation = IDTSSettingsAnnotations(self.context)
        annotation.remove()
        noLongerProvides(self.context, IDTSSupport)
        self.context.reindexObject(idxs=['object_provides'])
        plone_utils.addPortalMessage(_("Deliverance theme selector disable"))
        self.request.response.redirect(self.context.absolute_url())

    @button.buttonAndHandler(_(u'Cancel'))
    def handleCancel(self, action):
        plone_utils = getToolByName(self.context, 'plone_utils')
        plone_utils.addPortalMessage(_("Accion cancelled"))
        self.request.response.redirect(self.context.absolute_url())

DisableThemeSelectorView = wrap_form(DisableThemeSelectorForm)
