# File: ATPhotoTransform.py
# 
# Copyright (c) 2005 by ['']
# Generator: ArchGenXML Version 1.4.0-RC2 svn/development 
#            http://plone.org/products/archgenxml
#
# GNU General Public Licence (GPL)
# 
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 59 Temple
# Place, Suite 330, Boston, MA  02111-1307  USA
#
__author__  = '''Plone Multimedia Team <natea (at) jazkarta (dot) com>'''
__docformat__ = 'plaintext'


##code-section module-header #fill in your manual code here
from Products.CMFCore.permissions import View
from Globals import InitializeClass
from AccessControl import ClassSecurityInfo
from Products.CMFCore.permissions import ModifyPortalContent
from ExtensionClass import Base
from Products.ATPhoto.thirdparty.iptcinfo import IPTCInfo
from Products.ATContentTypes.config import HAS_PIL
from Products.ATContentTypes.lib.imagetransform import TRANSPOSE_MAP
from Products.ATContentTypes.configuration import zconf
from Products.Archetypes.utils import contentDispositionHeader
from Products.CMFCore.utils import getToolByName
from interfaces import IZippable
from StringIO import StringIO
from zipfile import ZipFile
from DateTime import DateTime
from uploadr import Uploadr
import os
import traceback
import string
from Acquisition import aq_self

import logging
LOG = logging.getLogger('ATPhoto')
if HAS_PIL:
    import PIL.Image
else:
    LOG.warn("ATPhoto can't find PIL. Please install PIL!",exc_info=False)

_types = {
    'PNG': 'image/png',
    'JPEG': 'image/jpeg',
    'GIF': 'image/gif',
    'BMP': 'image/x-ms-bmp',
    'PCX': 'image/pcx',
    'PPM': 'image/x-portable-pixmap',
    'TIFF': 'image/tiff',
    'ZIP': 'application/zip'
}
_orientation = {1: 'Horizontal (normal)',
              2: 'Mirrored horizontal',
              3: 'Rotated 180',
              4: 'Mirrored vertical',
              5: 'Mirrored horizontal then rotated 90 CCW',
              6: 'Rotated 90 CW',
              7: 'Mirrored horizontal then rotated 90 CW',
              8: 'Rotated 90 CCW'}
##/code-section module-header




