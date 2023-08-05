# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

from zope.interface import Interface
from zope import schema

from niteoweb.clickbank import ClickBankMessageFactory


_ = ClickBankMessageFactory

# control panel schema
class IClickBankConfiguration(Interface):
    """This interface defines the ClickBank plone_control_panel configlet."""

    secret_key = schema.Password(title=_(u"Enter your ClickBank Secret Key"),
                                  required=True) 

# exceptions
class ClickBankError(Exception):
    """Exception class for niteoweb.clickbank project"""

class POSTVerificationFailedError(ClickBankError):
    """Exception that is raised when we cannot verify a POST from ClickBank."""