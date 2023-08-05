# File: ATPhoto.py
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
from ATPhotoTransform import ATPhotoTransform
from FlickrExportable import FlickrExportable


# additional imports from tagged value 'import'
from Products.ATContentTypes.content.image import ATImageSchema
from Products.ATContentTypes.content.image import ATImage
#from Products.ATContentTypes.content.base import updateActions
from Products.ATContentTypes.content.base import ATCTFileContent
from Products.ATPhoto.config import *
if FS_STORAGE:
    try:
        from Products.FileSystemStorage.FileSystemStorage import FileSystemStorage
    except:
        raise DependancyError('If you want to use FileSystemStorage you need to install the FileSystemStorage Product')

##code-section module-header #fill in your manual code here
from Acquisition import aq_inner
from Acquisition import aq_parent
from Acquisition import aq_self
from Products.ATPhoto.interfaces import IScalable, IPossibleScalable

from Products.Archetypes.public import Schema
from Products.Archetypes.public import ImageField
from Products.Archetypes.public import ImageWidget
from Products.Archetypes.public import PrimaryFieldMarshaller
from Products.ATContentTypes.configuration import zconf
from Products.validation import V_REQUIRED

from Products.CMFCore.permissions import View
import random


if HAS_LINGUA_PLONE:
    from Products.LinguaPlone.public import *
##/code-section module-header

schema=Schema((
),
)


##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

ATPhoto_schema = ATImageSchema + \
    getattr(ATPhotoTransform,'schema',Schema(())) + \
    getattr(FlickrExportable,'schema',Schema(())) + \
    schema

if FS_STORAGE:
    Fullschema = ATPhoto_schema.copy()
    del Fullschema['image']
    ATPhoto_schema = Fullschema + Schema((
    ImageField('image',
               required=True,
               primary=True,
               languageIndependent=True,
#               storage = AnnotationStorage(migrate=True),
               storage = FileSystemStorage(),
               swallowResizeExceptions = zconf.swallowImageResizeExceptions.enable,
               pil_quality = zconf.pil_config.quality,
               pil_resize_algo = zconf.pil_config.resize_algo,
               max_size = zconf.ATImage.max_image_dimension,
               sizes= {'large'   : (768, 768),
                       'preview' : (400, 400),
                       'mini'    : (200, 200),
                       'thumb'   : (128, 128),
                       'tile'    :  (64, 64),
                       'icon'    :  (32, 32),
                       'listing' :  (16, 16),
                      },
               validators = (('isNonEmptyFile', V_REQUIRED),
                             ('checkImageMaxSize', V_REQUIRED)),
               widget = ImageWidget(
                        #description = "Select the image to be added by clicking the 'Browse' button.",
                        #description_msgid = "help_image",
                        description = "",
                        label= "Image",
                        label_msgid = "label_image",
                        i18n_domain = "plone",
                        macro='fss_file_widget',
                        show_content_type = False,)),

    ), marshall=PrimaryFieldMarshaller()
    )



##code-section after-schema #fill in your manual code here
ATPhoto_schema['title'].required = 0
##/code-section after-schema

class ATPhoto(ATPhotoTransform,FlickrExportable,ATImage):
    security = ClassSecurityInfo()
    __implements__ = (getattr(ATPhotoTransform,'__implements__',()),) + (getattr(FlickrExportable,'__implements__',()),) + (getattr(ATImage,'__implements__',()),)


    # This name appears in the 'add' box
    archetype_name             = 'Photo'

    meta_type                  = 'ATPhoto'
    portal_type                = 'ATPhoto'
    allowed_content_types      = [] + list(getattr(ATPhotoTransform, 'allowed_content_types', [])) + list(getattr(FlickrExportable, 'allowed_content_types', []))
    filter_content_types       = 1
    global_allow               = 1
    allow_discussion           = 0
    content_icon               = 'ATPhoto.gif'
    immediate_view             = 'atphoto_view'
    default_view               = 'atphoto_view'
    suppl_views                = ()
    typeDescription            = "Photo"
    typeDescMsgId              = 'description_edit_atphoto'

    actions =  (


       {'action':      "string:${object_url}/atphoto_view",
        'category':    "object",
        'id':          'view',
        'name':        'None',
        'permissions': ("View",),
        'condition'  : 'python:1'
       },


    )

    schema = ATPhoto_schema

    ##code-section class-header #fill in your manual code here
    #actions = updateActions(ATCTFileContent, ATPhotoTransform.actions)
    ##/code-section class-header


    #Methods

    security.declarePrivate('setImage')
    def setImage(self, value, refresh_exif=True, refresh_iptc=True, **kwargs):
        self.getIPTC(value,refresh=refresh_iptc)
        self.getEXIF(value, refresh=refresh_exif)
        self._setATCTFileContent(value, **kwargs)



    security.declarePublic('getMimeType')
    def getMimeType(self):
        return self.lookupMime(self.get_content_type())



    security.declarePublic('getSizes')
    def getSizes(self):
        field = self.getField('image')
        sizes = field.getAvailableSizes(self).keys()
        sizes.append('full')
        return sizes



    security.declarePublic('getWidth')
    def getWidth(self, scale=None):
        if(scale!='full'):
            return self.getSize(scale)[0]
        else:
            return self.width



    security.declarePublic('getHeight')
    def getHeight(self, scale=None):
        if(scale!='full'):
            return self.getSize(scale)[1]
        else:
            return self.height

    security.declarePublic('getAvailableSizes')
    def getAvailableSizes(self):
        """
           return avalaible sizes from ATPhoto schema
        """
        field = ATPhoto_schema.get('image')
        return field.sizes



    security.declarePublic('tag')
    def tag(self,**kwargs):
        """
        return the tag of symbolic_photo
        """
        scalable = aq_self(self)
        if IPossibleScalable.providedBy(scalable):
            if not kwargs.has_key('scale'):
                kwargs.setdefault('scale','thumb')
            return IScalable(self).tag(**kwargs)
        return ''

    security.declarePublic('redirect')
    def redirect(self, b_start, REQUEST):
        """
         Redirect to another photo in the folder
        """
        parent = aq_parent(aq_inner(self))
        objs = list(parent._objects)
        b_start = int(b_start)
        om = [om['id'] for om in objs if objs.index(om)==b_start ]
        img = parent[om[0]]
        REQUEST.RESPONSE.redirect("%s/view" % img.absolute_url())




registerType(ATPhoto,PROJECTNAME)
# end of class ATPhoto

##code-section module-footer #fill in your manual code here
##/code-section module-footer



