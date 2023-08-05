import logging
from zope.component import getUtility
import zope.event
from zope.schema.interfaces import IVocabularyFactory
from AccessControl.SecurityManagement import getSecurityManager
from AccessControl.SecurityManagement import newSecurityManager
from AccessControl.SecurityManagement import setSecurityManager
from AccessControl.SpecialUsers import system
from DateTime import DateTime
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from Products.membrane.interfaces import IMembraneUserAuth
from Products.statusmessages.interfaces import IStatusMessage
from collective.subscribemember.events import MemberCreatedOrRenewedEvent, ProcessSubscriptionEvent
from collective.subscribemember import config

logging.getLogger(config.PROJECTNAME)

class RenewExpiredView(BrowserView):
    
    template = ViewPageTemplateFile('templates/renew_expired_view.pt')

    def __call__(self):
        if self.request.form.has_key('form.submitted'):
            workflow = getToolByName(self.context, 'portal_workflow')
            member = None
            if self.request.form.get('memberid', None):
                memberid = self.request.form.get('memberid')
                mtool = getToolByName(self.context, 'portal_membership')
                member = mtool.getMemberById(memberid)
                if member:
                    if self.request.form.get('memberpassword', None):
                        memberpassword = self.request.form.get('memberpassword')
                        if IMembraneUserAuth(member).authenticateCredentials({'login': memberid, 'password': memberpassword}):
                            currentstate = workflow.getInfoFor(member, 'review_state')
                            if currentstate == 'disabled':
                                sm = getSecurityManager()
                                try:
                                    newSecurityManager(None, system)
                                    if getattr(member, 'old_state', None) == 'public':
                                        workflow.doActionFor(member, 'enable_public')
                                    else:
                                        workflow.doActionFor(member, 'enable_private')
                                    today = DateTime()
                                    member.Schema()['memberRenewedDate'].set(member, today)
                                    log = u"Renabled: %s" % member.getFullname()
                                    logging.info(log)
                                finally:
                                    setSecurityManager(sm)
                            else:
                                msg = "The membership for %s hasn't expired" % memberid
                                IStatusMessage(self.request).addStatusMessage(msg, type='error')
                                return self.template()                                    
                        else:
                            IStatusMessage(self.request).addStatusMessage("You have entered an incorrect username and/or password", type='error')
                            return self.template()
                    else:
                        IStatusMessage(self.request).addStatusMessage("You must enter a password", type='info')
                        return self.template()
                else:
                    IStatusMessage(self.request).addStatusMessage("No user exists with that userid", type='error')
                    return self.template()
            else:
                IStatusMessage(self.request).addStatusMessage("You must enter a user name", type='info')
                return self.template()
            if self.get_selected_membertype() != member.Schema()['memberType'].get(member):
                member.Schema()['memberType'].set(member, self.get_selected_membertype())
            zope.event.notify(MemberCreatedOrRenewedEvent(member))
            zope.event.notify(ProcessSubscriptionEvent(member))
        else:
            return self.template()
    
    def get_selected_membertype(self):
        return self.request.get('member_types', None)
    
    def getMemberId(self):
        if self.request.get('member', None):
            return self.request.get('member')
        else:
            return self.request.form.get('memberid', '')

    def member_types(self):
        member_types_factory = getUtility(IVocabularyFactory, 'collective.subscribemember.vocabulary.MemberTypes')
        return member_types_factory(None)