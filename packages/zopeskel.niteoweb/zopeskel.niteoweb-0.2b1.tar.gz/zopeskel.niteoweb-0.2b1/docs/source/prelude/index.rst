#######
Prelude
#######

******
Budget
******

Following this guide thoroughly will result in these monthly expenses:

- $11 - Rackspace Cloud instance for Headquarters server, ploneboutique.com
- $11 - Rackspace Cloud instance for one commercial project, ebar.si
- $6 - 3 Rackspace Email accounts: bob@ploneboutique.com, jane@ploneboutique.com and info@ploneboutique.com
- $9 - Micro plan at Unfuddle (code repository and task manager)
- $4 - JungleDisk Desktop for syncing company documents and files among employees with approx. 8 GB storage
- **SUM**: $41

*******
Purpose
*******

Purpose of this guide is to guide a less experienced Plone developer/administrator through the whole process of
starting and deploying a Plone project.

This guide differs from other guides by taking choices instead of reader. Plone and it's stack has many
movable parts and choosing right ones can be daunting. This guides makes this choices for you.
They are not always the best, however they can get you from square 1 to a decently deployed Plone site
in no time.

***********
End product
***********

Headquarters
============

End product of this guide is a Headquarters server with:

- Sphinx documentation of all your code projects (on ``sphinx.yourcompany.com``)
- system information for all your servers, gathered with `Munin`_ (on ``munin.yourcompany.com``)
- Hudson continuous integration service which runs your unit-tests every time you commit new code (on ``hudson.yourcompany.com``)

Commercial project
==================

Besides your main server, you'll have another server which runs your commercial project, ``ebar.si``, 
based on Plone 4.

End product
===========

.. image:: ../end_product.png
    :width: 100%

Legend: 

**Plone Boutique Ltd.**
    Imaginary Plone consultancy firm used throughout this guide.
    
**EBar Ltd.**
    Plone Boutique Ltd.'s imaginary client that needs a commercial Plone 4 site, running on http://ebar.si

**Bob**
    One of Plone Boutique Ltd. developers.

**Jane**
    One of Plone Boutique Ltd. developers.

**Unfuddle**
    Repository hosting and issue tracker for Plone Boutique Ltd.'s project.

**Rackspace Email**
    Email provider for Plone Boutique Ltd.


******************************
Security on production servers
******************************

Users
=====
#. Root SSH login is disabled.
#. SSH login only with password is disabled.
#. Administrator logs-in only with his dedicated maintenance account, then issues ``sudo su -`` to get higher privileges that enable him to do maintenance on the server.
#. Zope and related services run under dedicated user ``production`` which also has SSH login disabled. Administrators access this account by running ``sudo su - production``.
#. Nginx is running under a separate dedicated user ``nginx`` as it's the only service that is facing the internet directly.

.. image:: users.png
    :width: 600

Ports
=====

During deployment, a basic *iptables* firewall is installed on your server to block unwanted traffic. Allowed ports are:

#. 80 from anywhere - for HTTP requests
#. 22 from your office IP - for SSH access
#. 4949 from your Headquarters server IP - for Munin system reports

.. image:: ports.png
    :width: 600
    
***********
Assumptions
***********

Example names
=============

* Plone Boutique Ltd. - imaginary Plone company used as an example in this guide
* ``boutique`` - short name of imaginary Plone company used for usernames, code package names, etc.
* ``ebar`` - the name of an imaginary project of Plone Boutique Ltd., used as an example
* ``bob`` - one of developers in Plone Boutique Ltd.
* ``jane`` - another Plone Boutique Ltd. developer

Strictly following recommendations in Toolbox chapter
=====================================================

Since you want to make your life easier, acknowledge that this guide makes a lot of choices for you.
Just stick to them now and once you get the whole picture you will be able to do things your way.

Package structure
=================

This is an example of what files are in an imaginary commercial project for website ``ebar.si``. For this project we have one package with code and configuration, called ``boutique.ebar``.

::

    boutique.ebar/ (root folder of your egg)
    |-- base.cfg (buildout configuration that is shared among other *.cfg's, like project eggs, constants, ...)
    |-- bootstrap.py (run this to bootstrap your buildout environment)
    |-- buildout.cfg (symlink file pointing to development.cfg)
    |-- coverage.cfg (.cfg used to calculate code test coverage of this project on Headquar)
    |-- development.cfg (.cfg for building development environment with debugging, testing and deployment tools)
    |-- ebar.tmproj (TextMate project file)
    |-- hudson.cfg (.cfg used by Hudson to build your project and run unit tests on Headquarters server)
    |-- production.cfg (.cfg for building production environment on the server)
    |-- README.txt (where to find more info)
    |-- setup.cfg (configuration file for setup.py)
    |-- setup.py (python setup file)
    |-- sphinx.cfg (.cfg used to build Sphinx documentation of this project on Headquarters server)
    |-- svnignore (list of files/folders that should be ignored by subversion)
    |-- versions.cfg (list of pinned egg versions used for this project)
    |-- zopeskel.cfg (Answers to ZopeSkel's questions to ensure repeatability of 'paster create -t niteoweb_project')
    |-- docs (directory containing source files for Sphinx documentation)
    |   |-- HISTORY.txt (records changes made to this egg)
    |   |-- INSTALL.txt (info on installing this egg)
    |   |-- LICENSE.txt (info on licensing, normally its GPL)
    |   |-- LICENSE.GPL (copy of Gnu Public License)
    |   `-- source
    |       |-- conf.py (Sphinx configuration file)
    |       |-- index.rst (main documentation file)
    |       |-- _static (Sphinx puts images in this folder when generating HTML)
    |       `-- _templates (Sphinx puts files in this folder when generating HTML)
    |-- etc (folder containing configuration files generated by buildout from ./etc_templates)
    |-- etc_templates (containing templates that zc.buildout uses to generate system-level configuration)
    |   |-- iptables.conf.in (template for iptables configuration file)
    |   |-- fabfile.py.in (template for Fabric commands for deploymnent)
    |   |-- munin-node.conf.in (template for configuration for Munin node)
    |   `-- nginx.conf.in (template for Nginx configuration file)
    |-- keys (containing public keys of developers with access to production server)
    |   |-- bob.pub (Bob's public key)
    |   `-- jane.pub (Jane's public key)
    `-- boutique (directory containing actual code for this application)
         |-- __init__.py
         `-- ebar
             |-- __init__.py (initializer called when used as a Zope 2 product.)
             |-- config.py (defining project-wide code constants)
             |-- configure.zcml (main configure.zcml)
             |-- interfaces.py (defining project-wide interfaces and exceptions)
             |-- browser (directory containing Zope3 style resources)
             |   |-- __init__.py
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
             |-- static (directory containing static resources that will be server directly by Nginx in front of Zope)
             |   `-- error.html (static HTML error page that is displayed if something goes wrong with Zope)
             |-- tests (directory containing unit, functional and system tests)
             |   |-- __init__.py (setup TestCases for your project)
             |   |-- test_setup.py (test if this egg is correctly installed to Plone)
             |   `-- test_windmill.py (real-browser test of your Plone project)
             `-- xdv (directory containing collective.xdv templates and rules)
                 |-- template.html
                 `-- rules.xml         

.. URLs for links in content.

.. _Munin: http://munin-monitoring.org/