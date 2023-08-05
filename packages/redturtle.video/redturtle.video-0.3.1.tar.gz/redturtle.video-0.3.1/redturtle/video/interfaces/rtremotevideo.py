from zope import schema
from zope.interface import Interface

from zope.app.container.constraints import contains
from zope.app.container.constraints import containers
from Products.ATContentTypes.interface.link import IATLink
from redturtle.video.interfaces import IRTVideo

from redturtle.video import videoMessageFactory as _


class IRTRemoteVideo(IATLink, IRTVideo):
    """A link to a video with screenshot"""

    # -*- schema definition goes here -*-
