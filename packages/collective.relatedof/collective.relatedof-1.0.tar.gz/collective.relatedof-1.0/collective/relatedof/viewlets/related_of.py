
from zope.interface import Interface
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets.common import ViewletBase

class IRelatedOf(Interface):
    """File acquisito tramite scansione"""

class RelatedOfViewlet(ViewletBase):    
    
    def getInfoFor(self,item):
        wtool = getToolByName(self,'portal_workflow')
        return wtool.getInfoFor(item.getObject(), 'review_state', '')
    

    def computeRelatedItems(self):
        pc = getToolByName(self,"portal_catalog")
        return pc(getRawRelatedItems=self.context.UID())
        