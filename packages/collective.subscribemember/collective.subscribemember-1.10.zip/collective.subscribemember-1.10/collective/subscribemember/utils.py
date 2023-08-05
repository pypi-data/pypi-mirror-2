import logging
from DateTime import DateTime
from zope.component import getUtility, queryUtility
from zope.app.component.hooks import getSite
from zope.interface import implements
from plone.i18n.normalizer.interfaces import IURLNormalizer
from collective.subscribemember.interfaces import IMemberTypesGetter, IMemberImporter
from collective.subscribemember import config
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.interfaces import ISiteRoot

logging.getLogger(config.PROJECTNAME)

class MemberTypesGetter:
    implements(IMemberTypesGetter)
    
    def return_member_types(self):
        membertypes = {}
        context = getUtility(ISiteRoot)
        propstool = getToolByName(context, 'portal_properties')
        subscribemember_props = propstool.subscribemember_properties
        for i, line in enumerate(getattr(subscribemember_props, 'membertypes', [])):
            membervalues = line.split(';')
            membervalues[1] = int(membervalues[1])
            membervalues[3] = int(membervalues[3])
            membervalues[2] = eval(membervalues[2], {'__builtins__': {}})
            membertypes[str(i+1)] = membervalues
        return membertypes
    
    
class MemberImporter:
    implements(IMemberImporter)
    
    def import_member(self, memberdata, imported):
        context = getSite()
        i18n = queryUtility(IURLNormalizer)
        log = 'Processing %s...' % (memberdata[1],)
        logging.info(log)
        if not self.been_created(memberdata, context):
            id = memberdata[0]
            id = i18n.normalize(id)
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
            
            mdata = getToolByName(context, 'portal_memberdata')
            mdata.invokeFactory(id=id, type_name='Member') 
            mem = getattr(mdata, id)
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
            imported = imported + 1
            if not config.TESTING:
                log = "Created %s: %s" % (id, values)
                logging.info(log)
        else:
            if not config.TESTING:
                log = "Didn't create %s: Member already exists" % (memberdata[2],)
                logging.info(log)
                
        return imported
        
    def been_created(self, memberdata, context):
        id = memberdata[0]
        catalog = getToolByName(context, 'portal_catalog')
        existing = catalog(id=id, portal_type='Member')
        return len(existing) > 0