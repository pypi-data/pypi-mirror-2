import logging
from zope.component import getUtility
from collective.subscribemember import config
import DateTime
from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.interfaces import ISiteRoot
from Products.AdvancedQuery import Eq, Le, Between

logging.getLogger(config.PROJECTNAME)

class MemberExpiry(BrowserView):
    """
    Check expiry date on members and
    process accordingly.
    """
    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.catalog = getToolByName(context, 'portal_catalog')
    
    def __call__(self):
        self.catalog = getToolByName(self.context, 'portal_catalog')
        workflow = getToolByName(self.context, 'portal_workflow')
        today = DateTime.DateTime().latestTime()
        expiredmembers = self.catalog.evalAdvancedQuery(Eq('portal_type', 'Member') & \
                             (Eq('review_state', 'public') | Eq('review_state', 'private')) & \
                             Le('memberExpiryDate', today))
        if len(expiredmembers) != 0:
            for expiredmember in expiredmembers:
                memobj = expiredmember.getObject()
                workflow.doActionFor(memobj, 'disable')
                subject = "Your %s membership has been disabled" % self.context.title
                mto = memobj.getEmail()
                message = u"""%s,
                
Your membership has expired and your access to the %s site has been disabled.

In order to renew your membership online, you must click on the
following link to gain access to the site:  %s.

Kind regards,
%s
                """ % (expiredmember.fullname.decode('utf-8'),self.context.title,self.context.portal_url.getPortalObject().absolute_url()+'/@@renew_expired_view?member='+memobj.getId(),self.context.email_from_name)
                self.sendEmail(mto, subject, message)
                log = u"Disabled: %s" % expiredmember.fullname.decode('utf-8')
                if config.TESTING:
                    print log
                else:
                    logging.info(log)
        self.sendReminder()

                    
    def sendReminder(self):
        """
        Send reminder email to members
        whose subscription will
        expire soon.
        """
        today = DateTime.DateTime().latestTime()
        reminderdate = today + config.REMINDER_EMAIL_TRIGGER
        expiresoonmembers = self.catalog.evalAdvancedQuery(Eq('portal_type', 'Member') & \
                             (Eq('review_state', 'public') | Eq('review_state', 'private')) & \
                             Le('memberExpiryDate', reminderdate))
        if len(expiresoonmembers) != 0:
            for expiresoonmember in expiresoonmembers:
                memobj = expiresoonmember.getObject()
                if not getattr(memobj, 'remindersent', None) and expiresoonmember.memberExpiryDate:
                    subject = "Your membership will expire soon"
                    mto = memobj.getEmail()
                    log = u"Processing %s..." % expiresoonmember.fullname.decode('utf-8')
                    logging.info(log)
                    message = u"""%s,

Your membership to the %s site will expire on %s.

To renew your membership, please go to %s

Kind regards,
%s
                    """ % (expiresoonmember.fullname.decode('utf-8'), self.context.title, expiresoonmember.memberExpiryDate.Date(), self.context.absolute_url()+'/portal_memberdata/'+memobj.getId(), self.context.email_from_name)
                    self.sendEmail(mto, subject, message)
                    setattr(memobj, 'remindersent', True)
                    log = u"Sent renewal reminder email to: %s" % expiresoonmember.fullname.decode('utf-8')
                    if config.TESTING:
                        print log
                    else:
                        logging.info(log)

    def sendEmail(self, mto, subject, message):
        mhost = getToolByName(self.context, 'MailHost')
        mfrom = self.context.email_from_address
        mhost.send(message.encode('iso-8859-1', 'ignore'), mto=mto, mfrom=mfrom, subject=subject)        
