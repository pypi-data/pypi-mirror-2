from urllib import quote as url_quote

from zope.component import getMultiAdapter

from Acquisition import aq_inner, aq_parent
from AccessControl import getSecurityManager
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from Products.CMFDefault.DiscussionTool import DiscussionNotAllowed

from plone.app.layout.viewlets.common import ViewletBase


class CommentsViewlet(ViewletBase):
    render = ViewPageTemplateFile('comments.pt')

    def update(self):
        context = aq_inner(self.context)
        self.portal_state = getMultiAdapter((context, self.request),
                                            name=u'plone_portal_state')
        self.portal_url = self.portal_state.portal_url()
        self.portal_discussion = getToolByName(context, 'portal_discussion', None)
        self.portal_membership = getToolByName(context, 'portal_membership', None)

    def can_reply(self):
        return getSecurityManager().checkPermission('Reply to item', aq_inner(self.context))

    def is_discussion_allowed(self):
        if self.portal_discussion is None:
            return False
        else:
            return self.portal_discussion.isDiscussionAllowedFor(aq_inner(self.context))

    def get_replies(self):
        replies = []

        context = aq_inner(self.context)
        container = aq_parent(context)
        pd = self.portal_discussion

        def getRs(obj, replies, counter):
            rs = pd.getDiscussionFor(obj).getReplies()
            if len(rs) > 0:
                rs.sort(lambda x, y: cmp(x.modified(), y.modified()))
                for r in rs:
                    replies.append({'depth':counter, 'object':r})
                    getRs(r, replies, counter=counter + 1)

        try:
            getRs(context, replies, 0)
        except DiscussionNotAllowed:
            # We tried to get discussions for an object that has not only
            # discussions turned off but also no discussion container.
            return []
        return replies

    def is_anonymous(self):
        return self.portal_state.anonymous()

    def login_action(self):
        return '%s/login_form?came_from=%s' % (self.portal_url, url_quote(self.request.get('URL', '')),)

    def can_manage(self):
        return getSecurityManager().checkPermission('Manage portal', aq_inner(self.context))

    def member_info(self, creator):
        if self.portal_membership is None:
            return None
        else:
            return self.portal_membership.getMemberInfo(creator)

    def format_time(self, time):
        context = aq_inner(self.context)
        util = getToolByName(context, 'translation_service')
        return util.ulocalized_time(time, 1, context, domain='plonelocales')
