"""Step validators
"""
from Products.CMFCore.utils import getToolByName
from zope.i18nmessageid import MessageFactory

_ = MessageFactory("collective.amberjack.core")

def isAnonymous(context, request):
    """Return None if user is anonymous, else an error message."""
    mtool = getToolByName(context, 'portal_membership')
    if not mtool.isAnonymousUser():
        return _(u"You have to be anonymous to execute this step.")

def isAuthenticated(context,request):
    """Return None if user is authenticated, else an error message."""
    if isAnonymous(context, request) is None:
        return _(u"You have to be logged in to execute this step.")

def isManager(context, request):
    if not request.AUTHENTICATED_USER.has_role('Manager', context):
        return _(u"You have to be Manager to execute this step.")

def isReviewer(context, request):
    if not request.AUTHENTICATED_USER.has_role('Reviewer', context):
        return _(u"You have to be Reviewer to execute this step.")

def isContributor(context, request):
    if not request.AUTHENTICATED_USER.has_role('Contributor', context):
        return _(u"You have to be Contributor to execute this step.")

def isEditor(context, request):
    if not request.AUTHENTICATED_USER.has_role('Editor', context):
        return _(u"You have to be Editor to execute this step.")

def isReader(context, request):
    if not request.AUTHENTICATED_USER.has_role('Editor', context):
        return _(u"You have to be Reader to execute this step.")

