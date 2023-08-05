# File: testATPhoto.py
# 
# Copyright (c) 2005 by 
# Generator: ArchGenXML Version 1.4.0-beta2 devel 
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
__author__  = '''Plone Multimedia Team <unknown>'''
__docformat__ = 'plaintext'

import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

##code-section module-header #fill in your manual code here
##/code-section module-header

#
# test-cases for class(es) ATPhoto
#
import os, sys
from Testing import ZopeTestCase
from Products.ATPhoto.tests.testATContentTypeBase import testATContentTypeBase
# import the tested classes
from Products.ATPhoto.ATPhoto import ATPhoto

##code-section module-beforeclass #fill in your manual code here
from Globals import package_home
from Products.ATPhoto import config
from cStringIO import StringIO
##/code-section module-beforeclass


class testATPhoto(testATContentTypeBase):
    """ test-cases for class(es) ATPhoto
    """

    ##code-section class-header_testATPhoto #fill in your manual code here
    def testImageTransforms(self):
        ""
        pt = self.portal.portal_transforms
        imgFile = open(os.path.join(package_home(config.product_globals),'tests','input','canoneye.jpg'), 'rb')
        data = imgFile.read()
        gif = pt.convertTo(target_mimetype='image/gif',orig=data,width=100,height=100)
        png = pt.convertTo(target_mimetype='image/png',orig=data,width=100,height=100)
        bmp =pt.convertTo(target_mimetype='image/x-ms-bmp',orig=data,width=100,height=100)
        pcx =pt.convertTo(target_mimetype='image/pcx',orig=data,width=100,height=100)
        ppm =pt.convertTo(target_mimetype='image/x-portable-pixmap',orig=data,width=100,height=100)
        tiff =pt.convertTo(target_mimetype='image/tiff',orig=data,width=100,height=100)

    ##/code-section class-header_testATPhoto

    def afterSetUp(self):
        """
        """
        pass


    # from class ATPhoto:
    def test_view(self):
        """
        """
        #Uncomment one of the following lines as needed
        self.loginAsPortalOwner()
        self.folder.invokeFactory(id='temp_ATPhoto',type_name='ATPhoto')
        photo = self.folder.temp_ATPhoto
        photo.tag()
        pass


    # from class ATPhoto:
    def test_setImage(self):
        """
        """
        #Uncomment one of the following lines as needed
        ##self.loginAsPortalOwner()
        ##o=ATPhoto('temp_ATPhoto')
        ##self.folder._setObject('temp_ATPhoto', o)
        pass


    # from class ATPhoto:
    def test_getMimeType(self):
        """
        """
        #Uncomment one of the following lines as needed
        ##self.loginAsPortalOwner()
        ##o=ATPhoto('temp_ATPhoto')
        ##self.folder._setObject('temp_ATPhoto', o)
        pass


    # from class ATPhoto:
    def test_getSizes(self):
        """
        """
        #Uncomment one of the following lines as needed
        ##self.loginAsPortalOwner()
        ##o=ATPhoto('temp_ATPhoto')
        ##self.folder._setObject('temp_ATPhoto', o)
        pass


    # from class ATPhoto:
    def test_getWidth(self):
        """
        """
        #Uncomment one of the following lines as needed
        ##self.loginAsPortalOwner()
        ##o=ATPhoto('temp_ATPhoto')
        ##self.folder._setObject('temp_ATPhoto', o)
        pass


    # from class ATPhoto:
    def test_getHeight(self):
        """
        """
        #Uncomment one of the following lines as needed
        ##self.loginAsPortalOwner()
        ##o=ATPhoto('temp_ATPhoto')
        ##self.folder._setObject('temp_ATPhoto', o)
        pass


    # from class ATPhotoTransform:
    def test_hasPIL(self):
        """
        """
        #Uncomment one of the following lines as needed
        ##self.loginAsPortalOwner()
        ##o=ATPhotoTransform('temp_ATPhotoTransform')
        ##self.folder._setObject('temp_ATPhotoTransform', o)
        pass


    # from class ATPhotoTransform:
    def test_setIPTCAttr(self):
        """
        """
        #Uncomment one of the following lines as needed
        ##self.loginAsPortalOwner()
        ##o=ATPhotoTransform('temp_ATPhotoTransform')
        ##self.folder._setObject('temp_ATPhotoTransform', o)
        pass


    # from class ATPhotoTransform:
    def test_getIPTC(self):
        """
        """
        #Uncomment one of the following lines as needed
        ##self.loginAsPortalOwner()
        ##o=ATPhotoTransform('temp_ATPhotoTransform')
        ##self.folder._setObject('temp_ATPhotoTransform', o)
        pass


    # from class ATPhotoTransform:
    def test__exportPIL(self):
        """
        """
        #Uncomment one of the following lines as needed
        ##self.loginAsPortalOwner()
        ##o=ATPhotoTransform('temp_ATPhotoTransform')
        ##self.folder._setObject('temp_ATPhotoTransform', o)
        pass


    # from class ATPhotoTransform:
    def test__getZipFile(self):
        """
        """
        #Uncomment one of the following lines as needed
        ##self.loginAsPortalOwner()
        ##o=ATPhotoTransform('temp_ATPhotoTransform')
        ##self.folder._setObject('temp_ATPhotoTransform', o)
        pass


    # from class ATPhotoTransform:
    def test_exportImage(self):
        """
        """
        #Uncomment one of the following lines as needed
        ##self.loginAsPortalOwner()
        ##o=ATPhotoTransform('temp_ATPhotoTransform')
        ##self.folder._setObject('temp_ATPhotoTransform', o)
        pass


    # from class ATPhotoTransform:
    def test_exportFlickr(self):
        """
        """
        #Uncomment one of the following lines as needed
        ##self.loginAsPortalOwner()
        ##o=ATPhotoTransform('temp_ATPhotoTransform')
        ##self.folder._setObject('temp_ATPhotoTransform', o)
        pass


    # from class FlickrExportable:
    def test_isFlickrAuth(self):
        """
        """
        #Uncomment one of the following lines as needed
        ##self.loginAsPortalOwner()
        ##o=FlickrExportable('temp_FlickrExportable')
        ##self.folder._setObject('temp_FlickrExportable', o)
        pass

    # from class FlickrExportable:
    def test_getFlickrIdAndUrl(self):
        """
        """
        #Uncomment one of the following lines as needed
        ##self.loginAsPortalOwner()
        ##o=ATPhotoTransform('temp_ATPhotoTransform')
        ##self.folder._setObject('temp_ATPhotoTransform', o)
        pass



    # Manually created methods
    def test_export(self):
        """
        """
        #Uncomment one of the following lines as needed
        ##self.loginAsPortalOwner()
        ##o=ATPhotoTransform('temp_ATPhotoTransform')
        ##self.folder._setObject('temp_ATPhotoTransform', o)
        pass

    def test_transform(self):
        """
        """
        #Uncomment one of the following lines as needed
        ##self.loginAsPortalOwner()
        ##o=ATPhotoTransform('temp_ATPhotoTransform')
        ##self.folder._setObject('temp_ATPhotoTransform', o)
        pass


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testATPhoto))
    return suite

##code-section module-footer #fill in your manual code here
##/code-section module-footer


if __name__ == '__main__':
    framework()


