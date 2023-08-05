.. niteoweb.clickbank documentation master file, created by
   sphinx-quickstart on Thu Jul 15 14:38:10 2010.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to niteoweb.clickbank's documentation!
==============================================

:Project title: niteoweb.clickbank
:Latest version: |release|
:Author: NiteoWeb Ltd.
:Generated: |today|
:License: GPLv2
:URL: http://pypi.python.org/pypi/niteoweb.clickbank
:Docs: http://packages.python.org/niteoweb.clickbank
:Source: http://niteoweb.unfuddle.com/svn/niteoweb_plr/

""""""""""""""""""""""""""""""""

.. topic:: Summary

    Integrates `ClickBank`_ digital products retailer system with `Plone`_ to enable paid memberships on your Plone site.


How it works
============

#. Visitor comes to yoursite.com/order (or similar) and clicks Order link.
#. Visitor is sent to ClickBank's order form (on clickbank.com), 
    where he enters his personal information and performs payment.
#. ClickBank calls-back a special view on your plone site (/@@clickbank),
    which reads POST data from ClickBank, verifies it with your *Secret Key*
    and creates a new member.
#. The following information is stored in member data for later use:
    *product_id*
        ClickBank's Product ID of the purchased item.
        
    *affiliate*
        Affiliate who referred the buyer.
        
    *last_purchase_id*
        ClickBank receipt ID of the last purchase. This field gets updated on
        every recurring payment.

    *last_purchase_timestamp*
        Exact timestamp of the last purchase. This field gets updated on
        every recurring payment.    
    
#. Upon creating a new member, Plone send an email with login password.
#. New member can now login and use the site.

.. note::

    If a member already exists in Plone, then the @@clickbank view simply updates
    *last_purchase_id* and *last_purchase_timestamp* member fields.


Demo
====

You can see this product in action at http://bigcontentsearch.com/order.


Installation
============

To install in your own buildout just add it to your buildout's eggs and zcml listing as normal::

    eggs =
      Plone
      niteoweb.clickbank
      ...
      
    zcml = 
      niteoweb.clickbank
      ...


Configuration
=============

Clickbank
---------

Go to ClickBank and create a Vendor account. Add a test Product of type *Membership*.
Then set the following:

Secret Key
    Choose a strong password here.
    
Thank your page
    Enter a url for your *Thank You* page, normally *http://yoursite.com/thank-you*.
    
Hoplink destination url.
    Enter a url to a site with an order link, normally *http://yoursite.com/order*.

Test credit card.
    Create *Test Credit Card* so you can do test buys.


Plone
-----

#. Go to *Site Setup* -> *ClickBank* control panel form and configure the following fields:

    Secret Key
       Paste the Secret Key you defined above.

#. Create a Page *Order*. Insert the following markup, replacing capitalized strings::

    <a href="http://PRODUCT_ID.VENDOR_ID.pay.clickbank.net">Order a subscription to this site!</a>

#. Create a Page *Thank You*. Insert the following text::

    Thank you for your order!
    Your credit card or bank statement will show a charge by ClickBank or CLKBANK*COM.
    If you have any questions let us know on info@yoursite.com"


Test it
=======

Fire up your browser and point it to your *Order* page. Click on *Order a subscription to this site!*,
fill in your Test Credit Card info with your personal email and purchase the subscription.
Confirm by logging-in to ClickBank and checking to see if there were any purchases. You should also
receive an email with username and password for accessing your site.
    

Known issues
============

The following known issues exist:

    * If members stop paying for monthly or yearly subscriptions, 
        you have to manually delete them from your Plone site.

    * The same as above goes for any chargebacks or refunds. 
        You have to manage them manually.


Running tests
=============

Open up a console and run the following::

    $ cd <workspace>/niteoweb.clickbank
    
    # run a specific test
    $ bin/test -s niteoweb.clickbank -t test_setup

    # run all tests
    $ bin/test -s niteoweb.clickbank

    # calculate code test coverage
    $ bin/coverage-test -s niteoweb.clickbank


Releasing
=========

Open up a console and run the following::

    $ cd <workspace>/niteoweb.clickbank
    
    # use zest.releaser to make an egg distribution and upload it to PyPI
    $ fullrelease
    
    # build sphinx docs and upload them to packages.python.org
    $ bin/sphinxbuilder
    $ python setup.py upload_docs


API
===

Views & Controllers
---------------------------------------------------

.. automodule:: niteoweb.clickbank.browser.clickbank

    .. autoclass:: niteoweb.clickbank.browser.clickbank.ClickBankView
        :members: __call__, _verify_POST, _parse_POST, _create_or_update_member, _email_password, _generate_password

.. automodule:: niteoweb.clickbank.browser.configure_clickbank
    :members:


Utilities
---------------------------------

.. automodule:: niteoweb.clickbank.clickbank_settings
    :members:

.. automodule:: niteoweb.clickbank.interfaces
    :members:

    .. autointerface:: niteoweb.clickbank.interfaces.IClickBankSettings


Tests
-----------------------------------

.. automodule:: niteoweb.clickbank.tests
    :members: 

.. automodule:: niteoweb.clickbank.tests.test_setup
    :members: 

.. automodule:: niteoweb.clickbank.tests.test_clickbank
    :members:


.. include:: ../HISTORY.txt
    

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


.. _ClickBank: http://www.clickbank.com/
.. _Plone: http://plone.org/
