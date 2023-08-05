# -*- coding: utf-8 -*-
from Acquisition import aq_inner, aq_parent

from Products.Five import BrowserView

from zope.app import zapi
from interfaces import  IPhotoAlbum
from interfaces import  IScalable, ISlideShow, IZippable, ISortable
import os

class ScalableView(BrowserView):
    """
    a view for object with scalable image
    """

    def getImage(self,scale=None):
        # this is tricky. don't remove this test !
        # it's used when we want to test item_object/image_thumb in a template
        # - gawel
        if not self.request.URL.endswith('image_%s' % (scale,)):
            return True

        # get the image from adapted object
        adapted = IScalable(self.context)
        image = adapted.getScale(scale)
        index_html = getattr(image,'index_html',None)
        if index_html:
            return index_html(self.request,self.request.RESPONSE)
        return ''

    def image_thumb(self):
        return self.getImage('thumb')

    def image_preview(self):
        return self.getImage('preview')

    def image_large(self):
        return self.getImage('large')

    def image_mini(self):
        return self.getImage('mini')

    def image_tile(self):
        return self.getImage('tile')

    def image_icon(self):
        return self.getImage('icon')

    def image_listing(self):
        return self.getImage('listing')


class SortView(BrowserView):
    def redirect(self, msg):
        url = zapi.absoluteURL(self.context, self.request)
        redir = "%s/view?portal_status_message=%s" % (url,msg)
        return self.request.RESPONSE.redirect(redir)

    def sortById(self, reverse=False, caseunsensitive=False):
        adapted = ISortable(self.context)
        adapted.sort('id',reverse,caseunsensitive)
        msg = 'Album sorted by ID'
        self.redirect(msg)

    def sortByExifDateTime(self,reverse=False, caseunsensitive=False):
        adapted = ISortable(self.context)
        adapted.sortExifDateTime()
        msg = 'Album sorted fallowing the DateTime contained in EXIF tags'
        self.redirect(msg)

    def sortReverse(self):
        adapted = ISortable(self.context)
        adapted.sortReverse()
        msg = 'Album has a reversed order'
        self.redirect(msg)


class ZipView(BrowserView):
    def getZipFile(self, format, width, height, recursive=0):
        adapted = IZippable(self.context)
        for dict in self.context.listPhotos(recursive=int(recursive)):
            for key in dict.keys():
                object = dict[key]
                filename, data = object.exportImage(format,width,height)
                path,file = os.path.split(key)
                key = "%s/%s" % (path,filename)
                if file:
                    adapted.setFile(key,data)
        self.request.RESPONSE.setHeader('Content-Type','application/zip')
        self.request.RESPONSE.addHeader("Content-Disposition","filename=%s.zip" % self.context.getId())
        self.request.RESPONSE.write(adapted.getRawZip())


class SlideShowView(BrowserView):

    def getContents(self):
        ''' return js stuff for slideshow '''
        self.request.RESPONSE.setHeader('Content-Type','text/plain;charset=UTF-8')
        adapted = ISlideShow(self.context)
        return adapted.getContents()

class PhotoView(BrowserView):

    def nextURL(self,message=''):
        url = zapi.absoluteURL(self.context, self.request)
        return "%s/view?portal_status_message=%s" % (url,message)
    
    def setSymbolic(self):
        """
        set photo as symbolic photo
        """
        parent = aq_parent(aq_inner(self.context))
        if IPhotoAlbum.providedBy(parent):
            parent.setSymbolic_photo(self.context.UID())
            return self.request.RESPONSE.redirect(self.nextURL('Symbolic photo changed.'))
        return self.request.RESPONSE.redirect(self.nextURL('Photo is not in a valid album.'))

