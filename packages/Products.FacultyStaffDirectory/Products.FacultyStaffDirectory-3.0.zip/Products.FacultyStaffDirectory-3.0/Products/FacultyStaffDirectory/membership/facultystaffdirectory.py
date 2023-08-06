from zope.interface import implements
from zope.component import adapts

from Products.CMFCore.utils import getToolByName

from Products.membrane.interfaces import IGroup
from Products.membrane.interfaces import IMembraneUserAuth

# from Products.membrane.at.interfaces import ICategoryMapper

# from Products.membrane.config import ACTIVE_STATUS_CATEGORY
from Products.membrane.config import TOOLNAME as MEMBRANE_TOOL

# from Products.membrane.utils import generateCategorySetIdForType

from Products.FacultyStaffDirectory.interfaces.facultystaffdirectory import IFacultyStaffDirectory
from Products.FacultyStaffDirectory.permissions import PROVIDES_ROLES

class Group(object):
    """Allow a FacultyStaffDirectory to act as a group for contained people
    """
    implements(IGroup)
    adapts(IFacultyStaffDirectory)
    
    def __init__(self, context):
        self.context = context
        
    def Title(self):
        return self.context.Title()
    
    def getRoles(self):
        """Get roles for this directory-group.
        
        Return an empty list of roles if the directory is in a workflow state
        that is not active in membrane_tool.
        """
        pm = getToolByName(self.context, 'portal_membership')
        if pm.checkPermission(PROVIDES_ROLES,self.context):
            return self.context.getRoles()
        else:
            return ()
    
    def getGroupId(self):
        return self.context.getId()

    def getGroupMembers(self):
        mt = getToolByName(self.context, MEMBRANE_TOOL)
        usr = mt.unrestrictedSearchResults
        members = {}
        for m in usr(object_implements=IMembraneUserAuth.__identifier__,
                     path='/'.join(self.context.getPhysicalPath())):
            members[m.getUserId] = 1
        return tuple(members.keys())
