from zope.interface import Interface
from plone.portlets.interfaces import IPortletManager
from plone.app.portlets.interfaces import IColumn

class IContentPortlets(Interface):
    """
    Marker interface for portlet manager
    """

class IContentPortletManager(IPortletManager, IColumn):
    """
    """

