
# Zope imports
from AccessControl import ClassSecurityInfo
from ComputedAttribute import ComputedAttribute

# CMF imports
from Products.CMFCore.utils import getToolByName

# Archetypes imports
from Products.Archetypes.public import *

# Others
from Products.SimplePortlet.SimplePortletTool import registerPortlet
from Products.SimplePortlet.content import Portlet
from Products.SimplePortlet.content.portlet import PortletSchema

schema = PortletSchema + Schema((
    StringField('channel',
                default=None,
                widget=SelectionWidget(
                    label='Channel',
                    label_msgid='label_channel',
                    description='Select your RSS channel.',
                    description_msgid='help_channel',
                    i18n_domain='SimplePortlet'),
        ),
    IntegerField('max_results',
                default=10,
                accessor='getMaxResults',
                widget=IntegerWidget(
                    label='Maximum result',
                    label_msgid='label_max_results',
                    description='Enter the maximum results displayed in portlet.',
                    description_msgid='help_max_results',
                    i18n_domain='SimplePortlet'),
        ),
    ))


class CMFSinPortlet(Portlet):
    """
    A Portlet displaying rss based on CMFSin
    """

    schema = schema
    portlet_macro = 'here/portlet_cmfsin_macros/macros/portlet'
    security = ClassSecurityInfo()
    archetype_name = 'RSS Portlet'
    portal_type = meta_type = "RSSPortlet"

    security.declarePublic('getCMFSinChannels')
    def getCMFSinChannels(self):
        sin_tool = getToolByName(self, 'sin_tool')
        return DisplayList([(x.id, x.id) for x in list(sin_tool.Maps())])


    schema['channel'].vocabulary = ComputedAttribute(getCMFSinChannels, 1)

registerType(CMFSinPortlet)
registerPortlet(CMFSinPortlet)
