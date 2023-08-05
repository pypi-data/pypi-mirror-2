# File: ATPhotoAlbum.py
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


from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
from FlickrExportable import FlickrExportable


# additional imports from tagged value 'import'
from Products.CMFCore.utils import getToolByName
from Products.ATPhoto.ATPhoto import ATPhoto_schema
from cStringIO import StringIO
import os
import string
from zipfile import ZipFile
import tarfile
from uploadr import Uploadr
from Products.ATContentTypes.content.folder import ATFolder
from Products.ATContentTypes.content.folder import ATFolderSchema

from Products.ATPhoto.config import *
##code-section module-header #fill in your manual code here
from Acquisition import aq_self
from Products.ATPhoto.interfaces import IScalable, IPossibleScalable
from Products.CMFCore.permissions import View

if HAS_LINGUA_PLONE:
    from Products.LinguaPlone.public import *
##/code-section module-header

schema=Schema((
    ReferenceField('symbolic_photo',
        widget=ReferenceWidget(
            label='Symbolic photo',
            description="Choose a symbolic photo for the album.",
            label_msgid='ATPhoto_label_symbolic_photo',
            description_msgid='ATPhoto_help_symbolic_photo',
            i18n_domain='ATPhoto',
        ),
        required=False,
        relationship='Sym',
        multiValued=False,
        vocabulary='getDisplayPhotosList'
    ),

),
)


##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

