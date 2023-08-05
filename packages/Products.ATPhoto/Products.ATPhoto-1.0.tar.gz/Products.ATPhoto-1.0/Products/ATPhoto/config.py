#
# Product configuration. This contents of this module will be imported into
# __init__.py and every content type module.
#
# If you wish to perform custom configuration, you may put a file AppConfig.py
# in your product's root directory. This will be included in this file if
# found.
#
#from Products.CMFCore.CMFCorePermissions import setDefaultRoles
try:
    from Products.CMFCore.permissions import setDefaultRoles
except ImportError:
    from Products.CMFCore.CMFCorePermissions import setDefaultRoles

PROJECTNAME = "ATPhoto"

# Check for Plone 2.1
try:
    from Products.CMFPlone.migrations import v2_1
except ImportError:
    HAS_PLONE21 = False
else:
    HAS_PLONE21 = True
    
# Permissions
DEFAULT_ADD_CONTENT_PERMISSION = "Add portal content"
setDefaultRoles(DEFAULT_ADD_CONTENT_PERMISSION, ('Manager', 'Owner'))

product_globals=globals()

# Dependencies of Products to be installed by quick-installer
# override in custom configuration
DEPENDENCIES = []

# Dependend products - not quick-installed - used in testcase
# override in custom configuration
PRODUCT_DEPENDENCIES = []

# You can overwrite these two in an AppConfig.py:
# STYLESHEETS = [{'id': 'my_global_stylesheet.css'},
#                {'id': 'my_contenttype.css',
#                 'expression': 'python:object.getTypeInfo().getId() == "MyType"}]
# You can do the same with JAVASCRIPTS.
STYLESHEETS = []
JAVASCRIPTS = []

##code-section config-bottom #fill in your manual code here
##/code-section config-bottom


# load custom configuration not managed by ArchGenXML
try:
    from Products.ATPhoto.AppConfig import *
except ImportError:
    pass

FS_STORAGE = False

# End of config.py
