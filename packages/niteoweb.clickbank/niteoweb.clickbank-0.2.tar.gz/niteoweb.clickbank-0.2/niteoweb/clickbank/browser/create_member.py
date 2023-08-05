# -*- coding: utf-8 -*-
"""A BrowserView that ClickBank calls after a purchase."""

from zope.component import getMultiAdapter
from zope.component import getUtility

from Products.Five.browser import BrowserView

from niteoweb.clickbank.interfaces import POSTVerificationFailedError, IClickBankConfiguration


class ClickBankCreateMemberView(BrowserView):
    """A BrowserView that ClickBank calls after a purchase."""

    def __call__(self):
        """TODO"""

        # redirect to login-form for anonymous
        portal_state = getMultiAdapter((self.context, self.request), name=u'plone_portal_state')
        if portal_state.anonymous():
            self.request.RESPONSE.redirect(self.context.absolute_url() + '/login_form')
            return

        config = getUtility(IClickBankConfiguration)
        secret_key = config.secret_key
            
        self._verify_POST(secret_key)
        data = self._parse_POST()
        self._create_member(data)
        
        return """200 OK"""
        
    def _verify_POST(self, secret_key):
        """Verifies if received POST is a valid ClickBank POST request."""
        return True
        
    def _parse_POST(self):
        """Parses POST from ClickBank and extracts information we need."""
        
        return dict(name='John Smith', email='nejc.zupan@gmail.com')
        
    def _create_member(self, data):
        """Creates a new Plone member."""
        pass
        