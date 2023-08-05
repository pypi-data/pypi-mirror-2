import logging
from AccessControl import getSecurityManager
from cPickle import loads, dumps
from zope.interface import noLongerProvides
from zope.component import getUtility, getMultiAdapter
import zope.event
from DateTime import DateTime
from getpaid.core.interfaces import IShoppingCartUtility, IOrderManager, IBuyableContent, ILineItemFactory, workflow_states
from getpaid.core.order import Order
from collective.subscribemember.events import MemberCreatedOrRenewedEvent, ProcessSubscriptionEvent
from collective.subscribemember.interfaces import IMemberTypesGetter
from Products.Five.utilities.marker import mark
from Products.PloneGetPaid.interfaces import IBuyableMarker, IGetPaidManagementOptions
from Products.membrane.interfaces import IMembraneUser
from Products.remember.interfaces import IReMember
from config import PROJECTNAME

logging.getLogger(PROJECTNAME)
       
def makeBuyable(object, event):
    """Adapt the remember objects to the PGP Buyable interface
    """
    # Work around an error related to using
    # the PayPal sandbox
    if not IBuyableMarker.providedBy(object):
        mark(object, IBuyableMarker)

def makeBuyableContent(object, event):
    """Adapt the remember objects to the PGP Buyable
       Content interface
    """
    mark(object, IBuyableContent)
    zope.event.notify(MemberCreatedOrRenewedEvent(object))

def buyMembership(object, event):
    """
    Redirect new or renewing member to checkout wizard
    for payment.
    This subscriber assumes that the object is an
    IReMember.
    """
    # If the member was imported then
    # we don't process a payment
    if getattr(object, 'importedmember', None):
        delattr(object, 'importedmember')
        # Also remove the PGP interfaces
        noLongerProvides(object, IBuyableMarker)
        noLongerProvides(object, IBuyableContent)
        return

    MEMBERTYPES = getUtility(IMemberTypesGetter).return_member_types()
    # Ensure we save the selected member type
    # to the member object if it was changed
    memberType = object.Schema()['memberType'].get(object)
    if object.REQUEST.get('member_types', None):
        if memberType != object.REQUEST['member_types']:
            object.Schema()['memberType'].set(object, object.REQUEST['member_types'])
    site = object.portal_url.getPortalObject()

    # If we're Anonymous -> login
    user = getSecurityManager().getUser()
    if 'Anonymous' in user.getRoles():
        site = object.portal_url.getPortalObject()
        object.acl_users.session.setupSession(object.getId(), object.REQUEST.response)

    manage_options = IGetPaidManagementOptions(site)
    cart_util = getUtility(IShoppingCartUtility)
    cart = cart_util.get(object, create=True)
    itemfactory = getMultiAdapter((cart, object), ILineItemFactory)
    if itemfactory:
        item = itemfactory.create()
        # Override the item name as
        # its currently the members name
        item.name = MEMBERTYPES[memberType][0]
        cart.__delitem__(item.item_id)
        cart[item.item_id] = item
        order_manager = getUtility(IOrderManager)
        order = Order()
        order.processor_id = manage_options.payment_processor
        order.order_id = order_manager.newOrderId()
        order.user_id = object.getId()
        order.shopping_cart = loads(dumps(cart))
        order.finance_workflow.fireTransition('create')
        sdm = object.session_data_manager
        session = sdm.getSessionData(create=True)
        name = object.getFullname()
        session.set('form.bill_first_line', object.Schema()['billFirstLine'].get(object))
        session.set('form.bill_second_line', object.Schema()['billSecondLine'].get(object))
        session.set('order_id', order.order_id)
        session.set('form.bill_city', object.Schema()['billCity'].get(object))
        session.set('form.bill_state', object.Schema()['billState'].get(object))
        session.set('form.bill_country', object.Schema()['billCountry'].get(object))
        session.set('form.name', name)
        session.set('form.phone_number', object.Schema()['phoneNumber'].get(object))
        session.set('form.email', object.getEmail())
        session.set('form.bill_postal_code', object.Schema()['billPostalCode'].get(object))
        session.set('form.bill_name', name)
        url = object.absolute_url()+'/subscribemember_pay'
        object.REQUEST.response.redirect(url)


def assignPermissions(order, event): 
    """
    Assign relevant permissions to paid up members
    """
    if event.destination != workflow_states.order.finance.CHARGED:
        return
    MEMBERTYPES = getUtility(IMemberTypesGetter).return_member_types()
    for cart_item in order.shopping_cart.values():
        buyable_object = cart_item.resolve()
        if IReMember.providedBy(buyable_object):
            # Remove the IBuyable interface as we don't want the getpaid
            # portlet and tab showing anymore
            noLongerProvides(buyable_object, IBuyableMarker)
            # Give the member the appropriate role
            # based on the membership type they chose
            memberType = buyable_object.Schema()['memberType'].get(buyable_object)
            subscribememberroles = MEMBERTYPES[memberType][2]
            roles = list(buyable_object.getRoles())
            for role in subscribememberroles:
                if not role in buyable_object.getRoles():
                    roles.append(role)
            buyable_object.setRoles(roles)
            # Also set the joined and expiry dates on the member
            today = DateTime()
            buyable_object.Schema()['memberJoinedDate'].set(buyable_object, today)
            years = MEMBERTYPES[memberType][3]
            expirydate = today + (years*365)          
            buyable_object.Schema()['memberExpiryDate'].set(buyable_object, expirydate)
            buyable_object.reindexObject()
            # Reset the expiry reminder attribute
            if getattr(buyable_object, 'remindersent', None):
                setattr(buyable_object, 'remindersent', False)
    
def sendMemberCreatedEvent(object, event):
    zope.event.notify(MemberCreatedOrRenewedEvent(object))
    
def sendProcessSubscriptionEvent(event):
    if IMembraneUser.providedBy(event.object):
        subscribemember = event.object._getMembraneObject()
        zope.event.notify(ProcessSubscriptionEvent(subscribemember))

def renewMembership(object, event):
    request = object.REQUEST
    if request.get('form.button.renew', None):
        zope.event.notify(MemberCreatedOrRenewedEvent(object))
        zope.event.notify(ProcessSubscriptionEvent(object))