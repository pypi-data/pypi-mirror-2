import sys
from zope.interface import implements
from Acquisition import aq_acquire
from ZODB.POSException import ConflictError
from zope.component import getUtility
from Products.Five import BrowserView
from plone.portlets.interfaces import IPortletManager
from plone.app.portlets.utils import assignment_mapping_from_key
from zope.annotation.interfaces import IAnnotations
from zope.component import getUtility, getMultiAdapter
from plone.app.portlets.browser.interfaces import IManageContextualPortletsView
from plone.app.portlets.browser.manage import ManageContextualPortlets
import logging
logger = logging.getLogger('portlets')

REQUEST_KEY = 'contentportlets_removed_portlets' 

class ManagePortlets(ManageContextualPortlets):
    """
    I need to use adapter which is a child of ManageContextualPortlets to have proper context for inplace portlet editing.
    """
    
    implements(IManageContextualPortletsView)
    

    def set_manageparagraphs_blacklist_status(self, manager, group_status, content_type_status, context_status):
        """
        Customized function to provide consistent content portlet management
        """
        ManageContextualPortlets.set_blacklist_status(self, manager, group_status, content_type_status, context_status)
        baseUrl = str(getMultiAdapter((self.context, self.request), name='absolute_url'))
        if manager=='ContentPortlets':
            self.request.response.redirect(baseUrl + '/@@manage-contentportlets')
        return ''


class ContentPortlets(BrowserView):
    """
    The most of functionality related to content portlets is moved to that view
    """
    def __init__(self, context, request):
        super(ContentPortlets, self).__init__(context, request)
        self.manager = getUtility(IPortletManager, name=u'ContentPortlets')
        self.renderer = self.manager(context, request, self)
        self.portlets = self.renderer.portletsToShow()

    def set_manageparagraphs_blacklist_status(self, manager, group_status, content_type_status, context_status):
        """
        Customized function to provide consistent content portlet management
        """
        self.renderer.set_blacklist_status(self, manager, group_status, content_type_status, context_status)
        baseUrl = str(getMultiAdapter((self.context, self.request), name='absolute_url'))
        self.request.response.redirect(baseUrl + '/@@manage-contentportlets')
        return ''

    def numberOfPortlets(self):
        return len(self.portlets)
    
    def getPortletNames(self):
        """
        I need that function to invalidate removed portlets
        """
        return [p['name'] for p in self.portlets]
    
    def getPortlets(self):
        """
        Get content of all portlets
        """
        return [self.getPortlet(i) for i in range(len(self.portlets))]

    def getPortlet(self, position):
        """
        I can't use renderer's safe_render method as there are some problems with a context
        """
        try:
            return self.portlets[position]['renderer'].render()
        except ConflictError:
            raise
        except Exception:
            logger.exception('Error while rendering %r' % (self.renderer,))
            aq_acquire(self.context, 'error_log').raising(sys.exc_info())
            return self.renderer.error_message()

    def removePortlet(self, position):
        """
        Remove portlet on given position
        """
        portlet = self.portlets[position]
        assignments = assignment_mapping_from_key(self.context, 
                        portlet['manager'], portlet['category'], portlet['key'])
        del assignments[portlet['name']]
        self.portlets = [p for p in self.portlets if p['name']<>portlet['name']]
