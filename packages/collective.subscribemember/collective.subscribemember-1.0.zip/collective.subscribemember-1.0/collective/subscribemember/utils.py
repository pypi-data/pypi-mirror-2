from zope.component import getUtility
from zope.interface import implements
from collective.subscribemember.interfaces import IMemberTypesGetter
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.interfaces import ISiteRoot

class MemberTypesGetter:
    implements(IMemberTypesGetter)
    
    def return_member_types(self):
        membertypes = {}
        site = getUtility(ISiteRoot)
        propstool = getToolByName(site, 'portal_properties')
        subscribemember_props = propstool.subscribemember_properties
        for i, line in enumerate(getattr(subscribemember_props, 'membertypes', [])):
            membervalues = line.split(';')
            membervalues[1] = int(membervalues[1])
            membervalues[3] = int(membervalues[3])
            membervalues[2] = eval(membervalues[2], {'__builtins__': {}})
            membertypes[str(i+1)] = membervalues
        return membertypes