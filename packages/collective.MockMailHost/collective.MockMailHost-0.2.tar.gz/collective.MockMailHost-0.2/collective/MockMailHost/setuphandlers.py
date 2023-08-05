import transaction
from time import time
from random import betavariate
from Products.CMFCore.utils import getToolByName

def setupVarious(context):
    site=context.getSite()
    replace_mailhost(site)

def replace_mailhost(self):
    portal = getToolByName(self, 'portal_url').getPortalObject()
    portal._delObject('MailHost')
    portal._setObject('MailHost', portal.MockMailHost)
