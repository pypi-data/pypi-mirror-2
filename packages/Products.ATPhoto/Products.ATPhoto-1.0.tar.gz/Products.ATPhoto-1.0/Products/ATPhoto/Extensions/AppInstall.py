from StringIO import StringIO
from Products.CMFCore.utils import getToolByName

STYLESHEETS = (
        {'id': 'atphoto.css', 'media': "all", 'rendering': 'import','cookable': True},
)
JAVASCRIPTS = (
        {'id': 'batch.js',
         'expression': "python: object.meta_type in ('ATPhoto', 'ATPhotoAlbum') and 1",
         'cookable': True,
        },
        {'id': 'atphoto_transitions.js',
         'expression': "python: object.meta_type in ('ATPhoto', 'ATPhotoAlbum') and 2",
         'cookable': True,
        },
        {'id': 'atphoto.js',
         'expression': "python: object.meta_type in ('ATPhoto', 'ATPhotoAlbum') and 3",
         'cookable': True,
        },
        {'id': 'atphotoalbum.js',
         'expression': "python: object.meta_type in ('ATPhotoAlbum',) and 4",
         'cookable': True,
        },
        {'id': 'atslideshow.js',
         'expression': "python: object.meta_type in ('ATPhoto', 'ATPhotoAlbum') and 5",
         'cookable': True,
        },
)

def install(self):
    # add ATPhoto to typesUseViewActionInListings
    stp = getToolByName(self, 'portal_properties').site_properties
    typesUserViewActionInListings = stp.getProperty('typesUseViewActionInListings') 
    if typesUserViewActionInListings:
        view_action_types = list(typesUserViewActionInListings)
        if(not 'ATPhoto' in view_action_types):
           view_action_types.append('ATPhoto')
        view_action_types = tuple(view_action_types)
        stp._updateProperty('typesUseViewActionInListings',view_action_types)

    # hide ATPhoto from nav
    navtree_properties = getToolByName(self, 'portal_properties').navtree_properties
    metaTypesNotToList = list(navtree_properties.getProperty('metaTypesNotToList'))
    if 'ATPhoto' not in metaTypesNotToList:
        metaTypesNotToList.append('ATPhoto')
        navtree_properties._updateProperty('metaTypesNotToList',metaTypesNotToList)
        
    # intall portal actions
    at=getToolByName(self, 'portal_actions')
    actions = at.listActions()
    PloneJUploadAction = [n for n in range(len(actions)) if actions[n].getId()=='PloneJupload']
    if PloneJUploadAction:
        at.deleteActions(selections=PloneJUploadAction)
        at.addAction( id='PloneJupload',
                     name='Upload Files',
                     action='string:${folder_url}/PloneJUpload_view',
                     condition="python:object.meta_type!='ATPhotoAlbum'",
                     permission='Add portal content',
                     category='folder',
                    visible=1 )
    # our actions
    at.addAction('auto_rotate',
                name='Auto rotate',
                action='string:$object_url/autoTransformImage',
                condition="python:object.meta_type in ['ATPhoto','ATPhotoAlbum']",
                permission='Modify portal content',
                category='object_buttons')
    at.addAction('rotate_270',
                name='Rotate 90 clockwise',
                action='string:$object_url/transformImage?method=4',
                condition="python:object.meta_type=='ATPhoto'",
                permission='Modify portal content',
                category='object_buttons')
    at.addAction('rotate_90',
                name='Rotate 90 counterclockwise',
                action='string:$object_url/transformImage?method=2',
                condition="python:object.meta_type=='ATPhoto'",
                permission='Modify portal content',
                category='object_buttons')
    at.addAction('rotate_180',
                name='Rotate 180',
                action='string:$object_url/transformImage?method=3',
                condition="python:object.meta_type=='ATPhoto'",
                permission='Modify portal content',
                category='object_buttons')
    at.addAction('flip_left_right',
                name='Flip around vertical axis',
                action='string:$object_url/transformImage?method=0',
                condition="python:object.meta_type=='ATPhoto'",
                permission='Modify portal content',
                category='object_buttons')
    at.addAction('flip_top_bottom',
                name='Flip around horizontal axis',
                action='string:$object_url/transformImage?method=1',
                condition="python:object.meta_type=='ATPhoto'",
                permission='Modify portal content',
                category='object_buttons')
    at.addAction('set_as_symbolic',
                name='Set as symbolic photo',
                action='string:$object_url/setSymbolic',
                condition="python:object.meta_type=='ATPhoto' and folder.meta_type=='ATPhotoAlbum'",
                permission='Modify portal content',
                category='object_buttons')
    at.addAction('sort_by_id',
                name='Sort By Id',
                action='string:$object_url/sortById',
                condition="python:object.meta_type=='ATPhotoAlbum'",
                permission='Modify portal content',
                category='object_buttons')
    at.addAction('sort_by_exifdatetime',
                name='Sort By EXIF DateTime',
                action='string:$object_url/sortByExifDateTime',
                condition="python:object.meta_type=='ATPhotoAlbum'",
                permission='Modify portal content',
                category='object_buttons')
    at.addAction('reverse_sort',
                name='Reverse actual sort',
                action='string:$object_url/sortReverse',
                condition="python:object.meta_type=='ATPhotoAlbum'",
                permission='Modify portal content',
                category='object_buttons')


    # register in content type registry

    #pr = getToolByName(self, 'content_type_registry')
    #pr.updatePredicate(predicate=pr.getPredicate('image'),predicate_id='image',typeObjectName='ATPhoto')
    #pr.updatePredicate(predicate=pr.getPredicate('ATImage_ext'),predicate_id='ATImage_ext',typeObjectName='ATPhoto')



    # installing CSS
    csstool = getToolByName(self, 'portal_css')
    for css in STYLESHEETS:
        csstool.registerStylesheet(**css)

    # installing JS
    jstool = getToolByName(self, 'portal_javascripts')
    for js in JAVASCRIPTS:
        jstool.registerScript(**js)

    # installing new transform
    from Products.ATPhoto.transforms.image_to_gif import image_to_gif
    from Products.ATPhoto.transforms.image_to_png import image_to_png
    from Products.ATPhoto.transforms.image_to_jpeg import image_to_jpeg
    from Products.ATPhoto.transforms.image_to_bmp import image_to_bmp
    from Products.ATPhoto.transforms.image_to_pcx import image_to_pcx
    from Products.ATPhoto.transforms.image_to_ppm import image_to_ppm
    from Products.ATPhoto.transforms.image_to_tiff import image_to_tiff


    transformtool = getToolByName(self, 'portal_transforms')
    transformtool.registerTransform(image_to_png())
    transformtool.registerTransform(image_to_gif())
    transformtool.registerTransform(image_to_bmp())
    transformtool.registerTransform(image_to_jpeg())
    transformtool.registerTransform(image_to_pcx())
    transformtool.registerTransform(image_to_tiff())
    transformtool.registerTransform(image_to_ppm())


    return 'Custom Properties changed'

