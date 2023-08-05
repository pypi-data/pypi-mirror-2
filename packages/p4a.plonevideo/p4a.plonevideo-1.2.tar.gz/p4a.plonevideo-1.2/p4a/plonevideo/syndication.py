from zope import component
from zope import interface
from p4a.video import interfaces
from Products.CMFCore import utils as cmfutils
from Products.fatsyndication import adapters as fatadapters
from Products.basesyndication import interfaces as baseinterfaces

class VideoContainerFeed(fatadapters.BaseFeed):
    interface.implements(baseinterfaces.IFeed)
    component.adapts(interfaces.IVideoContainerEnhanced)

class VideoContainerFeedSource(fatadapters.BaseFeedSource):
    interface.implements(baseinterfaces.IFeedSource)
    component.adapts(interfaces.IVideoContainerEnhanced)

    def getFeedEntries(self):
        """See IFeedSoure
        """
        video_items = interfaces.IVideoProvider(self.context).video_items
        return [baseinterfaces.IFeedEntry(x.context) 
                for x in video_items]

class VideoFeed(fatadapters.BaseFeed):
    interface.implements(baseinterfaces.IFeed)
    component.adapts(interfaces.IVideoEnhanced)

class VideoFeedSource(fatadapters.BaseFeedSource):
    interface.implements(baseinterfaces.IFeedSource)
    component.adapts(interfaces.IVideoEnhanced)

    def getFeedEntries(self):
        """See IFeedSoure
        """
        return [baseinterfaces.IFeedEntry(self.context)]

class VideoFeedEntry(fatadapters.BaseFeedEntry):
    interface.implements(baseinterfaces.IFeedEntry)
    component.adapts(interfaces.IVideoEnhanced)
    
    def __init__(self, context):
        fatadapters.BaseFeedEntry.__init__(self, context)
        
        self.video = interfaces.IVideo(self.context)
    
    def getBody(self):
        """See IFeedEntry.
        """
        return ''
    
    def getEnclosure(self):
        return baseinterfaces.IEnclosure(self.context)
    
    def getTitle(self):
        return self.video.title

    def getDescription(self):
        return self.video.description

class ATFileEnclosure(object):
    interface.implements(baseinterfaces.IEnclosure)
    component.adapts(interfaces.IVideoEnhanced)
    
    def __init__(self, context):
        self.context = context
        self.enclosure = self.context.getFile()
    
    def getURL(self):
        return self.context.absolute_url()

    def getLength(self):
       return self.enclosure.get_size()

    def __len__(self):
        return self.getLength()

    def getMajorType(self):
        return self.getType().split('/')[0]

    def getMinorType(self):
        return self.getType().split('/')[1]

    def getType(self):
        return self.enclosure.getContentType()
