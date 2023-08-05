# -*- coding: utf-8 -*-
"""Test installation of PLR into Plone."""

import unittest

from Products.CMFCore.utils import getToolByName

from niteoweb.clickbank.tests import ClickBankIntegrationTestCase

class TestSetup(ClickBankIntegrationTestCase):
    """Test installation of PLR."""
        
    def test_disable_registration_for_anonymous(self):
        """Test if anonymous are prevented to register to the site."""
        # The API of the permissionsOfRole() function sucks - it is bound too
        # closely up in the permission management screen's user interface
        self.failIf('Add portal member' in [r['name'] for r in 
                                self.portal.permissionsOfRole('Anonymous') if r['selected']])

    def test_view_exists(self):
        """Test if @@cb-create-member exists."""
        pass
        # TODO

    def test_cb_fields_added(self):
        """Test if ClickBank-specific fields were added to memberdata."""
        pass
        # TODO
        # 
        # purchase_id, product_id, purchase_time
        # 

    def test_control_panel_configlet_installed(self):
        """Test if Plone Control Panel configlet for ClickBank was successfully installed
        and behaves like it should."""

        
def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestSetup))
    return suite
