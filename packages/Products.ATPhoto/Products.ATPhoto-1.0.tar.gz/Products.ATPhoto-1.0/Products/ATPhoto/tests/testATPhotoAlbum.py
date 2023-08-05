# File: testATPhotoAlbum.py
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
# test-cases for class(es) ATPhotoAlbum
#
import os, sys
from Testing import ZopeTestCase
from Products.ATPhoto.tests.testATContentTypeBase import testATContentTypeBase
# import the tested classes
from Products.ATPhoto.ATPhotoAlbum import ATPhotoAlbum
from Products.ATPhoto.interfaces import ISortable
from Globals import package_home
from Products.ATPhoto import config
from cStringIO import StringIO
from dummy import FileUpload

##code-section module-beforeclass #fill in your manual code here
##/code-section module-beforeclass


class testATPhotoAlbum(testATContentTypeBase):
    """ test-cases for class(es) ATPhotoAlbum
    """

    ##code-section class-header_testATPhotoAlbum #fill in your manual code here
    ##/code-section class-header_testATPhotoAlbum

    def afterSetUp(self):
        """
        """
        self.folder.invokeFactory(type_name="ATPhotoAlbum", id="photoalbum")
        self.pha = getattr(self.folder,"photoalbum")

    def testSortAdapter(self):
        """
        """
        self.pha.invokeFactory(type_name="ATPhoto", id="foo1", title="title1")
        self.pha.invokeFactory(type_name="ATPhoto", id="Foo2", title="title2")
        adapted = ISortable(self.pha)

        ## case is NOT important here
        adapted.sort('id', reverse=0, caseinsensitive=1)
        self.assertEqual(self.pha.objectIds(),['foo1','Foo2'])

        adapted.sort('id', reverse=1, caseinsensitive=1)
        self.assertEqual(self.pha.objectIds(),['Foo2','foo1'])

        ## yet we care about case
        adapted.sort('id', reverse=0, caseinsensitive=0)
        self.assertEqual(self.pha.objectIds(),['Foo2','foo1'])

        adapted.sort('id', reverse=1, caseinsensitive=0)
        self.assertEqual(self.pha.objectIds(),['foo1','Foo2'])

        adapted.sort('title', reverse=1)
        self.assertEqual(self.pha.objectIds(),['Foo2','foo1'])

        adapted.sortReverse()
        self.assertEqual(self.pha.objectIds(),['foo1','Foo2'])

        foo1 = getattr(self.pha,"foo1")
        Foo2 = getattr(self.pha,"Foo2")
        foo1._image_exif['EXIF DateTimeOriginal'] = '2005:12:21 06:51:06'
        Foo2._image_exif['EXIF DateTimeOriginal'] = '2004:12:21 06:51:06'
        adapted.sortExifDateTime()

        self.assertEqual(self.pha.objectIds(),['Foo2','foo1'])

        Foo2._image_exif['EXIF DateTimeOriginal'] = '2005:12:21 06:51:06'
        foo1._image_exif['EXIF DateTimeOriginal'] = '2004:12:21 06:51:06'
        adapted.sortExifDateTime()

        self.assertEqual(self.pha.objectIds(),['foo1','Foo2'])
        adapted.sortReverse()
        self.assertEqual(self.pha.objectIds(),['Foo2','foo1'])





    # from class ATPhotoAlbum:
    def test_view(self):
        """
        """
        #Uncomment one of the following lines as needed
        ##self.loginAsPortalOwner()
        ##o=ATPhotoAlbum('temp_ATPhotoAlbum')
        ##self.folder._setObject('temp_ATPhotoAlbum', o)
        pass


    # from class ATPhotoAlbum:
    def test_export(self):
        """
        """
        #Uncomment one of the following lines as needed
        ##self.loginAsPortalOwner()
        ##o=ATPhotoAlbum('temp_ATPhotoAlbum')
        ##self.folder._setObject('temp_ATPhotoAlbum', o)
        pass

    def importTest(self,file):
        """
        """
        result = self.pha.importPhotos(zipFile=file)
        self.assertEqual(result,'Imported 2 photos from file')
        photoIds = self.pha.objectIds()
        photoIds.sort()
        self.assertEqual(photoIds,['pict0199.jpg','pict1640.jpg'])
        photo1 = getattr(self.pha,'pict1640.jpg')
        self.assertEqual(photo1.getSize(),(25,19))
        self.assertEqual(photo1.size(),16701)
        print photo1.getObjSize()

    # from class ATPhotoAlbum:
    def test_importZip(self):
        """
        """
        ### testing with zipfile
        zipFile = open(os.path.join(package_home(config.product_globals),'tests','input','marie.zip'), 'rb')
        file = FileUpload(filename='marie.zip',file=zipFile)
        self.importTest(file)

    def test_importBz2(self):

        ### testing with bz2
        bz2File = open(os.path.join(package_home(config.product_globals),'tests','input','marie.tar.bz2'), 'rb')
        file = FileUpload(filename='marie.tar.bz2',file=bz2File)
        self.importTest(file)


    # from class ATPhotoAlbum:
    def test_slideshow(self):
        """
        """
        #Uncomment one of the following lines as needed
        ##self.loginAsPortalOwner()
        ##o=ATPhotoAlbum('temp_ATPhotoAlbum')
        ##self.folder._setObject('temp_ATPhotoAlbum', o)
        pass


    # from class ATPhotoAlbum:
    def test_getAvailableSizes(self):
        """
        """
        #Uncomment one of the following lines as needed
        ##self.loginAsPortalOwner()
        ##o=ATPhotoAlbum('temp_ATPhotoAlbum')
        ##self.folder._setObject('temp_ATPhotoAlbum', o)
        pass


    # from class ATPhotoAlbum:
    def test_exportAlbum(self):
        """
        """
        #Uncomment one of the following lines as needed
        ##self.loginAsPortalOwner()
        #o=ATPhotoAlbum('pa')
        #self.folder._setObject('pa', o)
        list = self.pha.listPhotos(basepath='bla',recursive=1)
        self.failUnlessEqual(list,[])

        self.pha.invokeFactory(type_name="ATPhoto", id="foo1")
        self.pha.invokeFactory(type_name="ATPhoto", id="foo2")
        list = self.pha.listPhotos(basepath='bla',recursive=1)
        self.failUnlessEqual(len(list),1)
        self.failUnlessEqual(list[0].has_key('bla/foo1'),True)
        self.failUnlessEqual(list[0].has_key('bla/foo2'),True)

        self.folder.photoalbum.invokeFactory(type_name="ATPhotoAlbum", id="subphotoalbum")
        subpha = getattr(self.folder.photoalbum,"subphotoalbum")
        list = self.pha.listPhotos(basepath='bla',recursive=1)
        self.failUnlessEqual(len(list),1)

        subpha.invokeFactory(type_name="ATPhoto",id="bar1")
        list = self.pha.listPhotos(basepath='bla',recursive=0)
        self.failUnlessEqual(len(list),1)
        list = self.pha.listPhotos(basepath='bla',recursive=1)
        self.failUnlessEqual(len(list),2)
        self.failUnlessEqual(list[0].has_key('bla/subphotoalbum/bar1'),True)
        self.failUnlessEqual(list[1].has_key('bla/foo1'),True)
        self.failUnlessEqual(list[1].has_key('bla/foo2'),True)

        #subpha = getattr(self.folder.photoalbum,"subphotoalbum")
        #print pha.listPhotos(basepath='bla',recursive=1)
        self.folder.photoalbum.subphotoalbum.invokeFactory(type_name="ATPhotoAlbum", id="subsubphotoalbum")
        subsubpha = getattr(self.folder.photoalbum.subphotoalbum,"subsubphotoalbum")
        list = self.pha.listPhotos(basepath='bla',recursive=1)
        self.failUnlessEqual(len(list),2)

        subsubpha.invokeFactory(type_name="ATPhoto",id="bar2")
        list = self.pha.listPhotos(basepath='bla',recursive=1)
        self.failUnlessEqual(len(list),3)
        self.failUnlessEqual(list[0].has_key('bla/subphotoalbum/subsubphotoalbum/bar2'),True)

        list = self.pha.listPhotos(recursive=1)
        self.failUnlessEqual(len(list),3)
        self.failUnlessEqual(list[0].has_key('photoalbum/subphotoalbum/subsubphotoalbum/bar2'),True)
        #pass

    # from class ATPhotoAlbum:
    def test_listPhotos(self):
        """
        """
        #Uncomment one of the following lines as needed
        ##self.loginAsPortalOwner()
        ##o=ATPhotoAlbum('temp_ATPhotoAlbum')
        ##self.folder._setObject('temp_ATPhotoAlbum', o)
        pass


    # from class ATPhotoAlbum:
    def test_exportFlickr(self):
        """
        """
        #Uncomment one of the following lines as needed
        ##self.loginAsPortalOwner()
        ##o=ATPhotoAlbum('temp_ATPhotoAlbum')
        ##self.folder._setObject('temp_ATPhotoAlbum', o)
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
        ##o=FlickrExportable('temp_FlickrExportable')
        ##self.folder._setObject('temp_FlickrExportable', o)
        pass


    # Manually created methods
    def test_getATSlideShowContents(self):
        """
        """
        #Uncomment one of the following lines as needed
        ##self.loginAsPortalOwner()
        ##o=ATPhotoAlbum('temp_ATPhotoAlbum')
        ##self.folder._setObject('temp_ATPhotoAlbum', o)
        pass


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testATPhotoAlbum))
    return suite

##code-section module-footer #fill in your manual code here
##/code-section module-footer


if __name__ == '__main__':
    framework()


