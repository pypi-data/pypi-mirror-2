# -*- coding: utf-8 -*-
"""A local utility for storing ClickBank configuration."""

from persistent import Persistent
from zope.interface import implements

from niteoweb.clickbank.interfaces import IClickBankConfiguration


class ClickBankConfiguration(Persistent):
    implements(IClickBankConfiguration)

    secret_key = ''