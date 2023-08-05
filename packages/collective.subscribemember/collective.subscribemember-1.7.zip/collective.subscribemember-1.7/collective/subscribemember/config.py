"""Common configuration constants
"""
from Products.CMFCore import permissions as cmfcore_permissions

PROJECTNAME = 'collective.subscribemember'

# Change a member's expiry date
EDIT_EXPIRYDATE_PERMISSION = cmfcore_permissions.ManageUsers

MEMBERTYPES = {
    '1' : ["Student members - $15/Year (No Journal Subscription)", 15, ('Member',), 1, 'STUD-2'],
    '2' : ["Student Members - $30/Year", 30, ('Member',), 1, 'STUD-1'],
    '3' : ["Individual Members - $135/Year", 135, ('Member',), 1, 'IND'],
    '4' : ["Individual Members - $250/2 Years", 250, ('Member',), 2, 'IND'],
    '5' : ["Individual Members - $360/3 Years", 360, ('Member',), 3, 'IND'],
    '6' : ["Associate Members - $30/Year (No Journal Subscription)", 30, ('Member',), 1, 'ASS'],
    '7' : ["Corporate Members - $700/Year", 700, ('Member',), 1, 'CORP'],
    '8' : ["Corporate Members - $1300/2 Years", 1300, ('Member',), 2, 'CORP'],
    '9' : ["Corporate Members - $1800/3 Years", 1800, ('Member',), 3, 'CORP']
    }

MEMBER_IMPORT_DIRECTORY = '/usr/local/zope/isiaq.org/var'
TESTING = False

# Number of days prior to expiry date to send
# reminder email
REMINDER_EMAIL_TRIGGER = 1
