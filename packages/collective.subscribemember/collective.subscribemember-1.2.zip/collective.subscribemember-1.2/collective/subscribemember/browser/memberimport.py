import re, os, csv, logging
from DateTime import DateTime
from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.interfaces import ISiteRoot
from collective.subscribemember import config
from collective.subscribemember.interfaces import IMemberTypesGetter
# To temporarily fixup the display of the PGP portlet
from Products.PloneGetPaid.interfaces import IBuyableMarker
from zope.component import getUtility
from zope.interface import noLongerProvides

logging.getLogger(config.PROJECTNAME)

class MemberImport(BrowserView):
    """Import members from a CSV file"""
    
    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.imported = 0
    
    def __call__(self):
        file = self.getFile()
        if file:
            reader = csv.reader(file)
            for i, line in enumerate(reader):
                if i<>0:
                    self.importMember(line)
            log = "Imported %s members" % str(self.imported) 
            logging.info(log)
            file.close()
    
    def getFile(self):
        """
        Get the first CSV file and return it
        """
        filenames = sorted(os.listdir(config.MEMBER_IMPORT_DIRECTORY))
        for filename in filenames:
            if re.search('.csv$', filename):
                file = open(os.path.join(config.MEMBER_IMPORT_DIRECTORY, filename), 'r')
                return file
            
    def importMember(self, memberdata):
        log = 'Processing %s...' % (memberdata[1],)
        logging.info(log)
        if not self.beenCreated(memberdata):
            id = memberdata[0]
            password = memberdata[15]
    
            if memberdata[9] == 'Y':
                makePrivate = 1
            else:
                makePrivate = 0
    
            if memberdata[11] != '':
                try:
                    memberJoinedDate = DateTime(memberdata[11], datefmt='international')
                except (DateTime.TimeError, DateTime.SyntaxError):
                    # Work around for incorrect
                    # dates set in spreadsheet
                    memberJoinedDate = DateTime(datefmt='international')-30
            else:
                memberJoinedDate = DateTime(datefmt='international')-30
            
            if memberdata[12] != '':
                try:
                    memberRenewedDate = DateTime(memberdata[12], datefmt='international')
                except (DateTime.TimeError, DateTime.SyntaxError):
                    # Work around for incorrect
                    # dates set in spreadsheet
                    memberRenewedDate = ''
            else:
                memberRenewedDate = ''
            
            memberExpiryDate = DateTime(memberdata[13], datefmt='international')
            
            mdata = getToolByName(self.context, 'portal_memberdata')
            mem = makeContent(mdata, id, 'Member')
            values = {'fullname': unicode(memberdata[2], 'utf-8'),
                      'billFirstLine': unicode(memberdata[3], 'utf-8'),
                      'billCity': unicode(memberdata[4], 'utf-8'),
                      'billState': unicode(memberdata[5], 'utf-8'),
                      'billPostalCode': memberdata[6],
                      'billCountry': unicode(memberdata[7], 'utf-8'),
                      'phoneNumber': int(memberdata[10]),
                      'memberType': memberdata[1],
                      'email': memberdata[8],
                      'password': password,
                      'confirm_password': password,
                      }
            # processForm triggers the state change to an active state
            mem.processForm(values=values)
            if makePrivate:
                mem.setMakePrivate(makePrivate)
                values['make_private'] = makePrivate
            if memberRenewedDate != '':
                mem.Schema()['memberRenewedDate'].set(mem, memberRenewedDate)
                values['memberRenewedDate'] = memberRenewedDate.Date()
            mem.Schema()['memberJoinedDate'].set(mem, memberJoinedDate)
            values['memberJoinedDate'] = memberJoinedDate.Date()                
            mem.Schema()['memberExpiryDate'].set(mem, memberExpiryDate)
            values['memberExpiryDate'] = memberExpiryDate.Date()
            membertypes = getUtility(IMemberTypesGetter).return_member_types()
            subscribememberroles = membertypes[mem.Schema()['memberType'].get(mem)][2]
            roles = list(mem.getRoles())
            for role in subscribememberroles:
                if not role in mem.getRoles():
                    roles.append(role)
            # Remove the temporarily assigned Authenticated role
            if 'Authenticated' in roles:
                roles.remove('Authenticated')
            mem.setRoles(roles)
            log = "Set the following role for %s: %s" % (memberdata[2], role)
            logging.info(log)
            # Set an imported flag
            setattr(mem, 'importedmember', True)
            mem.reindexObject()
            self.imported = self.imported + 1
            if not config.TESTING:
                log = "Created %s: %s" % (id, values)
                logging.info(log)
        else:
            if not config.TESTING:
                log = "Didn't create %s: Member already exists" % (memberdata[2],)
                logging.info(log)
        
    def beenCreated(self, memberdata):
        id = memberdata[0]
        catalog = getToolByName(self.context, 'portal_catalog')
        existing = catalog(id=id, portal_type='Member')
        return len(existing) > 0        
        

def makeContent(container, id, portal_type, title=None):
    container.invokeFactory(id=id, type_name=portal_type)
    o = getattr(container, id)
    if title is not None:
        o.setTitle(title)
    return o