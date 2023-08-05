from zope.i18nmessageid import MessageFactory

# your.app.package must match domain declaration in .po files
ContentMigrationUiMessageFactory = MessageFactory('collective.contentmigrationui')
  # -*- extra stuff goes here -*- 

def initialize(context):
    """Initializer called when used as a Zope 2 product."""
