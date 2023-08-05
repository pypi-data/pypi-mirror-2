from Products.CMFCore.utils import UniqueObject
from Acquisition import aq_inner, aq_parent
from Products.CMFCore.utils import getToolByName
from OFS.SimpleItem import SimpleItem
from OFS.PropertyManager import PropertyManager
from Globals import InitializeClass

try:
    from Products.CMFPlone.interfaces import INonStructuralFolder
    hasINonStructuralFolder = True # should be plone >= 2.1 version check?
except:
    hasINonStructuralFolder = False

# Dictionnaries containing portlet content types
_portlet_cts = {}


def registerPortlet(klass):
    """
    Add a new portlet
    """

    # Register structure
    data = {
        'class': klass,
        'portal_type': klass.portal_type,
        'meta_type': klass.meta_type,
        'portlet_macro': klass.portlet_macro,
        }

    key = data['meta_type']
    _portlet_cts[key] = data


class SimplePortletTool(UniqueObject, SimpleItem, PropertyManager):
    """ This tool provides some functions for portlet configuration and management in Plone """
    id = 'portlet_manager'
    meta_type= 'SimplePortlet tool'
    plone_tool = 1

    manage_options=PropertyManager.manage_options

    def __init__(self):
        # configuration
        self.manage_addProperty('conf_portlet_styles', (), 'lines')

        # portlets
        self.manage_addProperty('navigation', 'here/portlet_navigation/macros/portlet', 'string')
        self.manage_addProperty('login', 'here/portlet_login/macros/portlet', 'string')
        self.manage_addProperty('favorites', 'here/portlet_favorites/macros/portlet', 'string')
        self.manage_addProperty('user_defined_left', 'here/portlet_simpleportlet/macros/portlet_left', 'string')
        self.manage_addProperty('user_defined_right', 'here/portlet_simpleportlet/macros/portlet_right', 'string')
        self.manage_addProperty('calendar', 'here/portlet_calendar/macros/portlet', 'string')
        self.manage_addProperty('review', 'here/portlet_review/macros/portlet', 'string')
        self.manage_addProperty('related', 'here/portlet_related/macros/portlet', 'string')
        self.manage_addProperty('recent', 'here/portlet_recent/macros/portlet', 'string')
        self.manage_addProperty('news', 'here/portlet_news/macros/portlet', 'string')
        self.manage_addProperty('events', 'here/portlet_events/macros/portlet', 'string')

    def getPortletMetatypes(self):
        """
        Returns portlet meta types
        """

        return [x['meta_type'] for x in _portlet_cts.values()]

    def registerPortlet(self, friendlyName, path):
        """
        method to register portlets in the tool
        """
        # check if it doesn't exist yet
        if self.hasProperty(friendlyName):
            self.manage_changeProperties({friendlyName: path})
        else:
            self.manage_addProperty(friendlyName, path, 'string')

    def unRegisterPortlet(self, friendlyName):
        """
        method to un-register portlets in the tool
        """
        if self.hasProperty(friendlyName):
            self.manage_delProperties([friendlyName])

    def readProperties(self):
        trans=[]
        for dic in self._properties:
            if dic['id']!='title' and not dic['id'].startswith('conf_'):
                friendly=dic['id']
                unfriendly=self.getProperty(dic['id'])
                add={'unfriendly': unfriendly, 'friendly': friendly}
                trans.append(add)
        return trans

    def availablePortlets(self):
        res=[]
        for dic in self._properties:
            if dic['id']!='title' and not dic['id'].startswith('conf_'):
                res.append(dic['id'])
        res.sort()
        return res

    def makeFriendly(self, portlets):
        """ replaces portlet paths to friendly names """
        res=[]
        translations=self.readProperties()
        for s in portlets:
            appended=0
            for dic in translations:
                unfriendly=dic['unfriendly']
                friendly=dic['friendly']
                if unfriendly==s:
                    res.append(friendly)
                    appended=1
                    break
            if appended==0:
                #not found in translations. do not add to protect the user for typos
                #res.append(s)
                pass
        return res

    def getFolderPortlets(self, context, position, inherited):
        """
        method to get the portlet properties from a folder or the aquired properties.
        set inherit to return the aq. properties
        """
        if position=='columnOne':
            slot='left_slots'
        else:
            slot='right_slots'

        slots=[]
        if inherited:
            if context.portal_url.getPortalObject() is context:
                return None
            else:
                if hasattr(context.aq_self, slot):
                    slots=getattr(context.aq_parent, slot)
                else:
                    slots=getattr(context, slot)
        else:
            if hasattr(context.aq_self, slot):
                slots=getattr(context, slot)
            else:
                return None

        return self.makeFriendly(slots)

    def makeUnFriendly(self, portlets):
        """
        method to turn friendly portlets names into their real paths
        """
        res=[]
        translations=self.readProperties()
        for s in portlets:
            appended=0
            for dic in translations:
                unfriendly=dic['unfriendly']
                friendly=dic['friendly']
                if s==friendly:
                    res.append(unfriendly)
                    appended=1
                    break
            if appended==0:
                #not found in translations. Do not add to protect the user from typos
                #res.append(s)
                pass
        return res

    def configurePortlets(self, context):
        """
        process User portlet changes
        """
        columnOneSetting = context.REQUEST.get('columnOne')
        columnTwoSetting = context.REQUEST.get('columnTwo')
        columnOnePortlets = context.REQUEST.get('columnOnePortlets')
        columnTwoPortlets = context.REQUEST.get('columnTwoPortlets')

        if columnOneSetting=='columnOneInherit':
            # remove properties from this folder
            if hasattr(context.aq_self, 'left_slots'):
                if not context is context.portal_url.getPortalObject():
                    context.manage_delProperties(['left_slots'])
        else:
            #add property
            if hasattr(context.aq_self, 'left_slots'):
                context.manage_delProperties(['left_slots'], None)
            context.manage_addProperty('left_slots', tuple(self.makeUnFriendly(columnOnePortlets)), 'lines')

        if columnTwoSetting=='columnTwoInherit':
            # remove properties from this folder
            if hasattr(context.aq_self, 'right_slots'):
                if not context is context.portal_url.getPortalObject():
                    context.manage_delProperties(['right_slots'], None)
        else:
            #add property
            if hasattr(context.aq_self, 'right_slots'):
                context.manage_delProperties(['right_slots'], None)
            context.manage_addProperty('right_slots', tuple(self.makeUnFriendly(columnTwoPortlets)), 'lines')

    def getPortlets(self, context, position='columnOne'):
        mtool = getToolByName(context, 'portal_membership')
        portlets=[]
        ids=[]

        obj =context

        if not obj.isPrincipiaFolderish:
            obj=aq_parent(aq_inner(obj))

        current=obj
        allowedTypes =self.getPortletMetatypes()
        while mtool.checkPermission('View', current):
            folderObjects = current.getFolderContents(full_objects=True, contentFilter={'portal_type': allowedTypes})
            for o in folderObjects:
            # make sure o is of a proper portal_type
            # sometimes the filter doesn't work like with PloneLocalFolderNG
                if o.portal_type in allowedTypes:
                    ids.append(o.id)

                    if current is obj:
                        goOn=True
                    elif o.getShowinsubfolders():
                        goOn=True
                    elif hasINonStructuralFolder:
                        if INonStructuralFolder.providedBy(obj) and current is aq_parent(aq_inner(obj)):
                            goOn=True
                        else:
                            goOn=False
                    else:
                        goOn=False

                    if goOn:
                        if o.getPosition()==position:
                            if mtool.checkPermission('View', o):
                                if not o.id in [p.id for p in portlets]:
                                    portlets.append(o)

            if current==obj.portal_url.getPortalObject():
                break
            else:
                #get portlets on higher levels who have showinsubfolders set.
                current = aq_parent(aq_inner(current))

        # now filter out all objects that have getShow()=0
        portlets = [p for p in portlets if p.getShow()]

        return portlets


InitializeClass(SimplePortletTool)
