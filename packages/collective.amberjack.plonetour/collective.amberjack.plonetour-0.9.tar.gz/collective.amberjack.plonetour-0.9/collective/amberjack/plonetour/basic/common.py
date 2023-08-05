from Products.CMFCore.utils import getToolByName
from zope.i18nmessageid import MessageFactory

_ = MessageFactory('collective.amberjack.plonetour')


def isFolderCreated(context, request):
    portal = getToolByName(context, 'portal_url').getPortalObject()
    myfolder = getattr(portal, 'myfolder', None)
    if myfolder is None:
        return _(u"The [MyFolder] folder doesn't exist yet. Please close this tour and start the first tour.")

def isNotFolderCreated(context, request):
    if isFolderCreated(context, request) is None:
        return _(u"Please remove the [MyFolder] folder to start the tour.")
