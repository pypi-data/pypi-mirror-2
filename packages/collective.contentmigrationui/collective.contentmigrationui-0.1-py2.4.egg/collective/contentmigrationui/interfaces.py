from zope.interface import Interface
from zope.interface import Attribute

class IContentMigrator(Interface):
    """Interface for migrator registration"""
    title = Attribute("The migration title")
    src_meta_type = Attribute("source content meta type")
    src_portal_type = Attribute("source content portal type")
    dst_meta_type = Attribute("destination content meta type")
    dst_portal_type = Attribute("destination content portal type")