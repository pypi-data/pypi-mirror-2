"""Definition of the Remote Folder content type
"""

from zope.interface import implements, directlyProvides

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

from Products.remotefolder import remotefolderMessageFactory as _
from Products.remotefolder.interfaces import IRemoteFolder
from Products.remotefolder.config import PROJECTNAME

from plone.app.portlets.portlets.rss import RSSFeed
from plone.app.portlets.portlets.rss import FEED_DATA, Renderer
from plone.i18n.normalizer import idnormalizer
from zExceptions import BadRequest



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
    atapi.ComputedField(
        name='body',
        accessor="Body",
        searchable=False,
        widget=atapi.ComputedField._properties['widget'](
            label=u"Body",
            visible={'edit': 'invisible', 'view': 'visible'},
            label_msgid='body',
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

class ContentParser:
    """Class used to detect the type of feed and extract the usefull information
    out of it"""
    
    def __init__(self, item, generator):
        self.type = ""
        self.title = ""
        self.image = ""
        self.description = ""
        self.body = ""
        self.output = ""
        self.url = ""
        self.updated = ""
    
        # For printing all the keys on the items
        #for obj in item:
            #print("Key: " + obj + "\n")
    
        if generator is None:
            self.type = "Document"
        else:
            self.type = "Image"
        
        if item.has_key("title"):
            self.title = item["title"]
        if item.has_key("summary"):
            self.description = item["summary"]
        if item.has_key("url"):
            self.url = item["url"]
        if item.has_key("updated"):
            self.updated = item["updated"]
        if item.has_key("media:content"):
            self.image = item["media:content"]


class RemoteFolder(folder.ATFolder):
    """Folderish type that loads content from an external source like, for example, RSS feeds"""
    implements(IRemoteFolder)

    meta_type = "Remote Folder"
    schema = RemoteFolderSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')
    
    

    def getRemoteData(self):
        """Get items from RSS feed and convert them to plone objects.
        Receives a RemoteFolder item and updates all the URI"""
        URIField = getattr(self, "URI", None)
        returnValue = True
        
        if URIField is not None:
            urls = URIField.split(" ")
        else:
            returnValue = False
           
        for url in urls:
            feed = self.getFeed(url)
            if feed is not None:
                returnValue = self.addPloneObjects(feed)
            else:
                returnValue = "NO FEED"
            
        return returnValue
        
    def getFeed(self, url):
        """ Gets the RSS from the URL and updates it if it already exists"""
        feed = FEED_DATA.get(url,None)
        feedTimeOut = 100
        
        if feed is None:
            # create it
            feed = FEED_DATA[url] = RSSFeed(url, feedTimeOut)
            feed.update()
        
        return feed
    
    
    def addPloneObjects(self, feed):
        """From a feed object, create plone content in the remote folder"""
        container = self
        result = ""
        feedItem = None
        id = ""
        lastUpdate = getattr(self, "lastUpdated", None)
        
        #to print feed properties
        #for obj in dir(feed):
            #print(obj)
        
        if feed.needs_update:
            feed.update()
        else:
            """If there is no update, do nothing"""
            #return result
        
        for item in feed.items:
            feedItem = ContentParser(item, getattr(item, "generator", None))
            result += "<h1>" + feedItem.title  + "</h1>" + "<BR />" + feedItem.description + "<BR />"
            #ADD PLONE CONTENT HERE
            title = feedItem.title
            id = idnormalizer.normalize(title + "%s"%(feedItem.updated, ))
            
            if hasattr(container, id):
                #If the item exists we continue to the next one
                continue
           
            #And now we create our content
            container.invokeFactory(type_name="Document", id=id, title=feedItem.title)
            obj = container[id]
            obj.setText(feedItem.description)
            obj.portal_workflow.doActionFor(obj, "publish", comment="Remote content automatically published")
        
        return result
        
    def Update(self):
        """Update is used to update feed data and create plone objects"""
        return self.getRemoteData()

atapi.registerType(RemoteFolder, PROJECTNAME)
