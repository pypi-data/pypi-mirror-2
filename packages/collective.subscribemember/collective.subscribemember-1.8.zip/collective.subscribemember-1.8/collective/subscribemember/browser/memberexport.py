from StringIO import StringIO
from zope.component import getUtility
from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName
from collective.subscribemember import config
from collective.subscribemember.interfaces import IMemberExporter

class MemberExport(BrowserView):
    """
    Export all members in CSV format.
    """
    
    def __call__(self):
        # generate csv
        if config.TESTING:
            f = open('/tmp/members.csv', 'w')
        else:
            f = StringIO()
        exporter = getUtility(IMemberExporter)()
        csvdata = exporter.process(f)

        # send csv to browser
        RESPONSE = self.request.RESPONSE
        RESPONSE.setHeader("Content-disposition", 'inline; filename="members.csv"')
        RESPONSE.setHeader('Content-Type', 'text/x-csv')
        if not config.TESTING:
            RESPONSE.setHeader("Content-Length", f.len)
            tmp = f.getvalue()
        else:
            tmp = f
        f.close()
        return tmp