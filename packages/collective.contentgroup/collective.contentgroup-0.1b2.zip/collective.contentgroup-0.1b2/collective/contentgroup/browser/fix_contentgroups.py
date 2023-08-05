from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName
from collective.contentgroup.events import initialized
from collective.contentgroup.interfaces import IObjectWithGroup, IGroupManager
from StringIO import StringIO

class FixContentGroupsView(BrowserView):
    
    def fix_content_group(self, obj):
        group_name = obj.get_group_name()
        group_title = obj.get_group_title()
        group_manager = IGroupManager(obj)
        
        print >> self.out, 'Name: %s; Title: %s;' % (group_name, group_title),    
        
        if not group_manager.group_exists(group_name):
            group_manager.create_group(group_name)
            group_manager.set_group_title(group_name, group_title)
            print >> self.out, 'Group created.'
        else:
            print >> self.out, 'Group already exists.'
                            
    
    def __call__(self):
        self.out = StringIO()
        catalog = getToolByName(self.context, 'portal_catalog')
        brains = catalog(object_provides=IObjectWithGroup.__identifier__)
        for b in brains:
            o = b.getObject()
            self.fix_content_group(o)
                        
        return self.out.getvalue()