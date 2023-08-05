from Products.CMFCore.utils import getToolByName
from collective.subscribemember import config

def setupVarious(context):
    """ Setup miscellaneous non-GS-supported items """
    if context.readDataFile('subscribemember-setup-plugins.txt') is None:
        return
    portal = context.getSite()
        
    # Set AddPortalContent perm on portal_memberdata
    # Copied from:
    # http://dev.plone.org/collective/browser/Products.remember/trunk/Products/remember/security.py
    md = getToolByName(portal, 'portal_memberdata')
   
    app_perms = md.rolesOfPermission(permission='Add portal content')
    reg_roles = []
    for appperm in app_perms:
        if appperm['selected'] == 'SELECTED':
            reg_roles.append(appperm['name'])
    if 'Anonymous' not in reg_roles:
        reg_roles.append('Anonymous')

    md.manage_permission('Add portal content', roles=reg_roles,
                                  acquire=0)
    
    # Only install PloneGetPaid if it hasn't already been installed
    qi = getToolByName(portal, 'portal_quickinstaller')
    if not qi.isProductInstalled('PloneGetPaid'):
        qi.installProduct('PloneGetPaid')