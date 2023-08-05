from zope import schema
from zope.interface import Interface
import zope.component.interfaces

from plone.theme.interfaces import IDefaultPloneLayer

from collective.subscribemember import MessageFactory as _

class ISubscribemember(Interface):
    """A subscriber"""


class ISubscribememberLayer(IDefaultPloneLayer):
    """ default Subscribemember layer """

    
class IMemberCreatedOrRenewedEvent(zope.component.interfaces.IObjectEvent):
    """Event raised when a member is created or renewed"""


class IProcessSubscriptionEvent(zope.component.interfaces.IObjectEvent):
    """Event raised when a subscription is being processed"""
    

class IMemberExporter(Interface):
    """For the member exporter utility"""
    
    
class IMemberTypesGetter(Interface):
    """Interface for the utility that gets the membertypes"""