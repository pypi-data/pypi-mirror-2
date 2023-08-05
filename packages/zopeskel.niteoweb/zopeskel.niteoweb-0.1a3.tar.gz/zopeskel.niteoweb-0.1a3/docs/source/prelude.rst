=======
Prelude
=======

Budget
======

Following this guide thoroughly will result in these monthly expenses:

- $11 - Racspace Cloud instance for maintenance server at ploneboutique.com
- $11 - Rackspace Cloud instance for commercial project at ebar.si
- $6 - 3 Rackspace Email accounts: bob@ploneboutique.com, jane@ploneboutique.com and info@ploneboutique.com
- $9 - Micro plan at Unfuddle (code repository and task manager)
- $4 - JungleDisk Desktop for syncing company documents and files among employees with cca. 8 GB storage
- **SUM**: $41


Purpose
=======

Purpose of this guide is to guide a less experienced Plone developer/administrator through the whole process of
starting and deploying a Plone project.

This guide differs from other guides by taking choices instead of reader. Plone and it's stack has many
movable parts and choosing right ones can be daunting. This guides makes this choices for you.
They are not always the best, however they can get you from square 1 to a decently deployed Plone site
in no time.


End product
===========

End product of this guide is a server with static HTML/CSS site for your company/organization. On the same server
you'll also have documentation of all your products (on docs.yourcompany.com) and system information for all
your servers (gathered with Munin, at munin.yourcompany.com). 

Besides your main server, you'll have another server which runs your commercial project, ebar.si.com, 
based on Plone 4.


Assumptions
===========

Example names
-------------

* Plone Boutique Ltd. - imaginary Plone company used as an example in this guide
* boutique - short name of imaginary Plone company used for usernames, egg names, etc.
* ebar - the name of an imaginary project of Plone Boutique Ltd. that we use as an example


Strictly following recommendations in toolbox
---------------------------------------------

Since we want to make your life easier, this guide makes a lot of choices for you.
Just follow them now and once you get the whole picture you will be able
to do things your way.


Egg structure
-------------

::

    boutique.ebar/ (root folder of your egg)
    |-- .svnignore (list of files/folder that should be ignored by subversion)
    |-- ebar.tmproj (TextMate project file)
    |-- base.cfg (buildout configuration that is shared among other .cfg's, like project eggs, constants, ...)
    |-- bootstrap.py (run this to bootstrap your buildout environment)
    |-- development.cfg (.cfg for building development environment with debugging and testing tools)
    |-- buildout.cfg (symlink file pointing to development.cfg)
    |-- production.cfg (.cfg for building production environment)
    |-- versions.cfg (list of egg versions used for this project)
    |-- README.txt (where to find more info)
    |-- setup.py (python setup file)
    |-- setup.cfg (configuration file for setup.py)
    |-- zopeskel.cfg (Answers to ZopeSkel's questions to ensure repeatability of 'paster create -t niteoweb_project')
    |-- etc (containing system-level configuration for deployment)
    |   `-- iptables.conf (iptables configuration file)
    |-- etc_templates (containing templates that buildout uses to generate system-level configuration)
    |   |-- fabfile.py.in (template for Fabric commands for deploymnent)
    |   |-- munin-node.conf.in (template for configuration for Munin node)
    |   `-- nginx.conf.in (template for Nginx configuration file)
    |-- keys (containing public keys of developers with access to production server)
    |   |-- bob.pub (Bob's public key)
    |   `-- jane.pub (Jane's public key)
    |-- docs (directory containing source files for Sphinx documentation)
    |   |-- HISTORY.txt (records changes made to this egg)
    |   |-- INSTALL.txt (info on installing this egg)
    |   |-- LICENSE.txt (info on licensing, normally its GPL)
    |   |-- LICENSE.GPL (copy of Gnu Public License)
    |   `-- source
    |       |-- _static (TODO)
    |       |-- _templates (TODO)
    |       |-- conf.py (Sphinx configuration file)
    |       `-- index.rst (main documentation file)
    `-- boutique (directory containing actual code for this application)
         |-- __init__.py
         `-- ebar
             |-- __init__.py (initializer called when used as a Zope 2 product.)
             |-- configure.zml (main configure.zcml)
             |-- config.py (defining project wide constants)
             |-- interfaces.py (defining project wide interfaces and exceptions)
             |-- browser (directory containing Zope3 style resources)
             |   |-- __init__.py
             |   |-- interfaces.py (holding the IThemeSpecific interface for theme)
             |   `-- configure.zcml (configuring Zope3 style resources)
             |-- profiles (directory containing GenericSetup configuration)
             |   `-- default
             |       |-- cssregistry.xml (configure Plone's portal_css)
             |       |-- jsregistry.xml (configure Plone's portal_javascripts)
             |       |-- metadata.xml (version and other information for Plone about this egg)
             |       |-- properties.xml (configure Plone's main properties like site title)
             |       `-- skins.xml (configure Plone's portal_skins)
             |-- skins (directory containing Zope2 style resources)
             |   |-- ebar_css (directory containing your custom CSS)
             |   |-- ebar_images (directory containing your custom images)
             |   |-- ebar_js (directory containing your custom JavaScripts)
             |   |-- ebar_scripts (directory containing your custom Script (Python) scripts)
             |   `-- ebar_templates (directory containing your custom Zope Page Templates)
             |-- static (directory containing static resources that will be server directly by the web-proxy in front of Zope)
             |   `-- error.html (static HTML error page that is displayed if something goes wrong with Zope)
             |-- tests (directory containing unit, functional and system tests)
             |   |-- __init__.py (setup TestCases for your project)
             |   `-- test_setup.py (test if this egg is correctly installed to Plone)
             `-- xdv (directory containing collective.xdv templates and rules)
                 |-- template.html
                 `-- rules.xml         