ATPhotoAlbum_schema = ATFolderSchema + \
    getattr(FlickrExportable,'schema',Schema(())) + \
    schema

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class ATPhotoAlbum(FlickrExportable,ATFolder):
    security = ClassSecurityInfo()
    __implements__ = (getattr(FlickrExportable,'__implements__',()),) + (getattr(ATFolder,'__implements__',()),)


    # This name appears in the 'add' box
    archetype_name             = 'Photo Album'

    meta_type                  = 'ATPhotoAlbum'
    portal_type                = 'ATPhotoAlbum'
    allowed_content_types      = ['ATPhoto', 'ATPhotoAlbum'] + list(getattr(FlickrExportable, 'allowed_content_types', []))
    filter_content_types       = 1
    global_allow               = 1
    allow_discussion           = 0
    content_icon               = 'ATPhotoAlbum.gif'
    immediate_view             = 'atphotoalbum_dom_view'
    default_view               = 'atphotoalbum_dom_view'
    suppl_views                = ('atphotoalbum_dom_view','atphotoalbum_view','atphotoalbum_listing','folder_listing','folder_summary_view','folder_tabular_view' )
    typeDescription            = "Photo Album"
    typeDescMsgId              = 'description_edit_atphotoalbum'

    actions =  (


       {'action':      "string:${object_url}/view",
        'category':    "object",
        'id':          'view',
        'name':        'View',
        'permissions': ("View",),
        'condition'  : 'python:1'
       },


       {'action':      "string:${object_url}/atphotoalbum_export",
        'category':    "object",
        'id':          'export',
        'name':        'Export',
        'permissions': ("View",),
        'condition'  : 'python:1'
       },


       {'action':      "string:${object_url}/atphotoalbum_import",
        'category':    "object",
        'id':          'import',
        'name':        'Import',
        'permissions': ("View",),
        'condition'  : 'python:1'
       },


       {'action':      "string:${object_url}/atphotoalbum_slideshow",
        'category':    "object",
        'id':          'slideshow',
        'name':        'Slideshow',
        'permissions': ("View",),
        'condition'  : 'python:1'
       },


    )

    schema = ATPhotoAlbum_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header


    #Methods

    security.declarePublic('getAvailableSizes')
    def getAvailableSizes(self):
        """
           return avalaible sizes from ATPhoto schema
        """
        field = ATPhoto_schema.get('image')
        return field.sizes

    security.declarePublic('listPhotos')
    def listPhotos(self,basepath='',recursive=0):
        if(not basepath):
            basepath = self.getId()
        list = []
        dict = {}
        for object in self.listFolderContents():
            path = "%s/%s" % (basepath,object.getId())
            if(object.meta_type=='ATPhoto'):
                dict[path] = object
            elif recursive:
                list += object.listPhotos(basepath=path,recursive=1)
        if(dict):
            list.append(dict)
        return list

    security.declarePublic('exportFlickr')
    def importFlickrSet(self, photoSetId,frob, token=None,flickrAuth=None, REQUEST=None):
        """
          Import photos inside ATPhotoAlbum from Flickr
        """
        if(not flickrAuth):
            flickrAuth = REQUEST.SESSION.has_key('flickrAuth')
        if(not frob):
            frob = REQUEST.SESSION.get('frob')
        if(not token):
            token = REQUEST.SESSION.get('token')
        if(flickrAuth):
            flick = Uploadr(frob=str(frob),token=token)
        if(flickrAuth):
            photos = flick.getSetPhotos(photoSetId)
            count = 0
            for photo in photos:
                if(photo['id'] not in self.objectIds()):
                    self.invokeFactory('ATPhoto',photo['id'],RESPONSE=None)
                atphoto = getattr(self,photo['id'])
                atphoto.setImage(StringIO( photo['data']))
                atphoto.setTitle(photo['title'])
                count+=1
            msg = 'Imported %s photos from your flickr account' % count
        else:
            msg = 'Not Authenticated!'
        if(REQUEST):
            url = "%s/view?portal_status_message=" % self.absolute_url()
            target = "%s%s" % (url,msg)
            REQUEST.RESPONSE.redirect(target)
        else:
           return msg


    security.declarePublic('exportFlickr')
    def exportFlickr(self, frob, token,tags='', recursive=0,flickrAuth=False, REQUEST=None):
        """
          Export photos inside ATPhotoAlbum to Flickr
        """
        url = "%s/atphotoalbum_export?portal_status_message=" % self.absolute_url()
        #if(not flickrAuth):
        #    flickrAuth = REQUEST.SESSION.has_key('flickrAuth')
        if(flickrAuth):
        #    frob = REQUEST.SESSION.get('frob')
        #    token = REQUEST.SESSION.get('token')
            for dict in self.listPhotos(recursive=int(recursive)):
                for key in dict.keys():
                    object = dict[key]
                    dict[key] = object.exportFlickr(frob=frob,tags=tags,token=token,flickrAuth=1)
            msg = ', '.join(dict.values())
        else:
            msg = 'Not Authenticated!'
        target = "%s%s" % (url,msg)
        if(REQUEST):
            REQUEST.RESPONSE.redirect(target)
        else:
           return msg

    security.declarePublic('tag')
    def tag(self,**kwargs):
        """
        return the tag of symbolic_photo
        """
        container = aq_self(self)
        if IPossibleScalable.providedBy(container):
            if not kwargs.has_key('scale'):
                kwargs.setdefault('scale','thumb')
            return IScalable(container).tag(**kwargs)
        return ''

    security.declarePublic('hasPloneJUpload')
    def hasPloneJUpload(self):
        """
        test if we have PloneJUpload installed
        """
        qi = getToolByName(self,'portal_quickinstaller')
        ploneJUpload = [prod for prod in qi.listInstalledProducts() if (prod['id']=='PloneJUpload')]
        return (bool(ploneJUpload) and ploneJUpload[0]['status'] == 'installed')



    security.declarePrivate('extractZipFile')
    def extractZipFile(self, zipFile):
        """
          Extract file in a zip
        """
        zip = ZipFile(zipFile,"r",8)
        file_list = {}
        for filename in zip.namelist():
            path,newfilename = os.path.split(filename)
            if newfilename[:2] != '._': ## Avoid to import OSX files
                data = zip.read(filename)
                if(len(data)):
                    file_list[newfilename] = data
        return file_list



    security.declarePrivate('extractTarFile')
    def extractTarFile(self, tarFile, ext):
        """
          Extract file in a tar
        """
        file_list = {}
        if(ext == '.tar'):
            tar = tarfile.open(mode="r|",fileobj=tarFile)
        elif(ext == '.gz'):
            tar = tarfile.open(mode="r|gz",fileobj=tarFile)
        elif(ext == '.bz2'):
            tar = tarfile.open(mode="r|bz2",fileobj=tarFile)
        for filename in tar:
            path,newfilename = os.path.split(filename.name)
            if(filename.isfile() and newfilename[:2] != '._'):
                data = tar.extractfile(filename)
                file_list[newfilename] = data.read()
        return file_list



    security.declarePublic('importPhotos')
    def importPhotos(self, zipFile, REQUEST=None):
        """
          Import photos from a zipFile
        """
        name, ext = os.path.splitext(zipFile.filename)
        ext = string.lower(ext)
        if(ext == '.zip'):
            filesList = self.extractZipFile(zipFile)
        elif(ext in ['.tar','.gz','.bz2']):
            filesList = self.extractTarFile(zipFile, ext)
        else:
            msg = "Error: wrong extention! File must be zip, tar, gz or bz2"
            if(REQUEST):
                REQUEST.RESPONSE.redirect("%s/atphotoalbum_import?portal_status_message=%s" % (self.absolute_url(),msg))
            return msg
        for key in filesList:
        #    data = StringIO( filesList[key] )
            data = str(filesList[key])
            self.invokeFactory('ATPhoto',key,RESPONSE=None)
            atphoto = getattr(self,key)
            atphoto.setImage(str(data))
        msg = "Imported %s photos from file" % len(filesList)
        if(REQUEST):
            REQUEST.RESPONSE.redirect("%s/atphotoalbum_import?portal_status_message=%s" % (self.absolute_url(),msg))
        return msg


    security.declarePublic('autoTransformImage')
    def autoTransformImage(self, REQUEST=None):
        """
        auto rotate all photos in folder
        """
        imgs = self.getFolderContents(contentFilter={'meta_type':['ATPhoto']})
        rotated_img = []
        for img in imgs:
            if(img.getObject().autoTransformImage()[1]):
                rotated_img.append(img.getId)
        msg = "Auto rotated: %s" % ' ,'.join(rotated_img)
        if(REQUEST):
            REQUEST.RESPONSE.redirect("%s/view?portal_status_message=%s" % (self.absolute_url(),msg))
        return msg



    security.declarePrivate('getDisplayPhotosList')
    def getDisplayPhotosList(self):
        """
        return a display list for symbolic_photo field
        """
        brains = self.getFolderContents(contentFilter={'meta_type':['ATPhoto']})
        photos_list = [(b.getObject().UID(), str(b.Title or b.getId)[:70]) for b in brains]
        return DisplayList( [('','<no reference>')] + photos_list )



registerType(ATPhotoAlbum,PROJECTNAME)
# end of class ATPhotoAlbum

##code-section module-footer #fill in your manual code here
##/code-section module-footer



