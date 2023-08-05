from Products.Archetypes.public import listTypes
from Products.Archetypes.Extensions.utils import installTypes, install_subskin
from Products.CMFCore.utils import getToolByName
from StringIO import StringIO
from Acquisition import aq_base
# BBB for CMF < 2.1
try:
    from Products.CMFCore.permissions import setDefaultRoles
except ImportError:
    from Products.CMFCore.CMFCorePermissions import setDefaultRoles

from Products.SimplePortlet.config import *
import re

try:
    from Products.CMFDynamicViewFTI.migrate import migrateFTIs
    PRE_PLONE3 = True
except ImportError:   #CMF 2.1 or later
    PRE_PLONE3 = False


def install(self):
    out = StringIO()

    installTypes(self, out,
                 listTypes(PROJECTNAME),
                 PROJECTNAME)

    install_subskin(self, out, GLOBALS)

    if PRE_PLONE3:
        # Migrate FTI, to make sure we get the necessary infrastructure for the
        # 'display' menu to work.
        migrated = migrateFTIs(self, product=PROJECTNAME)
        print >>out, "Switched to DynamicViewFTI: %s" % ', '.join(migrated)

    # install slots
    slotpath='here/portlet_simpleportlet/macros/'

    # Enable portal_factory
    factory = getToolByName(self, 'portal_factory')
    types = factory.getFactoryTypes().keys()
    if 'Portlet' not in types:
        types.append('Portlet')
        factory.manage_setPortalFactoryTypes(listOfTypeIds = types)
    if 'TopicPortlet' not in types:
        types.append('TopicPortlet')
        factory.manage_setPortalFactoryTypes(listOfTypeIds = types)
    if 'RSSPortlet' not in types:
        types.append('RSSPortlet')
        factory.manage_setPortalFactoryTypes(listOfTypeIds = types)

    #create the tool instance
    portal = getToolByName(self, 'portal_url').getPortalObject()

    if not hasattr(self, 'portlet_manager'):
        addTool = portal.manage_addProduct['SimplePortlet'].manage_addTool
        addTool(type='SimplePortlet tool')

    at=getToolByName(self, 'portal_actions')

    if 'portlets' not in [action.id for action in at.listActions()]:
        at.addAction('portlets', 'Portlets', 'string: ${folder_url}/portlet_setup', 'python: portal.plone_utils.isDefaultPage(object) or object is folder', 'SimplePortlet: Manage Portlet Layout','object')

    try:
        if not slotpath + 'portlet_left' in portal.left_slots:
            portal.left_slots = list(portal.left_slots) + [slotpath+'portlet_left', ]
        if not slotpath + 'portlet_right' in portal.right_slots:
            portal.right_slots = list(portal.right_slots) + [slotpath+'portlet_right', ]
    except:
        pass

    # collect existing non-standard plone portlets
    additionalPortlets = extractExistingPortlets(self)

    # try to add them to the portlet_tool
    for p in additionalPortlets.keys():
        self.portlet_manager.registerPortlet(p, additionalPortlets[p])

    print >> out, "Successfully installed %s." % PROJECTNAME
    return out.getvalue()


def uninstall(self):
    # remove the references in each folder to our portlet:
    portal = getToolByName(self, 'portal_url').getPortalObject()

    request = self.REQUEST
    url = request.get('URL', request.get('ACTUAL_URL', None))
    # on reinstall do nothing
    if not url.endswith('reinstallProducts'):
        processObject(aq_base(portal))
        processFolderish(portal)


def processFolderish(folder):
    for obj in folder.contentValues():
        unwrapped = aq_base(obj)
        if unwrapped.isPrincipiaFolderish and unwrapped.meta_type!='CMF Collector':
            processObject(unwrapped)
            processFolderish(obj)


def processObject(object):
    if hasattr(object, 'left_slots'):
        slots = list(getattr(object, 'left_slots', []))
        try:
            slots.remove('here/portlet_simpleportlet/macros/portlet_left')
        except:
            pass

        try:
            slots.remove('here/portlet_simpleportlet/macros/portlet_right')
        except:
            pass
        object.left_slots=slots

    if hasattr(object, 'right_slots'):
        slots = list(getattr(object, 'right_slots', []))
        try:
            slots.remove('here/portlet_simpleportlet/macros/portlet_left')
        except:
            pass

        try:
            slots.remove('here/portlet_simpleportlet/macros/portlet_right')
        except:
            pass
        object.right_slots=slots


def makeValidPropertyId(id):
    """
    mangle the given string so that it is a valid property id
    """
    while id[:1] == '_':
        id = id[1:]
    while id.startswith('aq_'):
        id = id[3:]
    return re.sub(r'[\s&<>]', '_', id)


def extractExistingPortlets(self):
    """
    when SP is installed, it scans all folderish objects and
    collects all the existing portlets and tries to come up
    with friendly names so that they can be entered into the portlet_tool
    """
    portlets=[]
    portal = getToolByName(self, 'portal_url').getPortalObject()

    portlets=portlets + collectPortlets(aq_base(portal))

    portlets = portlets + processFolderishForPortlets(portal)

    standardPortlets= ['here/portlet_navigation/macros/portlet',
        'here/portlet_login/macros/portlet',
        'here/portlet_favorites/macros/portlet',
        'here/portlet_simpleportlet/macros/portlet_left',
        'here/portlet_simpleportlet/macros/portlet_right',
        'here/portlet_calendar/macros/portlet',
        'here/portlet_review/macros/portlet',
        'here/portlet_related/macros/portlet',
        'here/portlet_recent/macros/portlet',
        'here/portlet_news/macros/portlet',
        'here/portlet_events/macros/portlet',
        '']

    filteredPortlets=[]
    for p in portlets:
        if not p in standardPortlets:
            if p not in filteredPortlets:
                filteredPortlets.append(p)

    # now we have the portlets that need to be processed further
    processedPortlets={}

    for p in filteredPortlets:
        # p is usually of the form here/<filename>/macros/<macro name>
        # but it can also be here/<path>/<to>/<template>
        # try to come up with a friendly name

        parts = p.split("/")

        if parts[-1]!='portlet':
            friendlyName = makeValidPropertyId(parts[-1])
            if processedPortlets.has_key(friendlyName) and parts[-2] == 'macros':
                friendlyName = makeValidPropertyId(parts[-3] + '_' + parts[-1])
        else:
            friendlyName = makeValidPropertyId(parts[-3])

        # In case there are still name clashes, append a number to the id to
        # guarantee uniqueness (e.g. myportlet, myportlet2, myportlet3...)
        n = 2
        origFriendlyName = friendlyName
        while processedPortlets.has_key(friendlyName):
            friendlyName = origFriendlyName + str(n)
            n += 1

        processedPortlets[friendlyName]=p

    return processedPortlets


def collectPortlets(object):
    portlets=[]
    if hasattr(object, 'left_slots'):
        portlets = portlets + list(getattr(object, 'left_slots', []))
    if hasattr(object, 'right_slots'):
        portlets = portlets + list(getattr(object, 'right_slots', []))

    return portlets


def processFolderishForPortlets(folder):
    portlets=[]
    for obj in folder.contentValues():
        unwrapped = aq_base(obj)
        if unwrapped.isPrincipiaFolderish and unwrapped.meta_type!='CMF Collector':
            portlets = portlets + collectPortlets(unwrapped)
            portlets = portlets + processFolderishForPortlets(obj)

    return portlets
