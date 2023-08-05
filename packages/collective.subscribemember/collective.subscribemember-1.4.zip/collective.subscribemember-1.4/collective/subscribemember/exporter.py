import csv
from zope.interface import implements
from zope.component import getUtility
from interfaces import IMemberExporter
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.interfaces import ISiteRoot
from collective.subscribemember.interfaces import IMemberTypesGetter

class MemberExporter(object):
    """ """
    implements(IMemberExporter)

    def process(self, file):
        MEMBERTYPES = getUtility(IMemberTypesGetter).return_member_types()
        memprops = {}
        site = getUtility(ISiteRoot)
        workflow = getToolByName(site, 'portal_workflow')
        catalog = getToolByName(site, 'portal_catalog')
        members = catalog(portal_type='Subscribemember')
        csvfile = csv.writer(file)
        csvfile.writerow(["MemberID", "MemberType", "Fullname", "Address 1", "Address 2", "City", "State", "Postal Code", "Country", "Email", "Publish", "Phone", "Date Joined", "Date Renewed", "Expiration Date", "Payment Status"])
        for member in members:
            memobj = member.getObject()
            if memobj.getMakePrivate() == True:
                publish = 'N'
            else:
                publish = 'Y'
            if memobj.getDonationAmount():
                donation = memobj.getDonationAmount()
            else:
                donation = ''
            expirydate = ''
            if memobj.getMemberExpiryDate(): expirydate = memobj.getMemberExpiryDate().strftime('%d/%m/%Y')
            joineddate = ''
            if memobj.getMemberJoinedDate(): joineddate = memobj.getMemberJoinedDate().strftime('%d/%m/%Y')
            reneweddate = ''
            if memobj.getMemberRenewedDate(): reneweddate = memobj.getMemberRenewedDate().strftime('%d/%m/%Y')
            memprops = [
                        memobj.getId(),
                        MEMBERTYPES[memobj.Schema()['memberType'].get(memobj)][0],
                        memobj.getFullname(),
                        memobj.Schema()['billFirstLine'].get(memobj),
                        memobj.Schema()['billSecondLine'].get(memobj),
                        memobj.Schema()['billCity'].get(memobj),
                        memobj.Schema()['billState'].get(memobj),
                        memobj.Schema()['billPostalCode'].get(memobj),
                        memobj.Schema()['billCountry'].get(memobj),
                        memobj.getEmail(),
                        publish,
                        memobj.Schema()['phoneNumber'].get(memobj),
                        joineddate,
                        reneweddate,
                        expirydate,
                        workflow.getInfoFor(memobj, 'review_state')
                       ]
            csvfile.writerow(memprops)