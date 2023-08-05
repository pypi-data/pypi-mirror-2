# -*- coding: utf-8 -*-
from urlparse import urlparse
from zope import interface
from zope.component import getMultiAdapter

from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName

from plone.memoize.instance import memoize

from redturtle.video.interfaces import IVideoEmbedCode

class LinkRedirectView(BrowserView):
    """Simulate what the link_redirect_view.py script does for ATLink"""
    
    def __call__(self, request=None, response=None):
        context = self.context
        ptool = getToolByName(context, 'portal_properties')
        mtool = getToolByName(context, 'portal_membership')

        redirect_links = getattr(ptool.site_properties, 'redirect_links', False)
        can_edit = mtool.checkPermission('Modify portal content', context)

        if redirect_links and not can_edit:
            return context.REQUEST.RESPONSE.redirect(context.getRemoteUrl())
        else:
            # link_view.pt is a template in the plone_content skin layer
            return context.restrictedTraverse('@@smartlink_view')()

