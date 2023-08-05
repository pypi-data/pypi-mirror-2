from Permissions import ADD_CONTENTS_PERMISSION
from Products.Archetypes.public import DisplayList

PROJECTNAME = "SimplePortlet"
SKINS_DIR = 'skins'

GLOBALS = globals()

PORTLET_POSITION = DisplayList((
    ('columnOne', 'Column one', 'label_column_one'), ('columnTwo', 'Column two', 'label_column_two'),
    ))
