from Products.contentmigration.walker import CustomQueryWalker
from Products.contentmigration.archetypes import ATItemMigrator
from collective.contentmigrationui.interfaces import IContentMigrator
from zope.interface import implements
from collective.contentmigrationui.utils import BASE_AT_PROPERTIES

class DocumentToStructuredDocument(object, ATItemMigrator):
    """Migrate the old item type to the new item type
    """
    implements(IContentMigrator)

    walker = CustomQueryWalker
    src_meta_type = "ATDocument"
    src_portal_type = "Document"
    dst_meta_type = "Structured Document"
    dst_portal_type = "Structured Document"
    description = "Document to Structured Document"
    safeMigration = True

    def __init__(self, *args, **kwargs):
        ATItemMigrator.__init__(self, *args, **kwargs)
        self.fields_map = BASE_AT_PROPERTIES

DocToStructDocMigrator = DocumentToStructuredDocument