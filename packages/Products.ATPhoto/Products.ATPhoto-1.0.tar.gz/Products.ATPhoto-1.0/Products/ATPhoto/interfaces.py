# -*- coding: utf-8 -*-

from zope.interface import Interface
from zope.schema import Bytes

class ISortable(Interface):
    """
    sort objects in a container object
    """

class IZippable(Interface):
    """
    store your files in a zip file
    """
    def setFile(filename,data):
        """
        store the file inside the zip file
        """

    def setZip():
        """
        initialize the zip file
        """

    def closeZip():
        """
        close the zipe file
        """

    def getZip():
        """
        return the zip file object
        """

    def getRawZip():
        """
        return the raw zip file
        """

    def initIO():
        """
        reinit the ZIP IO
        """

class IScalable(Interface):
    """
    object with scalable image
    """

    def getScale(scale=None):
        """
        return scaled image
        """
    
    def tag(scale=None,**kwargs):
        """
        return image tag
        """
class IPossibleZippable(Interface):
    """
    marker interface for possible zippable object
    """

       
class IPossibleScalable(Interface):
    """
    marker interface for possible scalable object
    """


class ISlideShow(Interface):
    """
    provide some js stuff
    """

    def getContents():
        """
        return the js stuff
        """

class IPossibleSlideShow(Interface):
    """
    marker interface for possible slide show
    """

class IPhotoAlbum(Interface):
    """
    marker interface photo album
    """

    def setSymbolic_photo():
        """
        set the symbolic photo for an album
        """

class IPhoto(Interface):
    """
    marker interface for photo
    """
