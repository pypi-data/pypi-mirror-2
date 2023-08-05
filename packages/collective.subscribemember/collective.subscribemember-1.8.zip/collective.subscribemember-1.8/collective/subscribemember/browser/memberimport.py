import re, os, csv, logging
import transaction
from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.interfaces import ISiteRoot
from collective.subscribemember import config
from collective.subscribemember.interfaces import IMemberImporter
# To temporarily fixup the display of the PGP portlet
from Products.PloneGetPaid.interfaces import IBuyableMarker
from zope.component import getUtility

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
            importer = getUtility(IMemberImporter)
            reader = csv.reader(file)
            # Turn off new member email notifications
            site = getUtility(ISiteRoot)
            if site.validate_email:
                site.validate_email = False
            for i, line in enumerate(reader):
                # ignore the first line as its just headers
                if i <> 0:
                    # Create a savepoint for every
                    # 20th item
                    if i % 20 == 0:
                        transaction.savepoint()
                    self.imported = importer.import_member(line, self.imported)
            log = "Imported %s members" % str(self.imported) 
            logging.info(log)
            site.validate_email = True
            file.close()
    
    def getFile(self):
        """
        Get the first CSV file and return it
        """
        proptool = getToolByName(self.context, 'portal_properties')
        subscribemember_props = proptool.subscribemember_properties
        importdir = getattr(subscribemember_props, 'member_import_directory', None)
        if importdir:
            filenames = sorted(os.listdir(importdir))
            for filename in filenames:
                if re.search('.csv$', filename):
                    file = open(os.path.join(importdir, filename), 'r')
                    return file
        else:
            logging.error(u"An import directory hasn't been defined. Please specify one in portal_properties/subscribemember_properties.")