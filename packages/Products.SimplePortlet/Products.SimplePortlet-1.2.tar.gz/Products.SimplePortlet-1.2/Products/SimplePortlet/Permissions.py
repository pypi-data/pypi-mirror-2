# BBB for CMF < 2.1
try:
    from Products.CMFCore.permissions import setDefaultRoles
except ImportError:
    from Products.CMFCore.CMFCorePermissions import setDefaultRoles

# Add a Portlet
ADD_CONTENTS_PERMISSION = 'SimplePortlet: Add Portlet'
MANAGE_LAYOUT_PERMISSION = 'SimplePortlet: Manage Portlet Layout'

setDefaultRoles(ADD_CONTENTS_PERMISSION, ('Manager', 'Owner', ))
setDefaultRoles(MANAGE_LAYOUT_PERMISSION, ('Manager', 'Owner', ))
