# -*- coding: utf-8 -*-
"""
test_clickbank.py - test all aspects of @@clickbank
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
"""

import unittest
from DateTime import DateTime
from mocker import Mocker, ARGS, KWARGS

from Products.CMFCore.utils import getToolByName

from niteoweb.clickbank.tests import ClickBankIntegrationTestCase, MockMailHostTestCase


class TestClickBank(ClickBankIntegrationTestCase, MockMailHostTestCase):
    """Test all aspects of @@clickbank."""

    def afterSetUp(self):
        """Prepare testing environment."""
        super(TestClickBank, self).afterSetUp()
        self.view = self.portal.restrictedTraverse('clickbank')
        self.mailhost = self.portal.MailHost
        self.registration = getToolByName(self.portal, 'portal_registration')

    def test_call_with_no_POST(self):
        """Test @@clicbank's response when POST is empty."""
        html = self.view()
        self.failUnless('No POST request.' in html)

    def test_call_with_invalid_POST(self):
        """Test @@clicbank's response when POST cannot be verified."""

        # put something into self.request.form so it's not empty
        self.portal.REQUEST.form = dict(value='non empty value')
        
        # mock return from _verify_POST
        mocker = Mocker()
        mock_view = mocker.patch(self.view)
        mock_view._verify_POST(ARGS, KWARGS)
        mocker.result(False)
        mocker.replay()
        
        # test
        html = self.view()
        self.failUnless('POST verification failed.' in html)
        mocker.restore()

    def test_call_with_valid_POST(self):
        """Test @@clicbank's response when POST is valid."""

        # put something into self.request.form so it's not empty
        self.portal.REQUEST.form = dict(value='non empty value')
        
        # mock return from _verify_POST
        mocker = Mocker()
        mock_view = mocker.patch(self.view)
        mock_view._verify_POST(ARGS, KWARGS)
        mocker.result(True)

        # mock return from _parse_POST
        mock_view._parse_POST(ARGS, KWARGS)
        mocker.result(dict(username='username'))

        # mock return from _create_or_update_member
        mock_view._create_or_update_member(ARGS, KWARGS)
        mocker.result(True)
        mocker.replay()
                
        # test
        html = self.view()
        self.failUnless('POST successfully parsed.' in html)
        mocker.restore()

    def test_generate_password(self):
        """Test password generation."""
        password = self.view._generate_password(8)
        self.assertEqual(len(password), 8)

    def test_verify_POST(self):
        """Test POST verification process."""
        params = dict(
                    ccustname = 'test',
                    ccustemail = 'test',
                    ccustcc = 'test',
                    ccuststate = 'test',
                    ctransreceipt = 'test',
                    cproditem = 'test',
                    ctransaction = 'test',
                    ctransaffiliate= 'test',
                    ctranspublisher= 'test',
                    cprodtype= 'test',
                    cprodtitle= 'test',
                    ctranspaymentmethod= 'test',
                    ctransamount= 'test',
                    caffitid= 'test',
                    cvendthru = 'test',
                    cverify = '1B8383BF',
                    secret_key= 'secret',
                    )

        verified = self.view._verify_POST(params)
        self.failUnless(verified)

    def test_parse_POST(self):
        """Test that POST parameters are correctly mirrored into member fields."""
        params = dict(
                    ccustname = 'fullname',
                    ccustemail = 'email',
                    ctransreceipt = 'last_purchase_id',
                    cproditem = 'product_id',
                    ctransaffiliate= 'affiliate',
                    ctranstime = '1262300400'
                    )
        
        expected = dict(
                        fullname = 'fullname',
                        username = 'email',
                        email = 'email',
                        product_id = 'product_id',
                        affiliate = 'affiliate',
                        last_purchase_id = 'last_purchase_id',
                        last_purchase_timestamp = DateTime('2010/01/01'),
                        )

        result = self.view._parse_POST(params)
        self.assertEqual(result, expected)

    def test_create_member(self):
        """Test creating a new member out of POST parameters."""

        test_data = dict(
                    username = 'john@smith.name',
                    password = 'secret123',
                    email = 'john@smith.name',
                    fullname = 'John Smith',
                    product_id = '1',
                    affiliate = 'Jane Affiliate',
                    last_purchase_id = 'invoice_1',
                    last_purchase_timestamp = DateTime('2010/01/01'),
                    )

        # set From SMTP header
        self.portal.email_from_address = "mail@plone.test"
        
        # mock return from _generate_password
        mocker = Mocker()
        mock_view = mocker.patch(self.view)
        mock_view._generate_password(ARGS, KWARGS)
        mocker.result(test_data['password'])
        mocker.replay()
        
        # run method
        self.view._create_or_update_member(test_data['username'], test_data)
        
        # test member
        member = self.portal.acl_users.getUserById(test_data['username'])
        self.assertEqual(member.getProperty('email'), test_data['email'])
        self.assertEqual(member.getProperty('fullname'), test_data['fullname'])
        self.assertEqual(member.getProperty('product_id'), test_data['product_id'])
        self.assertEqual(member.getProperty('affiliate'), test_data['affiliate'])
        self.assertEqual(member.getProperty('last_purchase_id'), test_data['last_purchase_id'])
        self.assertEqual(member.getProperty('last_purchase_timestamp'), test_data['last_purchase_timestamp'])
        
        # test email
        self.assertEqual(len(self.mailhost.messages), 1)
        msg = self.mailhost.messages[0]
        self.failUnless('To: %s' %test_data['email'] in msg)
        self.failUnless('Subject: =?utf-8?q?Your_Plone_site_login_credentials' in msg)
        self.failUnless('u: %s' %test_data['username'] in msg)
        self.failUnless('p: %s' %test_data['password'] in msg)
        

    def test_update_member(self):
        """Test updating an existing member with POST parameters."""

        old_data = dict(
                            username = 'john@smith.name',
                            email = 'john@smith.name',
                            last_purchase_id = 'invoice_1',
                            last_purchase_timestamp = DateTime('2010/01/01'),
                            )
        new_data = old_data
        new_data['last_purchase_id'] = 'invoice_2'
        new_data['last_purchase_timestamp'] = DateTime('2010/02/02')
        
        # create a member in advance so POST parameters will perform UPDATE instead of CREATE
        self.registration.addMember(old_data['username'], 'test_password', properties=old_data)
                        
        # run method
        self.view._create_or_update_member(new_data['username'], new_data)
        
        # test member
        member = self.portal.acl_users.getUserById(new_data['username'])
        self.assertEqual(member.getProperty('last_purchase_id'), new_data['last_purchase_id'])
        self.assertEqual(member.getProperty('last_purchase_timestamp'), new_data['last_purchase_timestamp'])
        
        # test email
        self.assertEqual(len(self.mailhost.messages), 0)

    def test_email_password(self):
        """Test headers and text of email that is sent to newly created member."""
        
        test_data = dict(
                    username = 'john@smith.name',
                    password = 'secret123',
                    email = 'john@smith.name',
                    fullname = 'John Smith',
                    )

        # set portal properties
        self.portal.title = u'ClickBank Integration Site'
        self.portal.email_from_address = "mail@plone.test"
        
        # run method
        self.view._email_password(test_data['username'], test_data['password'], test_data)
        
        # test email
        self.assertEqual(len(self.mailhost.messages), 1)
        msg = self.mailhost.messages[0]

        # test email headers
        self.failUnless('To: %s' %test_data['email'] in msg)
        self.failUnless('From: %s' %self.portal.email_from_address in msg)
        self.failUnless('Subject: =?utf-8?q?Your_ClickBank_Integration_Site_login_credentials' in msg)
        
        # test email body text
        self.failUnless('Hello %s,' %test_data['fullname'] in msg)
        self.failUnless('u: %s' %test_data['username'] in msg)
        self.failUnless('p: %s' %test_data['password'] in msg)
        self.failUnless('You can now login at http://nohost/plone/login_form'in msg)
        self.failUnless('let us know on %s' %self.portal.email_from_address in msg)
        self.failUnless('Best wishes,\n%s Team' %self.portal.title in msg)


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestClickBank))
    return suite
