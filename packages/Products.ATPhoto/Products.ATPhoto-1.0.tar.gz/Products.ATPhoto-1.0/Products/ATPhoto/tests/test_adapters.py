# -*- coding: utf-8 -*-

import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))
from Testing import ZopeTestCase
ZopeTestCase.installProduct('Five')

def test_adapters():
    """
    >>> #import Products.Five
    >>> #from Products.Five import zcml
    >>> #from zope.app.tests.placelesssetup import setUp, tearDown
    >>> #setUp()
    >>> #import Products.ATPhoto
    >>> #zcml.load_config('meta.zcml', Products.Five)
    >>> #zcml.load_config('permissions.zcml', Products.Five)
    >>> #zcml.load_config('configure.zcml', Products.ATPhoto)

        test content

    >>> from Products.ATPhoto.ATPhotoAlbum import ATPhotoAlbum
    >>> album = ATPhotoAlbum('test_photo')
    >>> from Products.ATPhoto.ATPhoto import ATPhoto
    >>> photo = ATPhoto('test_photo')

        test scalable adapter

    >>> from Products.ATPhoto.adapters import Scalable
    >>> from Products.ATPhoto.interfaces import IScalable
    >>> adapted = IScalable(photo)
    >>> IScalable.providedBy(adapted)
    True
    >>> adapted.tag()
    '<img src="/image" alt="" title="" height="0" width="0" />'
    >>> adapted.tag(scale='thumb')
    '<img src="/image_thumb" alt="" title="" height="0" width="0" />'
    >>> adapted.tag() == adapted.tag(force_refresh=True)
    False
    >>> adapted = IScalable(album)
    >>> IScalable.providedBy(adapted)
    True
    >>> adapted.tag()
    ''

        test slideshow adapter

    >>> from Products.ATPhoto.adapters import SlideShow
    >>> from Products.ATPhoto.interfaces import ISlideShow
    >>> adapted = ISlideShow(photo)
    >>> ISlideShow.providedBy(adapted)
    True
    >>> adapted = ISlideShow(album)
    >>> ISlideShow.providedBy(adapted)
    True

        test zippable adapter

    >>> from Products.ATPhoto.adapters import Zippable
    >>> from Products.ATPhoto.interfaces import IZippable
    >>> adapted = IZippable(album)
    >>> IZippable.providedBy(adapted)
    True
    >>> adapted.setZip()
    >>> adapted.setFile('file1','xaedata1')
    >>> adapted.setFile('file2','xaedata2')
    >>> zip = adapted.getZip()
    >>> zip.namelist()
    ['file1', 'file2']
    >>> zip.read('file1')
    'xaedata1'
    >>> zip.read('file2')
    'xaedata2'
    >>> adapted.initIO()
    >>> zip = adapted.getZip()
    >>> zip.namelist()
    []
    >>> adapted.setFile('file3','xaedata3')
    >>> zip = adapted.getZip()
    >>> zip.namelist()
    ['file3']

        test sortable adapter

    >>> from Products.ATPhoto.adapters import Sortable
    >>> from Products.ATPhoto.interfaces import ISortable
    >>> adapted = ISortable(album)


    """



def test_suite():
    from Testing.ZopeTestCase import ZopeDocTestSuite
    return ZopeDocTestSuite()

if __name__ == '__main__':
    framework()

