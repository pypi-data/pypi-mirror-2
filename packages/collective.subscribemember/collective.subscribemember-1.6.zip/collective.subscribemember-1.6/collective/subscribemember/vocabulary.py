from zope.component import getUtility
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from Products.CMFCore.utils import getToolByName
from collective.subscribemember.interfaces import IMemberTypesGetter

def MemberTypes(context):
    membertypes = getUtility(IMemberTypesGetter).return_member_types()
    membertypeskeys = membertypes.keys()
    membertypeskeys.sort()
    membertypessorted = [(key, membertypes[key]) for key in membertypeskeys]
    return SimpleVocabulary([SimpleTerm(item[0], title=item[1][0]) for item in membertypessorted])