def uninstall(self):
    
    # remove ATPhoto from typesUseViewActionInListings
    stp = getToolByName(self, 'portal_properties').site_properties
    view_action_types = list(stp.getProperty('typesUseViewActionInListings'))
    view_action_types.remove('ATPhoto')
    view_action_types = tuple(view_action_types)
    stp._updateProperty('typesUseViewActionInListings',view_action_types)

    # remove ATPhoto from metaTypesNotToList
    navtree_properties = getToolByName(self, 'portal_properties').navtree_properties
    metaTypesNotToList = list(navtree_properties.getProperty('metaTypesNotToList'))
    if 'ATPhoto' in metaTypesNotToList:
        metaTypesNotToList.remove('ATPhoto')
        navtree_properties._updateProperty('metaTypesNotToList',metaTypesNotToList)
    
    # remove actions
    at=getToolByName(self, 'portal_actions')
    list_cpt = []
    cpt = 0
    list_id = ['rotate_90','rotate_180','rotate_270','flip_top_bottom','flip_left_right','auto_rotate','set_as_symbolic','sort_by_id','sort_by_exifdatetime','reverse_sort']
    for action in at.listActions():
        if action.getId() in list_id:
            list_cpt.append(cpt)
        cpt += 1
    at.deleteActions(list_cpt)
    #### remove our modified PloneJUpload action and get back to normal one
    actions = at.listActions()
    PloneJUploadAction = [n for n in range(len(actions)) if actions[n].getId()=='PloneJupload']
    if PloneJUploadAction:
        at.deleteActions(selections=PloneJUploadAction)
        at.addAction( id='PloneJupload',
                     name='Upload Files',
                     action='string:${folder_url}/PloneJUpload_view',
                     condition="",
                     permission='Add portal content',
                     category='folder',
                    visible=1 )

    ### remove our transforms
    transformtool = getToolByName(self, 'portal_transforms')
    installedTransforms = transformtool.objectIds()
    atphoto_transforms = ['image_to_png','image_to_gif','image_to_bmp','image_to_jpeg','image_to_pcx','image_to_ppm','image_to_tiff']
    for transform in atphoto_transforms:
        if transform in installedTransforms:
            transformtool.unregisterTransform(transform)

    ## remove content registry modifs
    pr = getToolByName(self, 'content_type_registry')
    try:
       pr.updatePredicate(predicate=pr.getPredicate('image'),predicate_id='image',typeObjectName='image')
       pr.updatePredicate(predicate=pr.getPredicate('ATImage_ext'),predicate_id='ATImage_ext',typeObjectName='image')
    except:
       pass



