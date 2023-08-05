# -*- coding: utf-8 -*-
"""
clickbank.py - handle ClickBank purchase notifications
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
"""
import hashlib
import random
import string

from zope.component import getUtility
from DateTime import DateTime

from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName

from niteoweb.clickbank.interfaces import IClickBankSettings


class ClickBankView(BrowserView):
    """A BrowserView that ClickBank calls after a purchase."""

    def __call__(self):

        # check for POST request
        if not self.request.form:
            self.request.response.setStatus(400, lock=True)
            return 'No POST request.'
                
        # verify POST request
        settings = getUtility(IClickBankSettings)
        params = dict(self.request.form)
        params['secret_key'] = settings.secret_key

        if not self._verify_POST(params):
            self.request.response.setStatus(400, lock=True)
            return 'POST verification failed.'

        # parse and handle POST
        data = self._parse_POST(params)
        self._create_or_update_member(data['username'], data)
        return 'POST successfully parsed.'

    def _verify_POST(self, params):
        """Verifies if received POST is a valid ClickBank POST request."""
        request_data = "%(ccustname)s|%(ccustemail)s|%(ccustcc)s|%(ccuststate)s|%(ctransreceipt)s|%(cproditem)s|%(ctransaction)s|%(ctransaffiliate)s|%(ctranspublisher)s|%(cprodtype)s|%(cprodtitle)s|%(ctranspaymentmethod)s|%(ctransamount)s|%(caffitid)s|%(cvendthru)s|%(secret_key)s" % params
        return params['cverify'] == hashlib.sha1(request_data).hexdigest()[:8].upper()

    def _parse_POST(self, params):
        """Parses POST from ClickBank and extracts information we need."""
        return {'username': params['ccustemail'],
                'email': params['ccustemail'],
                'fullname': params['ccustname'],
                'product_id': params['cproditem'],
                'affiliate': params['ctransaffiliate'],
                'last_purchase_id': params['ctransreceipt'],
                'last_purchase_timestamp': DateTime(int(params['ctranstime']))}
        
    def _create_or_update_member(self, username, data):
        """Creates a new Plone member. In case the member already exists,
        this method simply updates member's fields."""
        
        registration = getToolByName(self.context, 'portal_registration')
        password = self._generate_password()

        # update or create member
        member = self.context.acl_users.getUserById(username)
        if member:
            # update existing member
            member.setProperties(mapping={
                'last_purchase_id': data['last_purchase_id'],
                'last_purchase_timestamp': data['last_purchase_timestamp'],
            })
        else:
            # create a new member
            member = registration.addMember(username, password, properties=data)
            self._email_password(username, password)
        
    def _email_password(self, mto, password, mfrom=None):
        """Send an email with member's password.
        :param mto: email receipient
        :type mto: string
        
        :param length: number of characters to generate
        :type length: integer
        """
        
        if not mfrom:
            mfrom = self.context.email_from_address
        
        mailhost = getToolByName(self.context, 'MailHost')
        mailhost.send("Your password: %s" % password, mto=mto, mfrom=mfrom, subject=u"Registration successful", charset='utf-8')
        
    def _generate_password(self, length=8, include=string.letters + string.digits):
        """Generate random password in base64.

        :param include: set of characters to choose from
        :type include: string
        
        :param length: number of characters to generate
        :type length: integer
        
        :returns: a random password
        :rtype: string
        """
        random.seed()
        return ''.join(random.sample(include, length))