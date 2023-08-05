from zope import schema
from zope.interface import Interface

from zope.app.container.constraints import contains
from zope.app.container.constraints import containers

from Products.remotefolder import remotefolderMessageFactory as _

class IRemoteFolder(Interface):
    """Folderish type that loads content from an external source like, for example, RSS feeds"""
    
    # -*- schema definition goes here -*-
