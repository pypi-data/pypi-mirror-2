# -*- coding: utf-8 -*-
from zope.component import getUtility
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFPlone.interfaces import IPloneSiteRoot
from Products.CMFCore.utils import getToolByName
from plone.app.layout.viewlets.common import ViewletBase

class VarnishPurgeViewlet(ViewletBase):
    """
    Viewlet displaing link to purge
    actual url from varnish cache
    """
    
    render = ViewPageTemplateFile('varnish_purge.pt')
    homepage_views = [u'homepage_view', u'folder_tabular_view']
    
    def isPloneSite(self):
        """
        Returns boolean information if
        actual context is a Plone Site instance
        """
        # TODO: change this condition to be more universal
        if self.context.__class__.__name__ == 'PloneSite':
            return True
        return False
    
    def isHomePage(self):
        """
        Returns boolean information if
        actual context is a home page
        """
        portal = getUtility(IPloneSiteRoot)
        home_page_path = portal.portal_properties.site_properties.getProperty('home_page_path', '')
        if '/'.join(self.context.getPhysicalPath()) == home_page_path:
            return True
        if  self.isPloneSite() and self.view.__name__ in self.homepage_views:
            return True
        return False
    
    def showPurgeViewlet(self):
        """
        Returns boolean information if
        purge viewlet should be displayed 
        """
        mtool = getToolByName(self.context, "portal_membership")
        if mtool.checkPermission("Modify portal content", self.context) and not self.isPloneSite() or self.isControlPanel():
            return True
        # TODO: change this condition to be more universal
        if mtool.checkPermission("Modify portal content", self.context) and self.view.__name__ in self.homepage_views:
            return True
        return False
    
    def isControlPanel(self):
        """
        Returns boolean information if
        actual view is a SiteControlPanel view
        """
        if self.view.__class__.__name__ in ['SiteControlPanel', 'VarnishPurgerSettingsForm']:
            return True
        return False
