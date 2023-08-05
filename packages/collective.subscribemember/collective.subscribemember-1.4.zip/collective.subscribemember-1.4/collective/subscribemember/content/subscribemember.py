"""Definition of the Subscribemember content type
"""

from archetypes.schemaextender.field import ExtensionField
from archetypes.schemaextender.interfaces import ISchemaExtender, ISchemaModifier
from zope.component import adapts, getUtility
from zope.interface import implements
from Products.Archetypes import atapi
from Products.remember.interfaces import IReMember
from collective.subscribemember.config import PROJECTNAME, EDIT_EXPIRYDATE_PERMISSION
from collective.subscribemember.interfaces import IMemberTypesGetter

class MemberType(ExtensionField, atapi.StringField):
    """Membership Level."""
    def set(self, instance, value, **kwargs):
        if value != '':
            MEMBERTYPES = getUtility(IMemberTypesGetter).return_member_types()
            price = MEMBERTYPES[value][1]
            instance.Schema()['product_code'].set(instance, value)
            instance.Schema()['price'].set(instance, float(price))
        return value
    
    def get(self, instance, **kwargs):
        return instance.Schema()['product_code'].get(instance)

    def getRaw(self, instance, **kwargs):
        return self.get(instance, **kwargs)


class MemberExpiryDate(ExtensionField, atapi.DateTimeField):
    """Member Expiry Date."""


class MemberJoinedDate(ExtensionField, atapi.DateTimeField):
    """Member Joined Date."""

    
class MemberRenewedDate(ExtensionField, atapi.DateTimeField):
    """Member Renewed Date."""


class Price(ExtensionField, atapi.StringField):
    """Price"""
    
    
class ProduceCode(ExtensionField, atapi.StringField):
    """Product Code"""
    
    
class MadePayableBy(ExtensionField, atapi.StringField):
    """Made Payable By"""
    def getDefault(self, instance):
        return PROJECTNAME


class PhoneNumber(ExtensionField, atapi.IntegerField):
    """Phone Number"""


class BillFirstLine(ExtensionField, atapi.StringField):
    """Address 1"""
    

class BillSecondLine(ExtensionField, atapi.StringField):
    """Address 2"""


class BillCity(ExtensionField, atapi.StringField):
    """City"""    


class BillState(ExtensionField, atapi.StringField):
    """State"""


class BillCountry(ExtensionField, atapi.StringField):
    """Country"""


class BillPostalCode(ExtensionField, atapi.StringField):
    """Postal Code"""
    
            
class RememberExtender(object):
    adapts(IReMember)
    implements(ISchemaExtender)

    fields = [
        BillFirstLine(
            'billFirstLine',
            widget = atapi.StringWidget(label=u"Address 1"),
            required        = True,
            regfield        = True,
            searchable      = True,
            ),
        BillSecondLine(
            'billSecondLine',
            widget = atapi.StringWidget(label=u"Address 2"),
            required        = False,
            regfield        = True,
            searchable      = True,
            ),
        BillCity(
            'billCity',
            widget = atapi.StringWidget(label=u"City"),
            required        = True,
            regfield        = True,
            searchable      = True,
            ),
        BillState(
            'billState',
            widget = atapi.SelectionWidget(label=u"State"),
            required        = True,
            regfield        = True,
            searchable      = True,
            vocabulary_factory = 'getpaid.states'
            ),
        BillCountry(
            'billCountry',
            widget = atapi.SelectionWidget(label=u"Country"),
            required        = True,
            regfield        = True,
            searchable      = True,
            vocabulary_factory = 'getpaid.countries'
            ),
        BillPostalCode(
            'billPostalCode',
            widget = atapi.StringWidget(label=u"Zip/Postal Code"),
            required        = True,
            regfield        = True,
            searchable      = True,
            ),
        PhoneNumber(
            'phoneNumber',
            widget = atapi.IntegerWidget(label=u"Phone Number",
                                         description=u"Only digits allowed - e.g. 3334445555 and not 333-444-5555 ",
                                         size=12),
            required        = True,
            regfield        = True,
            searchable      = True,
            ),
        MemberType(
            "memberType",
            widget = atapi.SelectionWidget(label="Membership Level"),
            required        = True,
            regfield        = True,
            searchable      = True,
            vocabulary_factory = 'collective.subscribemember.vocabulary.MemberTypes',
            ),
        MemberExpiryDate(
            "memberExpiryDate",
            widget = atapi.CalendarWidget(label="Member Expiry Date"),
            write_permission = EDIT_EXPIRYDATE_PERMISSION,
            ),
        MemberExpiryDate(
            "memberJoinedDate",
            widget = atapi.CalendarWidget(label="Member Joined Date",
                                          visible = {'edit':'invisible', 'view': 'invisible'}),
            ),
        MemberExpiryDate(
            "memberRenewedDate",
            widget = atapi.CalendarWidget(label="Member Renewed Date",
                                          visible = {'edit':'invisible', 'view': 'invisible'}),
            ),
        Price(
            "price",
            widget = atapi.StringWidget(label="Price",
                                        visible = {'edit':'invisible', 'view': 'invisible'}),
            ),
        ProduceCode(
            "product_code",
            widget = atapi.StringWidget(label="Product Code",
                                        visible = {'edit':'invisible', 'view': 'invisible'}),
            ),
        MadePayableBy(
            "made_payable_by",
            widget = atapi.StringWidget(label="Made Payable By",
                                        visible = {'edit':'invisible', 'view': 'invisible'}),
            )
        ]

    def __init__(self, context):
        self.context = context

    def getFields(self):
        return self.fields
   

class RememberModifier(object):
    implements(ISchemaModifier)
    adapts(IReMember)
    
    def __init__(self, context):
        self.context = context
    
    def fiddle(self, schema):
        schema['fullname'].required = True
