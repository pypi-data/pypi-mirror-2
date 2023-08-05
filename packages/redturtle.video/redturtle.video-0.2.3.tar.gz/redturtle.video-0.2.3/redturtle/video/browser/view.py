from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from collective.flowplayer.browser.view import File, Link
from plone.memoize.instance import memoize
from zope import component, interface
import urllib

YOUTUBE_EMBED_CODE = """
<object width="640" height="385">
    <param name="movie" value="%(video_url)s"></param>
    <param name="allowFullScreen" value="true"></param>
    <param name="allowscriptaccess" value="always"></param>
    <embed src="%(video_url)s"
           type="application/x-shockwave-flash" allowscriptaccess="always"      
           allowfullscreen="true" width="640" height="385">
    </embed>
</object>
"""

class InternalVideo(File):
    """The Internal Video browser view"""

    def href(self):
        return self.context.absolute_url()+'/at_download/file'

class RemoteVideo(Link):
    """The External Video link browser view"""

    def fromYouTube(self):
        """Check if the current player must be taken from youtube"""
        return self.context.getRemoteUrl().startswith("http://www.youtube.com/")
    
    def getYoutubePlayerCode(self):
        """Return code to get the youtube player"""
        remote_url = self.context.getRemoteUrl()
        video_url = remote_url.replace('watch?v=', 'v/')
        return YOUTUBE_EMBED_CODE % {'video_url' : video_url} 