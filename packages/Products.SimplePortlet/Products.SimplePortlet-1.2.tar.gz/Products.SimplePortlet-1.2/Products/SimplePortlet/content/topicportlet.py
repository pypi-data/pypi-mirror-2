# Zope imports
from AccessControl import ClassSecurityInfo

# Archetypes imports
from Products.Archetypes.public import *

# Others
from Products.SimplePortlet.SimplePortletTool import registerPortlet
from Products.SimplePortlet.content import Portlet
from Products.SimplePortlet.content.portlet import PortletSchema

from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import *

schema = PortletSchema + Schema((
    ReferenceField('topic',
                default=None,
                relationship = "simpleportlet_topic",
                allowed_types = ('Topic'),
                widget=ReferenceBrowserWidget(
                    force_close_on_insert=1,
                    label='Smart Folder',
                    label_msgid='label_topic',
                    description='Select a Smart Folder whose items are shown in the portlet.',
                    description_msgid='help_topic',
                    i18n_domain='SimplePortlet',
                ),
        ),
    IntegerField('max_results',
                default=10,
                accessor='getMaxResults',
                widget=IntegerWidget(
                    label='Number of items to show in this portlet',
                    label_msgid='label_max_results',
                    description='',
                    description_msgid='help_max_results',
                    i18n_domain='SimplePortlet',
                ),
        ),
    BooleanField('show_more_link',
                 widget=BooleanWidget(label='Show link to more results',
                                      label_msgid='label_show_link_to_more_results',
                                      description='Include link to page showing more topic results.',
                                      description_msgid='help_show_link_to_more_results',
                                      i18n_domain='SimplePortlet'
                 ),
                 default=1
        ),
    BooleanField('show_date',
                 widget=BooleanWidget(label='Show item date',
                                      label_msgid='label_show_date',
                                      description='Include item date in portlet view.',
                                      description_msgid='help_show_date',
                                      i18n_domain='SimplePortlet'
                 ),
                 default=1
        ),

    ))


class TopicPortlet(Portlet):
    """Portlet to show the results of a predefined smart folder"""
    schema = schema
    portlet_macro = 'here/portlet_topicportlet_macros/macros/portlet'
    security = ClassSecurityInfo()
    archetype_name = 'Smart Folder Portlet'
    portal_type = meta_type = "TopicPortlet"

registerType(TopicPortlet)
registerPortlet(TopicPortlet)
