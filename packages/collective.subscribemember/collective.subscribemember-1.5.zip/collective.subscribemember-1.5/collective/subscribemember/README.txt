Overview
========

This package provides paid member subscription functionality for a Plone site, including 
subscription renewals, membership expiration, and CSV import/export of site members.

Member subscription payments are handled by PloneGetPaid: http://www.plonegetpaid.com and
member management is handled by Remember: http://plone.org/products/remember .

Dependencies
============

* Plone 3+ (tested with 3.2.x/3.3.x)
* Remember (tested with 1.1b3)
* Membrane (tested with 1.1b5)
* PloneGetPaid (tested with 0.7.9/0.8.8). Currently only works with synchronous (onsite) payment processors, although one production install has been customised to work with PayPal. 
* archetypes.schemaextender

Installation
============

Buildout
--------

*   The required configuration you need in your buildout can be seen here: http://dev.plone.org/collective/browser/collective.subscribemember/trunk/buildout.cfg .
    Just copy this into your existing buildout (or use it as is) and run buildout.

*   Restart Zope.

*   Go to the Site Setup page in the Plone interface and click on the Add/Remove Products
    link. Choose collective.subscribemember (check its checkbox) and click the Install
    button. If collective.subscribemember is not available on the Add/Remove Products
    list, it usually means that the product did not load due to missing prerequisites.

*   From the main Site Setup page, click on Zope Management Interface, portal_properties, then
    subscribemember_properties and enter the available membership subscription options
    in the `membertypes` field. Each subscription option is on a new line and the semicolon
    separated text values are as follows::
    
    > Label for dropdown menu;Subscription amount as an integer,['List of roles paid-up member is granted'],Number of years subscribed as an integer value,Other text description for membership type (optional)
    > E.g. Physician,15,['Member'],1,STUD-2
    
    Following this, you can enter the `member_import_directory` where collective.subscribemember
    should look for a CSV file containing member data to import and also the `reminder_email_trigger`,
    which is the number of days prior to the subscription expiry date that a member should be sent a
    reminder email asking them to renew their subscription.
    
Credits
=======

* Tim Knapp - main package author.
* netCorps/International Society of Indoor Air Quality and Climate/Madtek - sponsoring
  the development of the package.

License
=======

Distributed under the GPL.

See docs/LICENSE.txt and docs/LICENSE.GPL for details.
