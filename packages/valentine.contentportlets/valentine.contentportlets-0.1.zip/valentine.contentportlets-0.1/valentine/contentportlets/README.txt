valentine.contentportlets
=========================

First we check if manager is properly installed:

  >>> from zope.component import getUtility, getMultiAdapter
  >>> from plone.portlets.interfaces import IPortletManager
  >>> manager = getUtility(IPortletManager, name=u'ContentPortlets')
  >>> type(manager)
  <class 'plone.portlets.manager.PortletManager'>
  
Then we add a container object and example portlet:
  >>> self.setRoles(['Manager'])
  >>> doc = self.portal[self.portal.invokeFactory('Document', id='doc')]
  >>> from plone.portlet.static.static import Assignment as StaticPortlet
  >>> staticPortlet = StaticPortlet(header = 'MyHeader', text='portlet text', omit_border=True)
  >>> from plone.portlets.interfaces import IPortletAssignmentMapping
  >>> assignable = getMultiAdapter((doc, manager), IPortletAssignmentMapping).__of__(doc)
  >>> assignable['tempstatic'] = staticPortlet

Registered view provides functionality to manage portlets:
  >>> contentPortlets = doc.restrictedTraverse('@@contentportlets')
  >>> contentPortlets.getPortlets()
  [u'<div class="portletStaticText portlet-static-myheader">portlet text</div>\n\n']
  >>> contentPortlets.numberOfPortlets()
  1
  >>> contentPortlets.removePortlet(0)
  >>> contentPortlets.numberOfPortlets()
  0
