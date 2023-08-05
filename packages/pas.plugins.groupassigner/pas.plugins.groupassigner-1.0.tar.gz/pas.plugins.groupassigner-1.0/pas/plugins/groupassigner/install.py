from AccessControl.Permissions import manage_users
from Products.PageTemplates.PageTemplateFile import PageTemplateFile
from Products.PluggableAuthService import registerMultiPlugin

import plugin

manage_add_groupassigner_form = PageTemplateFile('browser/add_plugin',
                            globals(), __name__='manage_add_groupassigner_form' )


def manage_add_groupassigner( dispatcher, id,
                              title=None, group='', description='',
                              REQUEST=None ):
    """Add an GroupAssigner to the PluggableAuthentication Service."""

    sp = plugin.GroupAssigner( id, title, group, description )
    dispatcher._setObject( sp.getId(), sp )

    if REQUEST is not None:
        REQUEST['RESPONSE'].redirect( '%s/manage_workspace'
                                      '?manage_tabs_message='
                                      'GroupAssigner+added.'
                                      % dispatcher.absolute_url() )


def register_groupassigner_plugin():
    try:
        registerMultiPlugin(plugin.GroupAssigner.meta_type)
    except RuntimeError:
        # make refresh users happy
        pass


def register_groupassigner_plugin_class(context):
    context.registerClass(plugin.GroupAssigner,
                          permission = manage_users,
                          constructors = (manage_add_groupassigner_form,
                                          manage_add_groupassigner),
                          visibility = None,
                          icon='browser/icon.gif'
                         )
