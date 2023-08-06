"""The default comment class and factory.
"""
from datetime import datetime

from zope.annotation.interfaces import IAnnotatable

from zope.component.factory import Factory
from zope.component import queryUtility

from zope.i18n import translate
from zope.i18nmessageid import Message
from zope.interface import implements

from Acquisition import aq_parent, Implicit

from string import Template

from AccessControl.Role import RoleManager
from AccessControl.Owned import Owned

from persistent import Persistent

from Products.CMFCore.DynamicType import DynamicType
from Products.CMFCore.utils import getToolByName

from OFS.Traversable import Traversable

from plone.registry.interfaces import IRegistry

from plone.app.discussion import PloneAppDiscussionMessageFactory as _
from plone.app.discussion.interfaces import IComment
from plone.app.discussion.interfaces import IConversation
from plone.app.discussion.interfaces import IDiscussionSettings

try:
    # Plone 4:
    # Mixin CatalogAware and WorkflowAware into the Comment class
    # is necessary for comments to be indexed in Plone4.
    from Products.CMFCore.CMFCatalogAware import CatalogAware
    from Products.CMFCore.CMFCatalogAware import WorkflowAware
    PLONE_4 = True
except:
    # Plone 3:
    # Dummy imports to make Comment class happy
    from OFS.Traversable import Traversable as CatalogAware
    from OFS.Traversable import Traversable as WorkflowAware
    PLONE_4 = False

MAIL_NOTIFICATION_MESSAGE = _(u"mail_notification_message",
    default=u"A comment with the title '${title}' "
             "has been posted here: ${link}")


class Comment(CatalogAware, WorkflowAware, DynamicType, Traversable,
              RoleManager, Owned, Implicit, Persistent):
    """A comment.

    This object attempts to be as lightweight as possible. We implement a
    number of standard methods instead of subclassing, to have total control
    over what goes into the object.
    """

    implements(IComment)

    meta_type = portal_type = 'Discussion Item'
    # This needs to be kept in sync with types/Discussion_Item.xml title
    fti_title = 'Comment'

    __parent__ = None

    comment_id = None # long
    in_reply_to = None # long

    title = u""

    mime_type = "text/plain"
    text = u""

    creator = None
    creation_date = None
    modification_date = None

    author_username = None

    author_name = None
    author_email = None
    
    author_notification = None

    # Note: we want to use zope.component.createObject() to instantiate
    # comments as far as possible. comment_id and __parent__ are set via
    # IConversation.addComment().

    def __init__(self):
        self.creation_date = self.modification_date = datetime.utcnow()

    @property
    def __name__(self):
        return self.comment_id and unicode(self.comment_id) or None

    @property
    def id(self):
        return self.comment_id and str(self.comment_id) or None

    def getId(self):
        """The id of the comment, as a string
        """
        return self.id

    def getText(self):
        '''the text'''
        return self.text

    def Title(self):
        """The title of the comment
        """
        return self.title

    def Creator(self):
        """The name of the person who wrote the comment
        """
        return self.creator

    def Type(self):
        """The Discussion Item content type
        """
        return self.fti_title

    # CMF's event handlers assume any IDynamicType has these :(

    def opaqueItems(self):
        return []

    def opaqueIds(self):
        return []

    def opaqueValues(self):
        return []

CommentFactory = Factory(Comment)

def notify_workflow(obj, event):
    """Tell the workflow tool when a comment is added
    """
    tool = getToolByName(obj, 'portal_workflow', None)
    if tool is not None:
        tool.notifyCreated(obj)

def notify_content_object(obj, event):
    """Tell the content object when a comment is added
    """
    content_obj = aq_parent(aq_parent(obj))
    content_obj.reindexObject(idxs=('total_comments', 
                                    'last_comment_date', 
                                    'commentators',))

def notify_content_object_deleted(obj, event):
    """Remove all comments of a content object when the content object has been
       deleted.
    """
    if IAnnotatable.providedBy(obj):
        conversation = IConversation(obj)
        for comment in conversation.getComments():
            del conversation[comment.id]
            
def notify_user(obj, event):
    """Tell users when a comment has been added.
    
       This method composes and sends emails to all users that have added a 
       comment to this conversation and enabled user notification.
       
       This requires the user_notification setting to be enabled in the 
       discussion control panel. 
    """

    # Check if user notification is enabled
    registry = queryUtility(IRegistry)
    settings = registry.forInterface(IDiscussionSettings)
    if not settings.user_notification_enabled:
        return

    # Get informations that are necessary to send an email
    mail_host = getToolByName(obj, 'MailHost')
    portal_url = getToolByName(obj, 'portal_url')
    portal = portal_url.getPortalObject()
    sender = portal.getProperty('email_from_address')

    # Check if a sender address is available
    if not sender:
        return

    # Compose and send emails to all users that have add a comment to this
    # conversation and enabled author_notification.
    conversation = aq_parent(obj)
    content_object = aq_parent(conversation)
    
    for comment in conversation.getComments():
        if obj != comment and \
        comment.author_notification and comment.author_email:
            subject = translate(_(u"A comment has been posted."),
                context=obj.REQUEST)
            message = translate(Message(MAIL_NOTIFICATION_MESSAGE,
                mapping={'title': obj.title,
                         'link': content_object.absolute_url()}),
                context=obj.REQUEST)
            mail_host.send(message, comment.author_email, sender, subject)
            
def notify_moderator(obj, event):
    """Tell the moderator when a comment needs attention.
    
       This method sends an email to the site admin (mail control panel setting)
       if comment moderation is enabled and a new comment has been added that
       needs to be approved.   
    
       This requires the moderator_notification to be enabled in the discussion 
       control panel and the comment_review_workflow enabled for the comment 
       content type.
    """
    
    # Check if moderator notification is enabled
    registry = queryUtility(IRegistry)
    settings = registry.forInterface(IDiscussionSettings)
    if not settings.moderator_notification_enabled:
        return
    
    # Check if comment review workflow is enabled
    wf = getToolByName(obj, 'portal_workflow')    
    if wf.getChainForPortalType('Discussion Item') != \
           ('comment_review_workflow',):
        return
    
    # Get informations that are necessary to send an email
    mail_host = getToolByName(obj, 'MailHost')
    portal_url = getToolByName(obj, 'portal_url')
    portal = portal_url.getPortalObject()
    sender = portal.getProperty('email_from_address')
    mto = portal.getProperty('email_from_address')
    
    # Check if a sender address is available
    if not sender:
        return

    conversation = aq_parent(obj)
    content_object = aq_parent(conversation)

    # Compose email        
    #comment = conversation.getComments().next()
    subject = translate(_(u"A comment has been posted."), context=obj.REQUEST)
    message = translate(Message(MAIL_NOTIFICATION_MESSAGE,
        mapping={'title': obj.title,
                 'link': content_object.absolute_url()}),
        context=obj.REQUEST)

    # Send email
    if PLONE_4:
        mail_host.send(message, mto, sender, subject, charset='utf-8')
    else:
        mail_host.secureSend(message, mto, sender, subject=subject, charset='utf-8')
