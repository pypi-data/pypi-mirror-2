
import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from Testing import ZopeTestCase
from Products.SimplePortlet.tests import SimplePortletTC

# A test class defines a set of tests
class TestInstallation(SimplePortletTC.SimplePortletTestCase):

    # The afterSetUp method can be used to define test class variables
    # and perform initialisation before tests are run. The beforeTearDown() 
    # method can also be used to clean up anything set up in afterSetUp(),
    # though it is less commonly used since test always run in a sandbox
    # that is cleared after the test is run.
    def afterSetUp(self):
        self.css        = self.portal.portal_css
        self.kupu       = self.portal.kupu_library_tool
        self.skins      = self.portal.portal_skins
        self.types      = self.portal.portal_types
        self.factory    = self.portal.portal_factory
        self.workflow   = self.portal.portal_workflow
        self.properties = self.portal.portal_properties
        self.siteprops = self.properties.site_properties
        self.nav_props  = self.portal.portal_properties.navtree_properties
        self.actions = self.portal.portal_actions
        self.icons = self.portal.portal_actionicons
        
        # todo tool
        self.metaTypes = ('Portlet', 'TopicPortlet', 'RSSPortlet')
        
    def testSkinLayersInstalled(self):
        self.failUnless('SimplePortlet' in self.skins.objectIds())

    def testTypesInstalled(self):
        for t in self.metaTypes:
            self.failUnless(t in self.types.objectIds())

    def testPortalFactorySetup(self):
        self.failUnless('Portlet' in self.factory.getFactoryTypes())
        self.failUnless('TopicPortlet' in self.factory.getFactoryTypes())
        self.failUnless('RSSPortlet' in self.factory.getFactoryTypes())

    def testToolInstalled(self):
        self.failUnless('portlet_manager' in self.portal.objectIds())        
        
        
    
# This boilerplate method sets up the test suite
def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    # Add our test class here - you can add more test classes if you wish,
    # and they will be run together.
    suite.addTest(makeSuite(TestInstallation))
    return suite

if __name__ == '__main__':
    framework()