class ATPhotoTransform(Base):
    ''' '''
    __implements__ = (getattr(Base,'__implements__',()),)

    ##code-section class-header_ATPhotoTransform #fill in your manual code here
    security = ClassSecurityInfo()

    actions = (
        {
        'id'          : 'transform',
        'name'        : 'Transform',
        'action'      : 'string:${object_url}/atphoto_transform',
        'permissions' : (ModifyPortalContent,),
        'condition'   : 'object/hasPIL',
         },
        {'action':      "string:$object_url/atphoto_export",
        'category':    "object",
        'id':          'atphoto_export',
        'name':        'Export',
        'permissions': (View,),
        'condition'  : 'python:1'
       },

        )


    ##/code-section class-header_ATPhotoTransform

    security.declareProtected(View, 'getEXIFOrientation')
    def getEXIFOrientation(self):
        """Get the rotation and mirror orientation from the EXIF data
        Some cameras are storing the informations about rotation and mirror in
        the exif data. It can be used for autorotation.
        """
        exif = self.getEXIF()
        mirror = 0
        rotation = 0
        code = exif.get('Image Orientation', None)
        for key,value in _orientation.iteritems():
            if code == value:
                code = key
                break
        if code is None:
            return (mirror, rotation)
        try:
            code = int(code)
        except ValueError:
            return (mirror, rotation)
        if code in (2, 4, 5, 7):
            mirror = 1
        if code in (1, 2):
            rotation = 0
        elif code in (3, 4):
            rotation = 180
        elif code in (5, 6):
            rotation = 90
        elif code in (7, 8):
            rotation = 270
        return (mirror, rotation)

    def hasPIL(self):
        """Is PIL installed?
        """
        return HAS_PIL


    def setIPTCAttr(self,dict):
        """Set iptc attributes inside the photo
        """
        io = self.getImageAsFile(img, scale=None)
        if io is not None:
            # some cameras are naughty :(
            try:
                io.seek(0)
                iptc_info = IPTCInfo(io)
                for key in dict:
                    iptc_info[key]=dict
                iptc_info.saveAs(io)
            except:
                io.seek(0)
                LOG.error('Failed to process IPTC information', exc_info=True)
                # seek to 0 and do NOT close because we might work
                # on a file upload which is required later
            else:
                io.seek(0)
                self.setImage(io)


    def getIPTC(self, img=None, refresh=False):
        """Get the exif informations of the file
        The information is cached in _v_image_iptc
        """
        cache = '_image_iptc'
        if refresh:
            setattr(self, cache, None)
        iptc_data = getattr(self, cache, None)
        if iptc_data is None or not isinstance(iptc_data, dict):
            io = self.getImageAsFile(img, scale=None)
            if io is not None:
                # some cameras are naughty :(
                try:
                    io.seek(0)
                    iptc_data = IPTCInfo(io).getNiceData()
                except:
                    LOG.error('Failed to process IPTC information', exc_info=True)
                    iptc_data = {}
                # seek to 0 and do NOT close because we might work
                # on a file upload which is required later
                io.seek(0)

        if not iptc_data:
            # alawys return a dict
            iptc_data = {}
        # set the EXIF cache even if the image has returned an empty
        # dict. This prevents regenerating the exif every time if an
        # image doesn't have exif information.
        setattr(self, cache, iptc_data)
        return iptc_data


    def exportImage(self,format,newwidth=0,newheight=0,zip=0,REQUEST={}):
        """
          Export an image into a new format
        """
        name,ext = os.path.splitext(self.getField('image').getFilename(self))
        pt = getToolByName(self, 'portal_transforms')
        destMimetype = _types[format]
        newfilename = "%s.%s" % (name, string.lower(format))
        file = pt.convertTo(target_mimetype=destMimetype,orig=self.getImageAsFile().read(),\
                            width=newwidth,height=newheight)
        if(int(zip)==1):
            zipf = IZippable(self)
            zipf.setFile(newfilename,str(file))
            file = zipf.getRawZip()
            newfilename = '%s.zip' % newfilename

        if(REQUEST):
            header_value = contentDispositionHeader('attachment', self.getCharset(), filename=newfilename)
            REQUEST.RESPONSE.setHeader("Content-disposition", header_value)
            REQUEST.RESPONSE.write(str(file))
        else:
            return newfilename,file


    def exportFlickr(self, frob='', title='', description='', tags='', token='',flickrAuth=False, REQUEST=None):
        """
          Export photo inside ATPhoto to Flickr
        """
        url = "%s/atphoto_export?portal_status_message=" % self.absolute_url()
        if(not flickrAuth):
            flickrAuth = REQUEST.SESSION.has_key('flickrAuth')
        if(not frob):
            frob = REQUEST.SESSION.get('frob')
        if(not token):
            token = REQUEST.SESSION.get('token')
        if(flickrAuth):
            flick = Uploadr(frob=str(frob),token=token)
            flick.setTitle(title)
            flick.setTag(tags)
            flick.setDescription(description)
            field = self.getField('image')
            filename = field.getFilename(self)
            if(flick.uploadImageFromData(self.getImageAsFile().read(),filename)):
                msg = '%s export successful to your Flickr account' % self.getId()
            else:
                msg = 'Error while exporting %s: %s' % (self.getId(),flick.getError())
        else:
            msg = 'Not Authenticated!'
        target = "%s%s" % (url,msg)
        if(REQUEST):
            REQUEST.RESPONSE.redirect(target)
        else:
            return msg


    def transformImage(self, method, REQUEST=None):
        """
        Tra
        nsform an Image:
            FLIP_LEFT_RIGHT
            FLIP_TOP_BOTTOM
            ROTATE_90 (rotate counterclockwise)
            ROTATE_180
            ROTATE_270 (rotate clockwise)
        """ 
        method = int(method)
        if method not in TRANSPOSE_MAP:
            raise RuntimeError, "Unknown method %s" % method

        target = self.absolute_url() + '/view?force_refresh=1'

        if not HAS_PIL:
            if REQUEST:
                REQUEST.RESPONSE.redirect(target)

        image = self.getImageAsFile()
        image2 = StringIO()

        if image is not None:
            img = PIL.Image.open(image)
            del image
            fmt = img.format
            img = img.transpose(method)
            img.save(image2, fmt, quality=zconf.pil_config.quality)

            field = self.getField('image')
            mimetype = field.getContentType(self)
            filename = field.getFilename(self)

            # because AT tries to get mimetype and filename from a file like
            # object by attribute access I'm passing a string along
            self.setImage(image2.getvalue(), mimetype=mimetype,
                          filename=filename, refresh_exif=False)

        if REQUEST:
             REQUEST.RESPONSE.redirect(target)


##code-section module-footer #fill in your manual code here
##/code-section module-footer



