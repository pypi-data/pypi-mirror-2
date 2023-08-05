from config import PROJECTNAME
from Products.PloneGetPaid.content import BuyableContentAdapter

class BuyableContentAdapter(BuyableContentAdapter):

    def __init__(self, context):
        self.context = context
        self.price = context.getPrice()
        self.product_code = str(context.getMemberType())
        self.made_payable_by = PROJECTNAME