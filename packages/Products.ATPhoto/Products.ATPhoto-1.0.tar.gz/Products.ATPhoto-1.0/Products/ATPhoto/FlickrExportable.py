# File: FlickrExportable.py
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
from uploadr import Uploadr
##/code-section module-header




class FlickrExportable:
    ''' '''
    __implements__ = ()

    ##code-section class-header_FlickrExportable #fill in your manual code here
    ##/code-section class-header_FlickrExportable




    def isFlickrAuth(self,frob,REQUEST=None):
        """
        """
        if(REQUEST):
            flickrAuth = REQUEST.SESSION.get('flickrAuth',0)
            frob = REQUEST.SESSION.get('frob',0)
        if(not flickrAuth):
            flick = Uploadr(frob=str(frob))
            flickrAuth = flick.getToken()
            flick.checkToken()
            if(REQUEST and flickrAuth):
                REQUEST.SESSION['flickrAuth'] = 1
                token = flick.getTokenValue()
                REQUEST.SESSION['token'] = str(token)
        return flickrAuth


    def getFlickrIdAndUrl(self,REQUEST):
        """
          Generate Frob ID and flickr auth url
          Set them inside the session object
        """
        if(not REQUEST.SESSION.has_key('frob') or REQUEST.has_key('forceNewAuth')):
            flick = Uploadr()
            frob = flick.getFrob()
            url = flick.getAuthKey()
            session = REQUEST.SESSION
            session.set('flickrAuth',0)
            session.set('frob',str(frob))
            session.set('flickrurl',str(url))
        else:
            frob = REQUEST.SESSION.get('frob')
            url = REQUEST.SESSION.get('flickrurl')
        return (frob,url)

    def getFlickrSets(self, frob, token,flickrAuth=False, REQUEST=None):
        url = "%s/atphoto_export?portal_status_message=" % self.absolute_url()
        if(not flickrAuth):
            flickrAuth = REQUEST.SESSION.has_key('flickrAuth')
        if(not frob):
            frob = REQUEST.SESSION.get('frob')
        if(not token):
            token = REQUEST.SESSION.get('token')
        if(flickrAuth):
            flick = Uploadr(frob=str(frob),token=token)
            return flick.getSetList()
        else:
            msg = 'Not Authenticated!'
        target = "%s%s" % (url,msg)
        if(REQUEST):
            REQUEST.RESPONSE.redirect(target)
        else:
            return msg








##code-section module-footer #fill in your manual code here
##/code-section module-footer



