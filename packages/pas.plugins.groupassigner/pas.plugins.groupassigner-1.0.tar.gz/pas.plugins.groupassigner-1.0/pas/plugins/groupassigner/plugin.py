""" Class: GroupAssigner """
import zLOG

from AccessControl.SecurityInfo import ClassSecurityInfo
from App.class_init import default__class_init__ as InitializeClass

from OFS.Cache import Cacheable
from Products.PluggableAuthService.plugins.BasePlugin import BasePlugin
from Products.PluggableAuthService.utils import classImplements
from Products.PluggableAuthService.utils import createViewName

from Products.CMFCore.Expression import Expression
from Products.CMFCore.utils import getToolByName
from Products.PageTemplates.Expressions import getEngine
from Products.PageTemplates.Expressions import SecureModuleImporter

import interface

manage_options = list(BasePlugin.manage_options + Cacheable.manage_options)


def createExprContext(context, principal):
    '''
    An expression context provides names for TALES expressions.
    (adapted from Products.CMFCore.Expression)
    '''
    portal = getToolByName(context, 'portal_url').getPortalObject()

    data = {
        'portal':       portal,
        'nothing':      None,
        'modules':      SecureModuleImporter,
        'principal':    principal,
        }

    return getEngine().getContext(data)


class GroupAssigner(BasePlugin, Cacheable):
    """ Creates a virtual group, enables to assign this group to users """

    meta_type = 'Group Assigner'
    security = ClassSecurityInfo()

    _properties = (
        { 'id'      : 'title',
          'label'   : 'Title',
          'type'    : 'string',
          'mode'    : 'w',
        },
        { 'id'      : 'group',
          'label'   : 'Group Id',
          'type'    : 'string',
          'mode'    : 'w',
        },
        { 'id'      : 'group_title',
          'label'   : 'Group Title',
          'type'    : 'string',
          'mode'    : 'w',
        },
        { 'id'      : 'condition',
          'label'   : 'Condition',
          'type'    : 'text',
          'mode'    : 'w',
        },
        { 'id'      : 'debug',
          'label'   : 'Debug',
          'type'    : 'boolean',
          'mode'    : 'w',
        },

    )

    manage_options = manage_options

    def __init__(self, id, title='', group=None, condition=''):
        self._setId(id)
        self.title = title
        self.group = group
        self.group_title = title
        self.condition = condition or 'python:False'
        self.debug = False

    # IGroupEnumerationPlugin implementation
    def enumerateGroups(self, id=None, exact_match=False, sort_by=None, max_results=None, **kw):
        if kw:
            return []

        if id:
            id = id.lower()
            mygroup = self.group.lower()

            if exact_match and id!=mygroup:
                return []

            if not exact_match and id not in mygroup:
                return []

        return [ { 'id' : self.group,
                   'groupid' : self.group,
                   'title' : self.group_title,
                   'pluginid' : self.getId(),
               } ]


    # IGroupsPlugin implementation
    def getGroupsForPrincipal(self, principal, request=None):
        view_name = createViewName('getGroupsForPrincipal', principal)
        cached_info = self.ZCacheable_get(view_name)
        if cached_info is not None:
            return cached_info

        ec = createExprContext(self, principal)
        value = Expression(self.condition)(ec)

        if self.debug:
            zLOG.LOG( "Group Assigner",
                      zLOG.INFO,
                      "Group: %s Principal: %s Condition: %s Value: %s"%(
                            self.group, principal.getId(), self.condition, value))

        if value:
            groups = (self.group,)
        else:
            groups = ()

        self.ZCacheable_set(groups, view_name)
        return groups


    # IGroupIntrospection implementation
    def getGroupById(self, group_id):
        if group_id != self.group:
            return None

        return VirtualGroup(self.group, self.group_title)


    def getGroups(self):
        return [self.getGroupById(id) for id in self.getGroupIds()]


    def getGroupIds(self):
        return [ self.group ]


    def getGroupMembers(self, group_id):
        """ Empty because with many users this is potentially a DoS method"""
        return ()

classImplements(
    GroupAssigner,
    interface.IGroupAssigner,
)

InitializeClass(GroupAssigner)
