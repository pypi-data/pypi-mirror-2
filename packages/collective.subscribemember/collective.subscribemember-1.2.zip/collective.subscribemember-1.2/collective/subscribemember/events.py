import zope.component.interfaces
import zope.interface
from interfaces import IMemberCreatedOrRenewedEvent, IProcessSubscriptionEvent

class MemberCreatedOrRenewedEvent(zope.component.interfaces.ObjectEvent):
    zope.interface.implements(IMemberCreatedOrRenewedEvent)
    
    
class ProcessSubscriptionEvent(zope.component.interfaces.ObjectEvent):
    zope.interface.implements(IProcessSubscriptionEvent)