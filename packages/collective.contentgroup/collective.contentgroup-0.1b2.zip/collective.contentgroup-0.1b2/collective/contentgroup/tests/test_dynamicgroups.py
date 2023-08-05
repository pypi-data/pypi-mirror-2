from base import BaseTestCase
from Products.PluggableAuthService.plugins.DynamicGroupsPlugin import (
    DynamicGroupsPlugin, addDynamicGroupsPlugin)
import unittest
from StringIO import StringIO
from Products.PlonePAS.Extensions.Install import activatePluginInterfaces  

class TestDynamicGroups(BaseTestCase):
    
    def afterSetUp(self):
        BaseTestCase.afterSetUp(self)
        self.pas = self.portal.acl_users
        self.mtool = self.portal.portal_membership
        self.gtool = self.portal.portal_groups
        self.plugin_id = 'dgp'
        addDynamicGroupsPlugin(self.pas, self.plugin_id)
        self.plugin = getattr(self.pas, self.plugin_id)
        activatePluginInterfaces(self.portal, self.plugin_id, StringIO())
    
    def test_iintrospection_plugin_implementation(self):
        group_id = 'mygroup'
        
        # Group not created yet.
        self.failIf(self.plugin.getGroupById(group_id))
        self.failIf(self.plugin.getGroups())
        self.failIf(self.plugin.getGroupIds())
        
        # Create the group. The predicate makes all users belong to the group.
        self.plugin.addGroup(
            group_id=group_id,
            predicate='python: True',
            active=True
        )
        
        # Now check group existence.
        self.failUnless(self.plugin.getGroupById(group_id))
        self.failUnless(self.plugin.getGroups())
        self.failUnlessEqual(
            set(self.plugin.getGroupIds()), 
            set([group_id])
        )
        
        # Check membership.
        all_member_ids = set(self.mtool.listMemberIds())
        group_member_ids = set(self.plugin.getGroupMembers(group_id))         
        self.failUnless(group_member_ids)
        self.failUnlessEqual(all_member_ids, group_member_ids)
        
        # Play with portal_groups to see if we didn't break anything.        
        self.failUnless(group_id in self.gtool.listGroupIds())
        group_data = self.gtool.getGroupById(group_id)        
        self.failUnlessEqual(group_member_ids, set(group_data.getMemberIds()))
        
        
        
        
def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestDynamicGroups))
    
    return suite        