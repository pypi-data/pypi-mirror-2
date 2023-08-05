# File: testATContentTypeExifPerformance.py
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
# test-cases for class(es) 
#
import os, sys
from Testing import ZopeTestCase
from Products.ATPhoto.tests.testATContentTypeBase import testATContentTypeBase
# import the tested classes

##code-section module-beforeclass #fill in your manual code here
import gc
class a:
    pass
##/code-section module-beforeclass


class testATContentTypeExifPerformance(testATContentTypeBase):
    """ test-cases for class(es) 
    """

    ##code-section class-header_testATContentTypeExifPerformance #fill in your manual code here
    ##/code-section class-header_testATContentTypeExifPerformance

    def afterSetUp(self):
        """
        """
    # Manually created methods

    def test_amountOfCreatedObject(self):
        """
        """
        gc.enable()
        i = len(gc.get_objects())
        print i
        a()
        self.assertEquals(i+1,len(gc.get_objects()))
        gc.disable()


    def test_amountOfCreatedObjectWithExif(self):
        """
        """
        gc.enable()
        before = len(gc.get_objects())
        print "%s objects before exif parsing" % before
        atphoto = self.createATPhoto('canoneye.jpg')
        after = len(gc.get_objects())
        print "%s objects after exif parsing" % after
        gc.disable()
        total = after - before
        print "%s objects created." % total
        self.failUnless(total < 1812)



    # Manually created methods

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testATContentTypeExifPerformance))
    return suite

##code-section module-footer #fill in your manual code here
##/code-section module-footer


if __name__ == '__main__':
    framework()


