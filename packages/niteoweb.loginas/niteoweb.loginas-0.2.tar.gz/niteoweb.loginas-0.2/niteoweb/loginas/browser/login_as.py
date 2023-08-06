# -*- coding: utf-8 -*-
import re
import os

from zope.component import getMultiAdapter
from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Globals import DevelopmentMode
from niteoweb.loginas import NiteowebLoginasMF as _


class LoginAs(BrowserView):
    """ Form for adding new commercial websites """

    template = ViewPageTemplateFile('login_as.pt')

    def __call__(self):
        self.portal_state = getMultiAdapter((self.context, self.request), name=u'plone_portal_state')
        mtool = getToolByName(self.context, 'portal_membership')

        # Hide the editable-object border
        self.request.set('disable_border', True)

        if not DevelopmentMode:
            self.context.plone_utils.addPortalMessage(_(u'You can login as another user only in Development mode.'), 'info')
        else:
            # Handle clicks
            self.actions()
        
        return self.template()

    def actions(self):
        """Login the user"""
        if 'user' in self.request.keys():
            self.errors = {}
            user = self.request['user']
            if user not in [member['username'] for member in self.members()]:
                self.errors['user'] = user
                return

            if hasattr(self.context.acl_users.session, 'setupSession'):
                # Plone 3
                self.context.acl_users.session.setupSession(user, self.context.REQUEST.RESPONSE)
            else:
                # Plone 4
                self.context.acl_users.session._setupSession(user, self.context.REQUEST.RESPONSE)
                
            self.request.RESPONSE.redirect(self.portal_state.portal_url())

    def members(self):
        """ lists all members on this Plone site """

        membership = getToolByName(self.context, 'portal_membership')
        members = membership.listMembers()
        
        results = []
        
        for member in members:
            results.append({'username': member.id,
                            'fullname': member.getProperty('fullname')})
        
        return results
 
    def is_dev_mode(self):
        return DevelopmentMode
