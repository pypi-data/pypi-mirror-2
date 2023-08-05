from Products.PluggableAuthService.plugins.DynamicGroupsPlugin import (
    DynamicGroupsPlugin, addDynamicGroupsPlugin)
from base_groupmanager import BaseGroupManagerTestCase
from collective.contentgroup.groupmanager import (PortalGroupsGroupManager, 
    DGPGroupsGroupManager)
import base
import unittest
        
class PortalGroupsGroupManagerTestCase(BaseGroupManagerTestCase):
    
    def create_group_manager(self):
        return PortalGroupsGroupManager()    

class DGPGroupsGroupManagerTestCase(BaseGroupManagerTestCase):
    
    def create_group_manager(self):
        plugin_id = 'dgp'
        addDynamicGroupsPlugin(self.portal.acl_users, plugin_id)        
        return DGPGroupsGroupManager(
            plugin_id=plugin_id, 
            predicate='python: p.getId().startswith("rafael")'
        )
        
        
def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(PortalGroupsGroupManagerTestCase))
    suite.addTest(unittest.makeSuite(DGPGroupsGroupManagerTestCase))
    
    return suite
