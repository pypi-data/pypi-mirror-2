from interfaces import IGroupManager
from zope.interface import implements
from zope.app.component.hooks import getSite
from Products.CMFCore.utils import getToolByName
from zope.component.interfaces import ComponentLookupError

class PortalGroupsGroupManager(object):
    """Implementation of `IGroupManager` which uses the `portal_groups` tool."""    
    implements(IGroupManager)
    
    def __init__(self, obj=None):
        """
        Creates the group manager. The `obj` argument is necessary because this
        class can be used as an adapter.
        """        
        self.obj = obj
        self.portal = getSite()
        self.portal_groups_tool = getToolByName(self.portal, 'portal_groups')
        
    def _get_group(self, name):
        return self.portal_groups_tool.getGroupById(name)
    
    def create_group(self, name):
        self.portal_groups_tool.addGroup(id=name)
        
    def remove_group(self, name):
        self.portal_groups_tool.removeGroups([name])
    
    def group_exists(self, name):
        return self._get_group(name) is not None
        
    def set_group_title(self, name, title):
        self.portal_groups_tool.editGroup(id=name, title=title)
        
    def get_group_title(self, name):
        return self._get_group(name).getProperty('title')

class DGPGroupsGroupManager(object):
    """
    Implementation of `IGroupManager` which uses the `DynamicGroupsPlugin`
    from `Products.PluggableAuthService`.    
    """    
    implements(IGroupManager)
    
    def __init__(self, plugin_id, predicate, obj=None):        
        self.portal = getSite()
        self.pas = getToolByName(self.portal, 'acl_users', None)
        
        # Special case when removing the Plone Site.
        if self.pas is None:
            self.pas = getToolByName(obj, 'acl_users')
                
        self.plugin = getattr(self.pas.plugins, plugin_id)
        self.predicate = predicate
        self.obj = obj
        
        
    def create_group(self, name):
        self.plugin.addGroup(
            group_id=name,
            predicate=self.predicate,
            active=True
        )
        
    def remove_group(self, name):
        self.plugin.removeGroup(name)
    
    def group_exists(self, name):
        return name in self.plugin.listGroupIds()
        
    def set_group_title(self, name, title):
        self.plugin.updateGroup(
            group_id=name,
            predicate=self.predicate,
            title=title,
        )
        
    def get_group_title(self, name):
        return self.plugin.getGroupInfo(name)['title']
        
