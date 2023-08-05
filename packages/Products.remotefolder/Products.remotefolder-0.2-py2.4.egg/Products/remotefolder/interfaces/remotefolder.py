from zope import schema
from zope.interface import Interface

from zope.app.container.constraints import contains
from zope.app.container.constraints import containers

from Products.remotefolder import remotefolderMessageFactory as _

class IRemoteFolder(Interface):
    """Folderish type that loads content from an external source like, for example, RSS feeds"""
    
    # -*- schema definition goes here -*-
    
        
class IRemoteDataUpdater(Interface):
    """Class used to convert RSS data into Plone objects."""
 
    def getRemoteData(self, remoteFolder):
        """Get items from RSS feed and convert them to plone objects.
        Receives a RemoteFolder item and updates all the URI"""
   
    def _getFeed(self, url):
        """ Gets the RSS from the URL and updates it if it already exists"""


    def _addPloneObjects(self, feed):
        """From a feed object, create plone content in the remote folder"""
