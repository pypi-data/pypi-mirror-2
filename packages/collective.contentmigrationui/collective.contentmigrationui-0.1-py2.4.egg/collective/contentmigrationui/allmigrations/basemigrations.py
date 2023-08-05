from Products.contentmigration.walker import CustomQueryWalker
from Products.contentmigration.archetypes import ATFolderMigrator,ATItemMigrator
from collective.contentmigrationui.interfaces import IContentMigrator
from zope.interface import implements
from collective.contentmigrationui.utils import BASE_AT_PROPERTIES

class FolderToLargePloneFolder(object, ATFolderMigrator):
    """Migrate the old item type to the new item type
    """
    implements(IContentMigrator)

    walker = CustomQueryWalker
    src_meta_type = "ATFolder"
    src_portal_type = "Folder"
    dst_meta_type = "ATBTreeFolder"
    dst_portal_type = "Large Plone Folder"
    description = "Document to Document"
    safeMigration = True

    def __init__(self, *args, **kwargs):
        ATFolderMigrator.__init__(self, *args, **kwargs)
        self.fields_map = BASE_AT_PROPERTIES

FolderToLargePloneFolderMigrator = FolderToLargePloneFolder

class DocumentToDocument(object, ATItemMigrator):
    """Migrate the old item type to the new item type
    """
    implements(IContentMigrator)

    walker = CustomQueryWalker
    src_meta_type = "ATDocument"
    src_portal_type = "Document"
    dst_meta_type = "ATDocument"
    dst_portal_type = "Document"
    description = "Document to Document"
    safeMigration = True

    def __init__(self, *args, **kwargs):
        ATItemMigrator.__init__(self, *args, **kwargs)
        self.fields_map = BASE_AT_PROPERTIES

DocumentToDocumentMigrator = DocumentToDocument

class DocumentToEvent(object, ATItemMigrator):
    """Migrate the old item type to the new item type
    """
    implements(IContentMigrator)

    walker = CustomQueryWalker
    src_meta_type = "ATDocument"
    src_portal_type = "Document"
    dst_meta_type = "ATEvent"
    dst_portal_type = "Event"
    description = "Document to Event"
    safeMigration = True

    def __init__(self, *args, **kwargs):
        ATItemMigrator.__init__(self, *args, **kwargs)
        self.fields_map = BASE_AT_PROPERTIES

DocumentToEventMigrator = DocumentToEvent

class DocumentToNewsitem(object, ATItemMigrator):
    """Migrate the old item type to the new item type
    """
    implements(IContentMigrator)

    walker = CustomQueryWalker
    src_meta_type = "ATDocument"
    src_portal_type = "Document"
    dst_meta_type = "ATNewsItem"
    dst_portal_type = "News Item"
    description = "Document to News item"
    safeMigration = True

    def __init__(self, *args, **kwargs):
        ATItemMigrator.__init__(self, *args, **kwargs)
        self.fields_map = BASE_AT_PROPERTIES

DocumentToNewsitemMigrator = DocumentToNewsitem

class NewsitemToDocument(object, ATItemMigrator):
    """Migrate the old item type to the new item type
    """
    implements(IContentMigrator)

    walker = CustomQueryWalker
    src_meta_type = "ATNewsItem"
    src_portal_type = "News Item"
    dst_meta_type = "ATDocument"
    dst_portal_type = "Document"
    description = "Warning: Using this migration will cause lost of all news-item specific fields."
    safeMigration = False

    def __init__(self, *args, **kwargs):
        ATItemMigrator.__init__(self, *args, **kwargs)
        self.fields_map = BASE_AT_PROPERTIES
        
NewsitemToDocumentMigrator = NewsitemToDocument

class NewsItemToEvent(object, ATItemMigrator):
    """Migrate the old item type to the new item type
    """
    implements(IContentMigrator)

    walker = CustomQueryWalker
    src_meta_type = "ATNewsItem"
    src_portal_type = "News Item"
    dst_meta_type = "ATEvent"
    dst_portal_type = "Event"
    description = "Warning: Using this migration will cause lost of news-item's image."
    safeMigration = False

    def __init__(self, *args, **kwargs):
        ATItemMigrator.__init__(self, *args, **kwargs)
        self.fields_map = BASE_AT_PROPERTIES

NewsItemToEventMigrator = NewsItemToEvent