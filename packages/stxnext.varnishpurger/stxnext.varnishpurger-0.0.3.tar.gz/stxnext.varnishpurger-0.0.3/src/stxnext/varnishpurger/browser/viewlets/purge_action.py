# -*- coding: utf-8 -*-
import httplib
from zope.component import getUtility
from AccessControl import Unauthorized
from Products.CMFCore.utils import getToolByName
from Products.statusmessages.interfaces import IStatusMessage
from Products.Five import BrowserView
from Products.CMFPlone.interfaces import IPloneSiteRoot

from stxnext.varnishpurger import VPMessageFactory as _

class PurgeActionView(BrowserView):
    
    def PurgeAction(self):
        """
        Purging actual url by sending prepared request.
        The example request: 
        PURGE /VirtualHostBase/http/plone.radek.com:80/Plone/VirtualHostRoot/events HTTP/1.1
        Host: bolt:6081
        """
        mtool = getToolByName(self, 'portal_membership')
        if not mtool.checkPermission("Modify portal content", self.context):
            raise Unauthorized
        
        portal = getUtility(IPloneSiteRoot)
        
        varnish_host = portal.portal_properties.site_properties.getProperty('varnish_host', '')
        varnish_host = varnish_host.split(':')
        host = varnish_host[0]
        port = varnish_host[1]
        
        purging_sites = portal.portal_properties.site_properties.getProperty('purging_sites', '')
        
        page_path = self.context.getPhysicalPath()
        
        # if we are trying to purge home page (when other object is set as default view)
        if self.context.REQUEST.get('homepage', ''):
            page_path = ('', portal.id)

        list_path = list(page_path)
        list_path.insert(2, 'VirtualHostRoot')
        if len(list_path) < 4:
            list_path.append('')
        
        #TODO: Handle exceptions of connection problem
        for site in purging_sites.split('\n'):
            connection = httplib.HTTPConnection(host, port)
            connection.putrequest('PURGE', '/VirtualHostBase/http/' + site + '/'.join(list_path) + '$ HTTP/1.1')
            connection.putheader('Host', host + ':' + port)
            connection.endheaders()
            connection.send('')
            response = connection.getresponse()
        
        messages = IStatusMessage(self.request)
        messages.addStatusMessage(_("Cache of the page has been purged"), type="info")
        return self.request.RESPONSE.redirect(self.context.absolute_url())
            
    def PurgeEverythingAction(self):
        """
        Purging the whole domain by sending prepared request.
        """
        mtool = getToolByName(self, 'portal_membership')
        if not mtool.checkPermission("Manage portal", self.context):
            raise Unauthorized
        
        portal = getUtility(IPloneSiteRoot)
        
        varnish_host = portal.portal_properties.site_properties.getProperty('varnish_host', '')
        varnish_host = varnish_host.split(':')
        host = varnish_host[0]
        port = varnish_host[1]
        
        purging_sites = portal.portal_properties.site_properties.getProperty('purging_sites', '')
        
        for site in purging_sites.split('\n'):
        #TODO: Handle exceptions of connection problem
            connection = httplib.HTTPConnection(host, port)
            connection.putrequest('PURGE', '/VirtualHostBase/http/' + site + ' HTTP/1.1')
            connection.putheader('Host', host + ':' + port)
            connection.endheaders()
            connection.send('')
            response = connection.getresponse()
        
        messages = IStatusMessage(self.request)
        messages.addStatusMessage(_("Cache of the portal have been purged"), type="info")
        return self.request.RESPONSE.redirect(self.context.absolute_url())
