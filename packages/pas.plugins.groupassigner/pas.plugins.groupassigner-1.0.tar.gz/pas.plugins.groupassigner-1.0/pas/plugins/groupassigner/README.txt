Tests for pas.plugins.groupassigner

Test setup
----------

    >>> from Testing.ZopeTestCase import user_password
    >>> from Products.Five.testbrowser import Browser
    >>> browser = Browser()

Plugin setup
------------

    >>> acl_users_url = "%s/acl_users" % self.portal.absolute_url()
    >>> browser.addHeader('Authorization', 'Basic %s:%s' % ('portal_owner', user_password))

    >>> self.portal.acl_users.userFolderAddUser('test_user_2_', 'secret', ['Member'], [])
    >>> u1 = self.portal.acl_users.getUserById('test_user_1_')
    >>> gtool = self.portal.portal_groups
    >>> gtool.addGroup('group1', ())
    True

pas.plugins.groupassigner should be in the list of installable plugins:

    >>> browser.open("%s/manage_main" % acl_users_url)
    >>> browser.url
    'http://nohost/plone/acl_users/manage_main'
    >>> form = browser.getForm(index=0)
    >>> select = form.getControl(name=':action')

    >>> 'Group Assigner' in select.displayOptions
    True

and we can select it:

    >>> select.getControl('Group Assigner').click()
    >>> select.displayValue
    ['Group Assigner']
    >>> select.value
    ['manage_addProduct/pas.plugins.groupassigner/manage_add_groupassigner_form']

we add 'Group Assigner' to acl_users:

    >>> from pas.plugins.groupassigner.plugin import GroupAssigner
    >>> assigner = GroupAssigner('group_assigner_test', 'Group Assigner')
    >>> assigner.group = 'group1'
    >>> assigner.condition = "python: 'reflab.com' in principal.getProperty('email')"
    >>> self.portal.acl_users['group_assigner_test'] = assigner
    >>> assigner = self.portal.acl_users['group_assigner_test']

Now the tests:

    >>> assigner.getGroupsForPrincipal(u1)
    ()
    >>> assigner.getGroupMembers('group1')
    ()
    >>> u1.setProperties(email='u1@reflab.com')
    >>> assigner.getGroupsForPrincipal(u1)
    ('group1',)
    >>> assigner.getGroupMembers('group1')
    ()

    >>> assigner.enumerateGroups()
    [{'pluginid': 'group_assigner_test', 'title': 'Group Assigner', 'id': 'group1', 'groupid': 'group1'}]
    >>> assigner.enumerateGroups(id='group1')
    [{'pluginid': 'group_assigner_test', 'title': 'Group Assigner', 'id': 'group1', 'groupid': 'group1'}]
    >>> assigner.enumerateGroups(id='groupX')
    []
