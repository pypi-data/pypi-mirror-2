from Globals import package_home
from Products.Archetypes.public import process_types, listTypes
from Products.CMFCore import utils
from Products.CMFCore.DirectoryView import registerDirectory
import os, os.path, sys
import content
from config import SKINS_DIR, GLOBALS, PROJECTNAME
from config import ADD_CONTENTS_PERMISSION

from Globals import InitializeClass

# Module aliases - we don't always get it right on the first try, but and we
# can't move modules around because things are stored in the ZODB with the
# full module path. However, we can create aliases for backwards compatability.
sys.modules['Products.SimplePortlet.Portlet'] = content.portlet
sys.modules['Products.SimplePortlet.TopicPortlet'] = content.topicportlet
sys.modules['Products.SimplePortlet.CMFSinPortlet'] = content.cmfsinportlet

HAS_CMFSIN = True

try:
    from Products import CMFSin
except:
    HAS_CMFSIN = False


registerDirectory(SKINS_DIR, GLOBALS)


def initialize(context):
    ##Import Types here to register them
    from content import Portlet
    from content import TopicPortlet
    
    if HAS_CMFSIN:
        from content import CMFSinPortlet
    
    content_types, constructors, ftis = process_types(
        listTypes(PROJECTNAME),
        PROJECTNAME)
    
    utils.ContentInit(
        PROJECTNAME + ' Content',
        content_types      = content_types,
        permission         = ADD_CONTENTS_PERMISSION,
        extra_constructors = constructors,
        fti                = ftis,
        ).initialize(context)
    
    from SimplePortletTool import SimplePortletTool
    utils.ToolInit(
        'SimplePortlet tool', 
        tools=(SimplePortletTool,),  
        icon='tool.gif', ).initialize(context)
