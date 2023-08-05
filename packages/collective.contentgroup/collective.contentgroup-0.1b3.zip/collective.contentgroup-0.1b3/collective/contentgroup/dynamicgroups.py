"""
This module makes `DynamicGroupsPlugin` from `PluggableAuthService`
implements the `IGroupIntrospection` plugin. This way user interfaces can
list the members of the dynamic groups.

Not quite related to the purpose of this package, it's like a bonus.
"""

from plone.memoize.volatile import cache

from Products.PluggableAuthService.plugins.DynamicGroupsPlugin import (
    DynamicGroupsPlugin)
from Products.CMFCore.utils import getToolByName
from Products.PluggableAuthService.utils import classImplements
from Products.PlonePAS.interfaces.group import IGroupIntrospection
from Products.PlonePAS.tools.groupdata import GroupData
from zope.annotation import IAnnotations


def getGroupById(self, group_id):
    """Implementation of `IGroupIntrospection`."""
    if group_id not in self.listGroupIds():
        return None
        
    gtool = getToolByName(self, 'portal_groupdata')
    return GroupData(tool=gtool, id=group_id)
    
def getGroups(self):
    """Implementation of `IGroupIntrospection`."""
    return [self.getGroupById(id) for id in self.listGroupIds()]    

def getGroupIds(self):
    """Implementation of `IGroupIntrospection`."""
    return self.listGroupIds()

def getGroupMembers(self, group_id):
    """Implementation of `IGroupIntrospection`."""
    if group_id not in self.listGroupIds():
        return tuple()
            
    mtool = getToolByName(self, 'portal_membership')
    return [
        m.getId() for m in mtool.listMembers() 
        if group_id in self.getGroupsForPrincipal(m)
    ]

DynamicGroupsPlugin.getGroupById = getGroupById
DynamicGroupsPlugin.getGroups = getGroups
DynamicGroupsPlugin.getGroupIds = getGroupIds
DynamicGroupsPlugin.getGroupMembers = getGroupMembers
    
classImplements(DynamicGroupsPlugin, IGroupIntrospection)    
