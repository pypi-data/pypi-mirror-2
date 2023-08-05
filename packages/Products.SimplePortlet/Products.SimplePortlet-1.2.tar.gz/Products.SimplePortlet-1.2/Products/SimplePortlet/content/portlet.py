
# Python imports
from AccessControl import ClassSecurityInfo

# CMF imports
try:
    from Products.CMFCore import permissions
except ImportError:
    from Products.CMFCore import CMFCorePermissions as permissions
from Products.CMFCore.utils import getToolByName

# Archetypes imports
from Products.Archetypes.public import *

from Products.ATContentTypes.content.base import ATCTContent

# Others
from Products.SimplePortlet.config import PORTLET_POSITION
from Products.SimplePortlet.SimplePortletTool import registerPortlet

from Products.Archetypes.public import DisplayList

PortletSchema = ATCTContent.schema.copy() + Schema((
     StringField('id',
                 required=0, ## Still actually required, but
                             ## the widget will supply the missing value
                             ## on non-submits
                 mode="rw",
                 accessor="getId",
                 mutator="setId",
                 default=None,
                 widget=IdWidget(
     label="Short Name",
     label_msgid="label_short_name",
     description="Should not contain spaces, underscores or mixed case. "\
     "Short Name is part of the item's web address.",
     description_msgid="help_shortname",
     visible={'view': 'visible'},
     i18n_domain="plone"),
                 ),
    StringField('title',
                required=1,
                searchable=1,
                default='',
                accessor='Title',
                widget=StringWidget(label_msgid="label_title",
                                    description_msgid="help_title",
                                    i18n_domain="plone"),
                ),
    StringField('description',
                searchable=1,
                isMetadata=1,
                accessor='Description',
                widget=TextAreaWidget(label='Description',
                                      label_msgid='label_description',
                                      description='Give a description for this Portlet.',
                                      description_msgid='help_description',
                                      i18n_domain='SimplePortlet'), ),
    StringField('position',
                vocabulary=PORTLET_POSITION,
                widget=SelectionWidget(label='Portlet position',
                                       label_msgid='label_position',
                                       description='Chose in which column the portlet will appear.',
                                       description_msgid='help_position',
                                       i18n_domain='SimplePortlet'),
                default='columnTwo'),
    BooleanField('showinsubfolders',
                 widget=BooleanWidget(label='Show in subfolders',
                                      label_msgid='label_showinsubfolders',
                                      description='Will the portlet also appear in subfolders.',
                                      description_msgid='help_showinsubfolders',
                                      i18n_domain='SimplePortlet'),
                 default=0),
    BooleanField('show',
                 widget=BooleanWidget(label='Show portlet',
                                      label_msgid='label_show',
                                      description='Is the portlet visible?.',
                                      description_msgid='help_show',
                                      i18n_domain='SimplePortlet'),
                 default=0),
    StringField('style',
                 vocabulary='getPortletStyles',
                 widget=SelectionWidget(label='Portlet style',
                                        label_msgid='label_style',
                                        description='The style to use for rendering the portlet',
                                        description_msgid='help_style',
                                        i18n_domain='SimplePortlet',
                                        condition="object/getPortletStyles")
                 ),
    TextField('body',
              searchable=1,
              required=0,
              primary=1,
              default_content_type='text/html',
              default_output_type = 'text/x-html-safe',
              allowable_content_types=('text/plain', 'text/structured', 'text/html', ),
              widget=RichWidget(label='Body',
                                label_msgid='label_body',
                                description='Body text of the portlet',
                                description_msgid='help_body',
                                i18n_domain='SimplePortlet')),
    ))

# there is no need for this field, doesn't make sense.
del PortletSchema['relatedItems']


class Portlet(ATCTContent):
    """
    A Portlet will be displayed as Plone portlet in the left or right column
    """
    global_allow=1
    schema = PortletSchema
    portal_type = meta_type = "Portlet"
    portlet_macro = 'here/portlet_simpleportlet_macros/macros/portlet'
    content_icon='portlet_icon.gif'
    security = ClassSecurityInfo()
    archetype_name = 'Portlet'
    immediate_view = "portlet_view"
    default_view = "portlet_view"
    _at_rename_after_creation = True


    security.declareProtected(permissions.View, 'getMacro')
    def getMacro(self):
        """return macro path to display portlet"""
        return self.portlet_macro

    security.declareProtected(permissions.View, 'hasBody')
    def hasBody(self):
        """ return true if there are some characters in body text """
        value = self.getBody(mimetype='text/plain').strip()
        return not not value

    security.declareProtected(permissions.View, 'getPortletStyles')
    def getPortletStyles(self):
        """return available styles (CSS class names) for portlets,
           taken from a property in SimplePortletTool"""

        ptool = getToolByName(self, 'portlet_manager')
        styledefs = ptool.getProperty('conf_portlet_styles', ())
        vocab = []
        for style in styledefs:
            s = style.split(':', 1)
            if len(s) < 2:
                s = (s[0], s[0])
            vocab.append(s)
        return DisplayList(vocab)

registerType(Portlet)
registerPortlet(Portlet)
