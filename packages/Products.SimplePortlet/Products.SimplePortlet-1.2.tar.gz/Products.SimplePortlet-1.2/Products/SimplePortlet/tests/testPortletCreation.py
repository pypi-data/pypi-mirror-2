
import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from Testing import ZopeTestCase
from Products.SimplePortlet.tests import SimplePortletTC
from DateTime import DateTime
from Products.Archetypes.utils import shasattr
from Products.Archetypes.public import DisplayList

# A test class defines a set of tests
class TestPortletCreation(SimplePortletTC.SimplePortletTestCase):

    # The afterSetUp method can be used to define test class variables
    # and perform initialisation before tests are run. The beforeTearDown() 
    # method can also be used to clean up anything set up in afterSetUp(),
    # though it is less commonly used since test always run in a sandbox
    # that is cleared after the test is run.
    def afterSetUp(self):
        self.membership = self.portal.portal_membership
        self.membership.memberareaCreationFlag = 1   
        self.addMember('fred', 'Fred Flintstone', 'fred@bedrock.com', ['Member', 'Manager'], '2002-01-01')
        self.login('fred')
        self.portal.invokeFactory('Folder', 'f1')
        self.f1 = self.portal.f1
        self.tool = self.portal.portlet_manager


    def addMember(self, username, fullname, email, roles, last_login_time):
        self.membership.addMember(username, 'secret', roles, [])
        member = self.membership.getMemberById(username)
        member.setMemberProperties({'fullname': fullname, 'email': email,
                                    'last_login_time': DateTime(last_login_time),}) 
        
    def testAddPortlet(self):
        self.f1.invokeFactory('Portlet', 'portlet1')
        self.failUnless(shasattr(self.f1, 'portlet1'))
        
    def testAddTopicPortlet(self):
        self.f1.invokeFactory('TopicPortlet', 'topicportlet1')
        self.failUnless(shasattr(self.f1, 'topicportlet1'))

    def testAddRSSPortlet(self):
        self.f1.invokeFactory('RSSPortlet', 'rssportlet1')
        self.failUnless(shasattr(self.f1, 'rssportlet1'))

    def testEditPortlet(self):
        self.f1.invokeFactory('Portlet', 'portlet1')
        self.failUnless(shasattr(self.f1, 'portlet1'))
        p = self.f1.portlet1
        p.setTitle('A Title')
        p.setDescription('A Description')
        p.setBody('<p>Some text</p>')
        p.setPosition('columnOne')
        p.setShowinsubfolders(1)
        p.setShow(1)
        p.setStyle('somestyle')
        

        self.failUnlessEqual(p.Title(), 'A Title')
        self.failUnlessEqual(p.Description(), 'A Description')
        self.failUnlessEqual(p.getBody(), '<p>Some text</p>')        
        self.failUnlessEqual(p.getPosition(), 'columnOne')
        self.failUnlessEqual(p.getShowinsubfolders(), 1)
        self.failUnlessEqual(p.getShow(), 1)
        self.failUnlessEqual(p.getStyle(), 'somestyle')
        
        self.failUnlessEqual(p.getMacro(), 'here/portlet_simpleportlet_macros/macros/portlet')

    def testEditTopicPortlet(self):
        self.f1.invokeFactory('TopicPortlet', 'topicportlet1')
        self.f1.invokeFactory('Topic', 'sf')
        p = self.f1.topicportlet1
        
        sf = self.f1.sf

        p.setTitle('A Title')
        p.setDescription('A Description')
        p.setBody('<p>Some text</p>')
        p.setPosition('columnOne')
        p.setShowinsubfolders(1)
        p.setShow(1)
        p.setStyle('somestyle')
        p.setTopic(sf)
        p.setMax_results(9)

        self.failUnlessEqual(p.Title(), 'A Title')
        self.failUnlessEqual(p.Description(), 'A Description')
        self.failUnlessEqual(p.getBody(), '<p>Some text</p>')        
        self.failUnlessEqual(p.getPosition(), 'columnOne')
        self.failUnlessEqual(p.getShowinsubfolders(), 1)
        self.failUnlessEqual(p.getShow(), 1)
        self.failUnlessEqual(p.getStyle(), 'somestyle')
        self.failUnlessEqual(p.getTopic(), sf)
        self.failUnlessEqual(p.getMaxResults(), 9)
        
        self.failUnlessEqual(p.getMacro(), 'here/portlet_topicportlet_macros/macros/portlet')

    def testEditRSSPortlet(self):
        self.f1.invokeFactory('RSSPortlet', 'rssportlet1')
        p = self.f1.rssportlet1
        
        p.setTitle('A Title')
        p.setDescription('A Description')
        p.setBody('<p>Some text</p>')
        p.setPosition('columnOne')
        p.setShowinsubfolders(1)
        p.setShow(1)
        p.setStyle('somestyle')
        p.setChannel('somechannel')
        p.setMax_results(9)

        self.failUnlessEqual(p.Title(), 'A Title')
        self.failUnlessEqual(p.Description(), 'A Description')
        self.failUnlessEqual(p.getBody(), '<p>Some text</p>')        
        self.failUnlessEqual(p.getPosition(), 'columnOne')
        self.failUnlessEqual(p.getShowinsubfolders(), 1)
        self.failUnlessEqual(p.getShow(), 1)
        self.failUnlessEqual(p.getStyle(), 'somestyle')
        self.failUnlessEqual(p.getChannel(), 'somechannel')
        self.failUnlessEqual(p.getMaxResults(), 9)

        self.failUnlessEqual(p.getMacro(), 'here/portlet_cmfsin_macros/macros/portlet')

    def testGetPortletStyles(self):
        self.tool.conf_portlet_styles = ('styleA', 'styleB')
        self.f1.invokeFactory('Portlet', 'portlet1')
        p = self.f1.portlet1
        expected = DisplayList((('styleA','styleA'),('styleB','styleB')))
        self.failUnlessEqual(p.getPortletStyles(), expected)
        
# This boilerplate method sets up the test suite
def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    # Add our test class here - you can add more test classes if you wish,
    # and they will be run together.
    suite.addTest(makeSuite(TestPortletCreation))
    return suite

if __name__ == '__main__':
    framework()
