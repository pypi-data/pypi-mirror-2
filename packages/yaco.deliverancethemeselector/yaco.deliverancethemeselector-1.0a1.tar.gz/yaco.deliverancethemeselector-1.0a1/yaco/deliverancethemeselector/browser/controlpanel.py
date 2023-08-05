# -*- coding: utf-8 -*-

from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper

from yaco.deliverancethemeselector.interfaces import IDeliveranceThemeSelectorSettings
from plone.z3cform import layout

class DeliveranceThemeSelectorPanelForm(RegistryEditForm):
    """
    """
    schema = IDeliveranceThemeSelectorSettings

DeliveranceThemeSelectorPanelView = layout.wrap_form(
    DeliveranceThemeSelectorPanelForm,
    ControlPanelFormWrapper)
