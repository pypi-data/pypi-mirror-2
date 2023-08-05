from collective.contentmigrationui.interfaces import IContentMigrator
from collective.contentmigrationui import ContentMigrationUiMessageFactory as _
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from Products.statusmessages.interfaces import IStatusMessage
from zope.component import queryUtility,getUtilitiesFor

## PER LA SITEMAP
from Acquisition import aq_inner  
from Products.Five import BrowserView
from Products.CMFPlone.browser.interfaces import ISitemapView
from Products.CMFPlone.browser.navtree import NavtreeQueryBuilder
from Products.CMFPlone.browser.navtree import SitemapNavtreeStrategy
from plone.app.layout.navigation.navtree import buildFolderTree,NavtreeStrategyBase

from collective.contentmigrationui.browser.filterednavtreestategy import FilteredStrategyBase

from StringIO import StringIO
from Products.CMFPlone.PloneTool import transaction
from plone.app.linkintegrity.exceptions import LinkIntegrityNotificationException



class ContentmigrationView(BrowserView):
    
    confirmSelection = ViewPageTemplateFile('templates/confirm.pt')
    selectMigration = ViewPageTemplateFile('templates/selectMigration.pt')
    selectChildren = ViewPageTemplateFile('templates/selectChildren.pt')

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.messages=IStatusMessage(self.request)
        self.portal = getToolByName(self.context, 'portal_url').getPortalObject()

    def __call__(self):
        # Hide the editable-object border
        self.request.set('disable_border', True)
        folder_path = '/'.join(self.context.getPhysicalPath())
        postback = True
        form = self.request.form
        # Make sure we had a proper form submit, not just a GET request
        submitted = form.get('form.submitted', False)
        self.paths = form.get('paths', [])
        self.chosen_type = form.get('chosen_type', False)
        self.confirm = form.get('form.confirm', False)
        save_button = form.get('form.button.Save', None) is not None
        cancel_button = form.get('form.button.Cancel', None) is not None
        change_selection_btn = form.get('form.button.Change_selection', None) is not None
        change_migration_btn = form.get('form.button.Change_migration', None) is not None
        # No migration selected. Display migration list
        if not self.chosen_type or change_migration_btn:
            return self.selectMigration()
        # User has selected a migration. Display children select list.
        if self.chosen_type:
            self.migrate = queryUtility(IContentMigrator,name=self.chosen_type)
        if not self.paths:
            return self.selectChildren()
        # User has selected children list. Ask confirm
        if self.chosen_type and self.paths and not save_button:
            self.src_query = {'portal_type' : self.migrate.src_portal_type, 'path' : self.paths, 'sort_on' : 'id'}
            self.dst_query = self.src_query.copy()
            self.dst_query['portal_type'] = self.migrate.dst_portal_type
            self.childrenList = self.portal_catalog(self.src_query)
            if not len(self.childrenList) or change_selection_btn:
                self.paths = []
                self.messages.addStatusMessage(_(u"No items found in selection"),type="error")
                return self.selectChildren()
            else: return self.confirmSelection()
                #self.messages.addStatusMessage(_(u"No items selected"),type="error")
        # User has confirmed the selection. Start conversion.
        if submitted and save_button and not cancel_button:
            try:
                self.startConvert()
                message = len(self.paths)==1 and _(u"Item converted") or _(u"feedback", default=u"${num} contents migrated", mapping={ u"num" : len(self.paths)})
                self.messages.addStatusMessage(message,type="info")
            except LinkIntegrityNotificationException:
                message = _(u"Link integrity check failure.")
                self.messages.addStatusMessage(message,type="error")
        if save_button or cancel_button:
            self.request.response.redirect(self.portal.absolute_url() + '/contentmigration')

    def startConvert(self):
        src_query = {'portal_type' : self.migrate.src_portal_type, 'path' : self.paths, 'sort_on' : 'id'}
        dst_query = src_query.copy()
        dst_query['portal_type'] = self.migrate.dst_portal_type
        out = StringIO()
        walker = self.migrate.walker(self.portal,self.migrate, query=src_query)
        walker.go(out=out)
        #transaction.commit()
        print >> out, walker.getOutput()
        #Refresh catalog indixes
        #self.portal_catalog.reindexIndex(self.portal_catalog.indexes(),None)
        self.portal_catalog.refreshCatalog()
        print >> out, "Migration finished"
        return out.getvalue()
    
    def back_link(self):
        return dict(label=_(u"Up to Site setup"),
                    url=self.context.absolute_url())

    @property
    def portal_catalog(self):
        return getToolByName(self.context, 'portal_catalog')

    def getAllMigrations(self):
        allmigrations = []
        for utility in getUtilitiesFor(IContentMigrator):
            info = self.getMigrationInfo(utility[1])
            if info[0] is not None and info[1] is not None:
                allmigrations.append(utility)
        return sorted(allmigrations,key=lambda migration:migration[1].src_portal_type)

    def getMigrationInfo(self,migrationUtility):
        pt = getToolByName(self.context,'portal_types')
        src_portal_type = getattr(migrationUtility,'src_portal_type',None)
        dst_portal_type = getattr(migrationUtility,'dst_portal_type',None)
        return pt.getTypeInfo(src_portal_type),pt.getTypeInfo(dst_portal_type)

    def createSiteMap(self):
        query = {'query': '/', 'navtree' : 1 }
        strategy = FilteredStrategyBase(self.portal,self.migrate.src_portal_type)
        data = buildFolderTree(self.portal, obj=None, query=query, strategy=strategy)
        return data.get('children',[])
