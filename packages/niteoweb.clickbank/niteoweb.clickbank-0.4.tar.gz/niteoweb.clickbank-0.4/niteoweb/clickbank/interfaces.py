# -*- coding: utf-8 -*-
"""
interfaces.py - where all interfaces, events and exceptions live
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
"""

from zope.interface import Interface
from zope import schema

from niteoweb.clickbank import ClickBankMessageFactory


_ = ClickBankMessageFactory

# control panel schema
class IClickBankSettings(Interface):
    """This interface defines fields for ClickBank plone_control_panel configlet."""

    secret_key = schema.Password(title=_(u"ClickBank Secret Key"),
                                  required=True) 

# exceptions
class ClickBankError(Exception):
    """Exception class for niteoweb.clickbank project"""

class POSTVerificationFailedError(ClickBankError):
    """Exception that is raised when we cannot verify a POST from ClickBank."""
    
class MemberCreationFailedError(ClickBankError):
    """Exception that is raised when there is a problem with creating a new member."""
    
class MemberUpdateFailedError(ClickBankError):
    """Exception that is raised when there is a problem with updating member's fields."""