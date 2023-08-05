"""Test setup for integration and functional tests.

When we import PloneTestCase and then call setupPloneSite(), all of
Plone's products are loaded, and a Plone site will be created. This
happens at module level, which makes it faster to run each test, but
slows down test runner startup.
"""

import os, tempfile, shutil
from zope.component import getUtility, getMultiAdapter, getSiteManager
from Products.Five import zcml
from Products.Five import fiveconfigure

from Testing import ZopeTestCase as ztc

from Products.CMFCore.utils  import getToolByName
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import onsetup
from Products.remember.tests.base import makeContent, mem_data, def_mem_data
from Products.PloneGetPaid.tests.base import PloneGetPaidFunctionalTestCase
from Products.MailHost.interfaces import IMailHost
from Products.SecureMailHost.SecureMailHost import SecureMailHost
from collective.subscribemember import config
import DateTime

#HACK due to 2.4 functools
try:
    from functools import partial
except ImportError:
    def partial(func_, *args, **kwargs):
        def newfunc(*fargs, **fkwargs):
            return func_(*(args + fargs), **dict(kwargs, **fkwargs))
        newfunc.func = func_
        newfunc.args = args
        newfunc.keywords = kwargs
        try:
            newfunc.__name__ = func_.__name__
        except TypeError: # python 2.3
            pass
        return newfunc
    import functools
    functools.partial = partial

from testfixtures import Replacer, test_time
from DateTime import DateTime

# When ZopeTestCase configures Zope, it will *not* auto-load products
# in Products/. Instead, we have to use a statement such as:
#   ztc.installProduct('SimpleAttachment')
# This does *not* apply to products in eggs and Python packages (i.e.
# not in the Products.*) namespace. For that, see below.
# All of Plone's products are already set up by PloneTestCase.

ztc.installProduct('remember')
ztc.installProduct('membrane')
ztc.installProduct('PloneGetPaid')

@onsetup
def setup_product():
    """Set up the package and its dependencies.

    The @onsetup decorator causes the execution of this body to be
    deferred until the setup of the Plone site testing layer. We could
    have created our own layer, but this is the easiest way for Plone
    integration tests.
    """

    # Load the ZCML configuration for the example.tests package.
    # This can of course use <include /> to include other packages.

    fiveconfigure.debug_mode = True
    import collective.subscribemember
    import Products.remember
    import Products.membrane
    import getpaid.nullpayment
    import Products.PloneGetPaid
    zcml.load_config('configure.zcml', Products.PloneGetPaid)
    zcml.load_config('configure.zcml', getpaid.nullpayment)
    zcml.load_config('configure.zcml', Products.membrane)
    zcml.load_config('configure.zcml', Products.remember)
    zcml.load_config('configure.zcml', collective.subscribemember)
    fiveconfigure.debug_mode = False

    # We need to tell the testing framework that these products
    # should be available. This can't happen until after we have loaded
    # the ZCML. Thus, we do it here. Note the use of installPackage()
    # instead of installProduct().
    # This is *only* necessary for packages outside the Products.*
    # namespace which are also declared as Zope 2 products, using
    # <five:registerPackage /> in ZCML.

    # We may also need to load dependencies, e.g.:
    #   ztc.installPackage('borg.localrole')
    ztc.installPackage('collective.subscribemember')

# The order here is important: We first call the (deferred) function
# which installs the products we need for this product. Then, we let
# PloneTestCase set up this product on installation.

setup_product()
ptc.setupPloneSite(extension_profiles=('collective.subscribemember:testing',))

class TestCase(ptc.PloneTestCase):
    """We use this base class for all the tests in this package. If
    necessary, we can put common utility or setup code in here. This
    applies to unit test cases.
    """

class FunctionalTestCase(PloneGetPaidFunctionalTestCase):
    """We use this class for functional integration tests that use
    doctest syntax. Again, we can put basic common utility or setup
    code in here.
    """

    def beforeTearDown(self):
        self.replacer.restore()

    def afterSetUp(self):
        config.TESTING = True
        PloneGetPaidFunctionalTestCase.afterSetUp(self)

        # Setup mock Secure Mail Host
        self.loginAsPortalOwner()
        sm = getSiteManager(self.portal)
        sm.unregisterUtility(provided=IMailHost)
        self.dummyMailHost = MockSecureMailHost('dMailhost')
        sm.manage_changeProperties({'email_from_address': 'test@test.com'})
        sm.registerUtility(self.dummyMailHost, IMailHost)

        # Set mail host for tools which use getToolByName() look up
        self.MailHost = self.dummyMailHost
 
        # Make sure that registration tool uses mail host mock
        rtool = getToolByName(self.portal, 'portal_registration')
        rtool.MailHost = self.dummyMailHost

        def raising(self, info):
            import traceback
            traceback.print_tb(info[2])
            print info[1]            
        from Products.SiteErrorLog.SiteErrorLog import SiteErrorLog
        SiteErrorLog.raising = raising

        self.createNewMember('member')

        proptool = getToolByName(self.portal, 'portal_properties')
        tmp = tempfile.mkdtemp()
        importdir = os.path.join(tmp, 'testfiles')
        setattr(proptool.subscribemember_properties, 'member_import_directory', importdir)
        testfiles = os.path.join(os.path.dirname(__file__), 'testfiles')
        shutil.copytree(testfiles, importdir)

        self.replacer = Replacer()
        self.days = 0        
        self.date = None
        case = self
        def custom__init__(self,*args, **kw):
            try:
                if args == () and kw == {}:
                    from datetime import timedelta, datetime
                    if case.date is not None: 
                        now = datetime(*case.date)
                    else:
                        now = datetime.today()
                    t = now + timedelta(days=case.days)
                    self._parse_args(str(t))
                else:
                    self._parse_args(*args, **kw)
            except (self.DateError, self.TimeError, self.DateTimeError):
                raise
        self.replacer.replace('DateTime.DateTime.__init__',custom__init__)
        
    def createNewMember(self, id):
        mdata = self.portal.portal_memberdata
        password = 'secret'
        mem = makeContent(mdata, id, 'Member')
        values = {'fullname': 'New Member',
                  'billFirstLine': 'My Address',
                  'billCity': 'My City',
                  'billState': 'NZ-WGN',
                  'billPostCode': '1234',
                  'billCountry': 'NZ',
                  'phoneNumber': 1234567,
                  'memberType': '3',
                  'email': 'noreply@xxxxxxxxyyyyyy.com',
                  'password': password,
                  'confirm_password': password,
                  }
        # processForm triggers the state change to an active state
        mem.processForm(values=values)

    def deleteTestMember(self, id):
        mtool = getToolByName(self.portal, 'portal_membership')
        testmember = mtool.getMemberById(id)
        testmember.delete('Remove') 

    def restore(self):
        self.replacer.restore()

    def setToday(self,y,m,d):
        self.date = (y,m,d)

    def setDaysOffset(self, days):
        self.days += days
        

class MockSecureMailHost(SecureMailHost):
    """Mock SecureMailHost"""
    
    meta_type = 'Dummy secure Mail Host'
    def __init__(self, id):
        self.id = id
        
        # Use these two instance attributes to check what email has been sent
        self.sent = []        
        self.mto = None

    def send(self, msg, mto=None, mfrom=None, subject=None):
        return self._send(mfrom, mto, msg)

    def _send(self, mfrom, mto, messageText, debug=False):
        self.sent.append(messageText)
        self.mto = mto