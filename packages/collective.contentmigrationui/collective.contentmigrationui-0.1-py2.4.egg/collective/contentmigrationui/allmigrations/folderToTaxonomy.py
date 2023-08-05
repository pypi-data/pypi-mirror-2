from Products.contentmigration.walker import CustomQueryWalker
from Products.contentmigration.archetypes import ATFolderMigrator,ATItemMigrator
from collective.contentmigrationui.interfaces import IContentMigrator
from zope.interface import implements
from collective.contentmigrationui.utils import BASE_AT_PROPERTIES

class FolderToTaxonomy(object, ATFolderMigrator, ATItemMigrator):
    """Migrate the old item type to the new item type
    """
    implements(IContentMigrator)

    walker = CustomQueryWalker
    src_meta_type = "ATFolder"
    src_portal_type = "Folder"
    dst_meta_type = "FolderTaxonomy"
    dst_portal_type = "FolderTaxonomy"
    description = "Folder to Folder Taxonomy"
    safeMigration = True

    def __init__(self, *args, **kwargs):
        ATFolderMigrator.__init__(self, *args, **kwargs)
        ATItemMigrator.__init__(self, *args, **kwargs)
        self.fields_map = BASE_AT_PROPERTIES

FolderToTaxonomyMigrator = FolderToTaxonomy