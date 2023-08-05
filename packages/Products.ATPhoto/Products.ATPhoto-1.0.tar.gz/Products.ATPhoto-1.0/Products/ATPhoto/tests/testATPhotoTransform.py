# File: testATPhotoTransform.py
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
# test-cases for class(es) ATPhotoTransform
#
import os, sys
from Testing import ZopeTestCase
from Products.ATPhoto.tests.testATContentTypeBase import testATContentTypeBase
# import the tested classes
from Products.ATPhoto.ATPhotoTransform import ATPhotoTransform
from cStringIO import StringIO
from Products.CMFCore.utils import getToolByName

##code-section module-beforeclass #fill in your manual code here
##/code-section module-beforeclass


class testATPhotoTransform(testATContentTypeBase):
    """ test-cases for class(es) ATPhotoTransform
    """

    ##code-section class-header_testATPhotoTransform #fill in your manual code here
    ##/code-section class-header_testATPhotoTransform

    def afterSetUp(self):
        """
        """
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
#    def test__exportPIL(self):
#        """
#        """
#        atphoto = self.createATPhoto('canoneye.jpg')
#        gifphoto = atphoto._exportPIL('GIF',0,0)
#        atphoto.setImage(gifphoto)
#        self.assertEqual(atphoto.get_content_type(),'image/gif')
#        self.assertEqual((atphoto.getWidth(scale='full'),atphoto.getHeight(scale='full')),(20,17))
#        pngphoto = atphoto._exportPIL('PNG',10,10)
#        atphoto.setImage(pngphoto)
#        self.assertEqual(atphoto.get_content_type(),'image/png')
#        self.assertEqual(atphoto.getWidth(scale='full'),10)


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
        mtr = self.portal.mimetypes_registry
        atphoto = self.createATPhoto('canoneye.jpg')

        newname,gifphoto = atphoto.exportImage('GIF',100,100,0)
        self.assertEqual(mtr.classify(str(gifphoto)),'image/gif')

        newname,bmpphoto = atphoto.exportImage('PNG',100,100,0)
        self.assertEqual(mtr.classify(str(bmpphoto)),'image/png')

        newname,tiffphoto = atphoto.exportImage('TIFF',100,100,0)
        self.assertEqual(mtr.classify(str(tiffphoto)),'image/tiff')

        newname,zipphoto = atphoto.exportImage('ZIP',100,100,1)
        self.assertEqual(mtr.classify(str(zipphoto)),'application/zip')


    # from class ATPhotoTransform:
    def test_exportFlickr(self):
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
        atphoto = self.createATPhoto('canoneye.jpg')
        #print atphoto.exportImage('GIF')
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

    def test_getFlickrIdAndUrl(self):
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
    suite.addTest(makeSuite(testATPhotoTransform))
    return suite

##code-section module-footer #fill in your manual code here
##/code-section module-footer


if __name__ == '__main__':
    framework()


