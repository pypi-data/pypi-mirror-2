from Products.contentmigration.walker import CustomQueryWalker
from Products.contentmigration.archetypes import ATFolderMigrator,ATItemMigrator
from collective.contentmigrationui.interfaces import IContentMigrator
from zope.interface import implements
from collective.contentmigrationui.utils import BASE_AT_PROPERTIES
from Acquisition import aq_parent
from Products.CMFCore.utils import getToolByName

class TaxonomyToFolder(object, ATFolderMigrator,ATItemMigrator):
    """Migrate the old item type to the new item type
    """
    walker = CustomQueryWalker
    src_meta_type = "FolderTaxonomy"
    src_portal_type = "FolderTaxonomy"
    dst_meta_type = "ATFolder"
    dst_portal_type = "Folder"
    description = "Warning : This migration will merge siteAreas field into subject field"
    safeMigration = False

    def __init__(self, *args, **kwargs):
        ATFolderMigrator.__init__(self, *args, **kwargs)
        ATItemMigrator.__init__(self, *args, **kwargs)
        self.fields_map = BASE_AT_PROPERTIES

    # Includo tutte le siteAreas nei subject
    def beforeChange_storeSubojects(self):
        ATFolderMigrator.beforeChange_storeSubojects(self)
        for child in self.subobjs.values():
            listtitle = []
            if getattr(child,'siteAreas',False):
                listuids = child.getSiteAreas()
                portal_catalog = getToolByName(self.old,'portal_catalog')
                for uid in listuids:
                    results = portal_catalog.searchResults(UID=uid)
                    if results:
                        listtitle.append(results[0].Title)
                listtitle.extend(child.subject)
                child.setSubject(set(listtitle))

TaxonomyToFolderMigrator = TaxonomyToFolder