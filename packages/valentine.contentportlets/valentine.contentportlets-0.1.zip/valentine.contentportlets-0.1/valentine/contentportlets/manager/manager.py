from zope.interface import Interface
from zope.component import adapts
from zope.publisher.interfaces.browser import IBrowserView
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.portlets.manager import ColumnPortletManagerRenderer
from valentine.contentportlets.interfaces import IContentPortlets, IContentPortletManager

class ContentPortletManagerRenderer(ColumnPortletManagerRenderer):
    """A renderer for the column portlets
    """
    adapts(Interface, IDefaultBrowserLayer, IBrowserView, IContentPortletManager)
    template = ViewPageTemplateFile('portlets.pt')
