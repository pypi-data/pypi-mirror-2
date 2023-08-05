Introduction
============

    The plugin creates a virtual group and helps to assign this group to
    users by evaluation of a TALES expression.

Installation
============

    Buildout

      See docs/INSTALL.txt

    Plone Site

      - Go in the site acl_users then add "Group Assigner"
      - Set the properties: group id, group title and the condition
        (see below for the meaning of 'debug')
      - Activate all the functionalities provided by the plugin

Notes
=====

    The expression is based only on principal methods and attributes.
    It is not possible to assign the group on context base.

    Variable available are:

        principal
        portal
        nothing
        modules

    From 'principal' you can use the 'getProperty' method to use in your
    expression. For example:

      python: principal.getProperty('email').split('@')[-1] in ['reflab.com',]

    To assign more than one group you have to add one plugin for each group.

    To cache the plugin add a RAMCache manager and assign the plugin to him.
    If the plugin is cached remember to invalidate the cache when changing
    properties.

    You can activate the 'debug' properties to log the evaluation of the
    expression (in this case don't use cache).

Other infos
===========

    Questions and comments to riccardo@reflab.com

    Report bugs at riccardo@reflab.com

    Code repository: http://svn.plone.org/svn/collective/PASPlugins/pas.plugins.groupassigner
