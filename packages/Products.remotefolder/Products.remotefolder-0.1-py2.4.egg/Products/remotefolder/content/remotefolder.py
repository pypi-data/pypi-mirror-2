"""Definition of the Remote Folder content type
"""

from zope.interface import implements, directlyProvides

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

from Products.remotefolder import remotefolderMessageFactory as _
from Products.remotefolder.interfaces import IRemoteFolder
from Products.remotefolder.config import PROJECTNAME

RemoteFolderSchema = folder.ATFolderSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-
    atapi.StringField(
        name='URI',
        required=False,
        searchable=True,
        widget=atapi.StringWidget(
            label=u"Source URI",
            label_msgid='remotefolder_label_URI',
        )
    ),

))

# Set storage on fields copied from ATFolderSchema, making sure
# they work well with the python bridge properties.

RemoteFolderSchema['title'].storage = atapi.AnnotationStorage()
RemoteFolderSchema['description'].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(
    RemoteFolderSchema,
    folderish=True,
    moveDiscussion=False
)

class RemoteFolder(folder.ATFolder):
    """Folderish type that loads content from an external source like, for example, RSS feeds"""
    implements(IRemoteFolder)

    meta_type = "Remote Folder"
    schema = RemoteFolderSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')
    
    # -*- Your ATSchema to Python Property Bridges Here ... -*-

atapi.registerType(RemoteFolder, PROJECTNAME)
