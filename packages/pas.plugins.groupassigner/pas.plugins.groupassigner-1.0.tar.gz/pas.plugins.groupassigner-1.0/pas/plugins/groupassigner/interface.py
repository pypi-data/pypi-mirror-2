from Products.PluggableAuthService.interfaces.plugins import IGroupEnumerationPlugin
from Products.PluggableAuthService.interfaces.plugins import IGroupsPlugin
from Products.PlonePAS.interfaces.group import IGroupIntrospection

class IGroupAssigner( IGroupEnumerationPlugin, IGroupsPlugin,
                      IGroupIntrospection):
    """interface for GroupAssigner."""
