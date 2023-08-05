# -*- coding: utf-8 -*-

from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName

from collective.disqus.browser.configlet import IDisqusSettings


class Summary(BrowserView):
    """ Summary listing (for Folder, Topic) with showing number of comments per
        item in the list.
    """

    def render_js_settings(self):
        """
        js for getting number of comments for each item in summary listing.
        """

        portal_url = getToolByName(self.context, 'portal_url')
        portal = portal_url.getPortalObject()
        self.settings = IDisqusSettings(portal)

        return ''''
            var disqus_shortname = '$(forum_id)s';
            (function () {
              var s = document.createElement('script'); s.async = true;
              s.src = 'http://disqus.com/forums/$(forum_id)s/count.js';
              (document.getElementsByTagName('HEAD')[0] || document
                       .getElementsByTagName('BODY')[0]).appendChild(s);
            }());''' % dict(forum_id = self.settings.forum_id)
