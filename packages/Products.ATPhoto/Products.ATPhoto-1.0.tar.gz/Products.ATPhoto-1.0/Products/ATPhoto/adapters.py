# -*- coding: utf-8 -*-
from Acquisition import aq_inner, aq_parent
from zExceptions import BadRequest
from Products.CMFCore.utils import getToolByName
from ATPhoto import ATPhoto_schema
from cStringIO import StringIO
from zipfile import ZipFile

from DocumentTemplate import sequence

from zope.interface import implements
from zope.app import zapi

from OFS.IOrderSupport import IOrderedContainer

from interfaces import IPhoto, IPhotoAlbum
from interfaces import IScalable, ISlideShow, IPossibleScalable
from interfaces import IZippable, ISortable

import random
import zLOG

AVAILABLE_SIZES = ATPhoto_schema.get('image').sizes.keys()

# Format strings into something that can be parsed as
# javascript.  Be warned that this logic right now is quite
# fragile (ie doesn't take into account non-ascii chars, etc)...
# but previously didn't take care of newlines - Rocky
def js_format(orig):
    formatted = ''
    for c in orig:
        if c == "\r":
            c = ''
        elif c == "\n":
            c = "\\n"
        elif c == "'":
            c = "\\'"
        formatted += c
    return formatted

class Zippable(object):
    """
    store your files in a zip file
    """
    implements(IZippable)

    _zip = None
    sIO = None

    def __init__(self,context):
        self.context = context
        self.initIO()

    def initIO(self):
        """
        reinit the Zip IO
        """
        self.sIO = StringIO()
        self._zip = ZipFile(self.sIO,"w",8)

    def getZippable(self):
        self.context

    def setFile(self,filename,data):
        """
        store the file inside the zip file
        """
        if(self._zip):
            self._zip.writestr(filename,str(data))
        else:
            raise BadRequest,"Unitialized Zip file"

    def setZip(self):
        """
        initialize the zipe file
        """
        self._zip = ZipFile(self.sIO,"w",8)

    def closeZip(self):
        """
        close the zip file
        """
        self._zip.close()

    def getZip(self):
        """
        get the zip file object
        """
        if(self.sIO):
            self.closeZip()
            zip = ZipFile(self.sIO,'r')
            self.setZip()
            return zip

    def getRawZip(self):
        """
        return the raw zip file
        """
        if(self._zip):
            self.closeZip()
            value = self.sIO.getvalue()
            self.setZip()
            return value
        else:
            raise BadRequest,"Unitialized Zip file"

class Sortable(object):
    """
    sort objects in a container object
    """
    implements(ISortable)

    def __init__(self,context):
        if IOrderedContainer.isImplementedBy(context):
            self.context = context
        else:
            raise 'Object must implement IOrderedContainer'

    def sort(self, key, reverse=0,caseinsensitive=0):
        """
        if no key use the last sortKey in object
        """
        sortFunc = 'cmp'
        if caseinsensitive:
            sortFunc = 'nocase'

        ids = [ id for id, obj in sequence.sort( self.context.objectItems(),( (key, sortFunc, 'asc'), ) ) ]
        if reverse:
            ids.reverse()
        self.context.moveObjectsByDelta( ids, -len(self.context.objectItems()) )
        self.reindexObjects()


    def reindexObjects(self):
        for obj in self.context.objectValues():
            obj.reindexObject()

    def sortReverse(self):
        ids = self.context.objectIds()
        ids.reverse()
        self.context.moveObjectsByDelta( ids, -len(ids) )
        self.reindexObjects()

    def sortExifDateTime(self):
        return self.sort('getEXIFOrigDate')


class Scalable(object):
    """
    object with scalable image
    """
    implements(IScalable)

    field = 'image'
    def __init__(self,context):
        self.context = context

    def getScalable(self):
        """
        return the scalable object himself
        """
        return self.context

    def getScale(self,scale=None):
        """
        return scaled image
        """
        if IPossibleScalable.providedBy(self.context) and self.field:
            field = self.context.getField(self.field)
            if scale is None or scale in field.getAvailableSizes(self.context):
                image = field.getScale(self.context, scale=scale)
            if image is not None and not isinstance(image, basestring):
                return image
        return ''

    def tag(self,**kwargs):
        """
        return image tag
        """
        if IPossibleScalable.providedBy(self.context) and self.field:
            context = aq_inner(self.context)
            field = context.getField(self.field)
            tag = field.tag(context, **kwargs)
            if kwargs.get('force_refresh',False):
                random.seed()
                overide = '?random_refresh=%i" alt="'  % random.randint(0,100)
                tag = tag.replace('" alt="',overide)
            zLOG.LOG('ATPhoto', zLOG.INFO, '', tag)
            return tag
        return ''
            
class ScalableFolder(Scalable):
    """
    folderish object with scalable image
    """
    implements(IScalable)
    
    meta_types = ['ATPhoto']

    def __init__(self,container):
        context = None
        container = aq_inner(container)
        try:
            context = container.getSymbolic_photo()
        except AttributeError:
            pass
        if not context and self.meta_types:
            pc = getToolByName(container,'portal_catalog',None)
            if pc:
                brains = pc.searchResults(meta_type=self.meta_types,
                                          path='/'.join(container.getPhysicalPath()),
                                          limit=1)
                if brains:
                    context = brains[0].getObject()
        self.context = context

class SlideShow(object):
    """
    adapter to provide some js stuff
    """
    implements(ISlideShow)
    
    def __init__(self,context):
        self.context = context

    def getContents(self):
        context = self.context
        if context.isPrincipiaFolderish:
            container = aq_inner(context)
            b_start = 0
        else:
            container = aq_parent(aq_inner(context))
            b_start = context.getObjPositionInParent()

        batch = container.getFolderContents()

        sizes = AVAILABLE_SIZES

        # js structure
        Context = "function getContext() { context = new BaseContent('%s'"+",'%s'"*8+"); }\n"
        BaseContent = "    photo = new BaseContent('%s'"+",'%s'"*8+");\n"
        Photo = "    ATPhoto(photo,%i,'%s');\n"
        PhotoSizes = "    photo.setSize('%s',%i,%i,'%s');\n"

        
        out = [Context % (context.absolute_url(), 'id',
                          'title', 'description',
                          context.meta_type,
                          context.portal_type,
                          context.isPrincipiaFolderish in (True,1) and 'true' or 'false',
                          'published','n/a')]

        out.append('''
var b_start = %s;
function getSlideShowContents(show_folderish) {
    var photo;
''' % (b_start,))

        # create a js object for each batch item
        i = 0
        for p in batch:
            obj = p.getObject()
            if IPossibleScalable.providedBy(obj):
                photo = IScalable(obj).getScalable()
            else:
                continue
            # init BaseContent
            title = p.Title or p.getId
            url = p.getURL()
            out.append(BaseContent % (url, p.getId,
                                title.replace("'","\\\'"),
                                js_format(p.Description),
                                p.meta_type,
                                p.Type,
                                p.is_folderish == True and 'true' or 'false',
                                p.review_state,
                                p.getObjSize or 'n/a'))
            # init Photo object
            out.append(Photo % (i,photo.content_type))
            # adding scales
            
            out.extend([ PhotoSizes % (scale,
                                       photo.getWidth(scale=scale),
                                       photo.getHeight(scale=scale),
                                       '%s/image_%s' % (url,scale)) for scale in sizes])
            # add to js batch
            out.append('    if ( !photo.is_folderish || (show_folderish && photo.is_folderish) ) { Batch.additem(photo); };\n')

            i = i+1

        out.append('}\n')

        return ''.join(out)

