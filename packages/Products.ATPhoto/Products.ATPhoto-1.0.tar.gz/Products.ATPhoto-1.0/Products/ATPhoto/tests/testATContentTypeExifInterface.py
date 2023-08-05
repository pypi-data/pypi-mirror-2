# File: testATContentTypeExifInterface.py
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
from Globals import package_home
from Products.CMFCore.utils import getToolByName

##/code-section module-header

#
# test-cases for class(es) 
#
from Testing import ZopeTestCase
from Products.ATPhoto.tests.testATContentTypeBase import testATContentTypeBase
# import the tested classes

class testATContentTypeExifInterface(testATContentTypeBase):
    """ test-cases for class(es) 
    """

    ##code-section class-header_testATContentTypeExifInterface #fill in your manual code here
    ##/code-section class-header_testATContentTypeExifInterface

    def afterSetUp(self):
        """
        """
        import os
        from Globals import package_home



    # Manually created methods
    def _createType(self, context, portal_type, id, **kwargs):
        """Helper method to create a new type.
        """
        ttool = getToolByName(context, 'portal_types')
        cat = self.portal.portal_catalog
        fti = ttool.getTypeInfo(portal_type)
        fti.constructInstance(context, id, **kwargs)
        obj = getattr(context.aq_inner.aq_explicit, id)
        cat.indexObject(obj)
        return obj

    def createImageFd(self):
        """
        """
        from Products.ATPhoto import config
        imgFile = open(os.path.join(package_home(config.product_globals),'tests','input','canoneye.jpg'), 'rb')
        return imgFile



def test_suite():
    from unittest import TestSuite
    from Testing.ZopeTestCase.zopedoctest import ZopeDocFileSuite

    return TestSuite((
        ZopeDocFileSuite('testATContentTypeExifInterface.txt',
                         package='Products.ATPhoto.doc',
                         test_class=testATContentTypeExifInterface),
    ))


##code-section module-footer #fill in your manual code here
##/code-section module-footer


if __name__ == '__main__':
    framework()


