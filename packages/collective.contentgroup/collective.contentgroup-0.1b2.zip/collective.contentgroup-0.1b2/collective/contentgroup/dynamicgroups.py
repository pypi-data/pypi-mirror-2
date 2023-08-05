"""
This module makes `DynamicGroupsPlugin` from `PluggableAuthService`
implements the `IGroupIntrospection` plugin. This way user interfaces can
list the members of the dynamic groups.

It also makes `getGroupsForPrincipal` cache its results on the request. It's
useful to enhance performance when there are many dynamic groups.

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

def get_cache(func, self, principal, request=None):    
    if request is None:
        request = getattr(self, 'REQUEST', None)
    
    if request is None:
        return {}

    # Detect test mode and disable cache in this case.
    url = request.get('SERVER_URL')
    if url and ('nohost' in url):
        return {}
    
    
    return IAnnotations(request)
    

def get_cache_key(func, self, principal, request=None):
    return self.getId() + principal.getId()

def cache_in_request(func):
    return cache(get_key=get_cache_key, get_cache=get_cache)(func)

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
DynamicGroupsPlugin.getGroupsForPrincipal = \
    cache_in_request(DynamicGroupsPlugin.getGroupsForPrincipal)
    
classImplements(DynamicGroupsPlugin, IGroupIntrospection)    
