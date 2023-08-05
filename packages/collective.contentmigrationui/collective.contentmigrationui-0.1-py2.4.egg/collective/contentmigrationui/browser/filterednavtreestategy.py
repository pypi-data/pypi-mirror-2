from plone.app.layout.navigation.navtree import buildFolderTree,NavtreeStrategyBase
from Products.CMFPlone.browser.navtree import DefaultNavtreeStrategy
from zope.interface import implements
from plone.app.layout.navigation.interfaces import INavtreeStrategy
from Products.CMFCore.utils import getToolByName

class FilteredStrategyBase(DefaultNavtreeStrategy):
    """Basic navigation tree strategy that does nothing.
    """

    implements(INavtreeStrategy)

    __allow_access_to_unprotected_subobjects__ = 1
    
    rootPath = None
    showAllParents = True
    
    def __init__(self,context, filterType= None):
        DefaultNavtreeStrategy.__init__(self,context)
        self.filterType = filterType

    def nodeFilter(self, node):
        portalType = getattr(node['item'], 'portal_type', None)
        catalog = getToolByName(self.context, 'portal_catalog')
        results = catalog.searchResults({'portal_type' : self.filterType})
        pathList = [res.getPath() for res in results]
        for path in pathList:
            if node['item'].getPath() in path:
                return True
        return False