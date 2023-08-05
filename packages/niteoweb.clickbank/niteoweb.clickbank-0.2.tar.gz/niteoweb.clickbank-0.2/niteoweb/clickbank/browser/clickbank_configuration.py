# -*- coding: utf-8 -*-
"""A BrowserView for ClickBank configuration."""

from zope.component import getUtility
from zope.formlib import form

from plone.app.controlpanel.form import ControlPanelForm

from niteoweb.clickbank import ClickBankMessageFactory
from niteoweb.clickbank.interfaces import IClickBankConfiguration


_ = ClickBankMessageFactory

def clickbank_configuration(context):
    return getUtility(IClickBankConfiguration)

class ClickBankConfigurationForm(ControlPanelForm):
    form_fields = form.Fields(IClickBankConfiguration)
    form_name = _("ClickBank configuration")
    label = _(u"ClickBank configuration form")
    description = _(u"Enter your ClickBank settings.")