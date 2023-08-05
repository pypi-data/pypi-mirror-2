.. zopeskel.niteoweb documentation master file, created by
   sphinx-quickstart on Mon Feb  8 19:10:04 2010.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to zopeskel.niteoweb's documentation!
================================================================

:Project title: zopeskel.niteoweb
:Latest version: |release|
:Author: NiteoWeb Ltd.
:Framework: Plone 4
:URL: http://ploneboutique.com
:Source: http://svn.plone.org/svn/collective/zopeskel.niteoweb

""""""""""""""""""""""""""""""""


.. topic:: Summary

    This is a guide for less-experienced Plone developers, integrators and administrators. The guide makes
    development and deployment choices instead of you ensuring a smooth path from first code modifications
    to properly deploying a Plone 4 site on the cloud.

At the end of this journey you'll have a Plone 4 project with:

* latest collective.xdv with sample rules.xml and template.html,
* .svnignore files to ignore files/folders that should not be stored inside
  your code repository,
* base.cfg that holds global configuration for your buildout,
* versions.cfg that pins all your eggs to specific versions to ensure
  repeatability,
* development.cfg that builds a development environment,
* production.cfg that builds a production environment with ZEO,
* sphinx.cfg that is used to generate documentation for your code,
* test_setup.py that shows you how to write tests for your project,
* fabfile.py with Fabric commands to automatically deploy your code and data
  to a Rackspace Cloud server instance running CentOS,
* Sphinx documentation for your project,
* nginx.conf template to setup the Nginx web-proxy in front of your Zope,
* basic iptables configuration to deny access on all ports but the ones you
  actually use,
* munin-node.conf template to setup Munin system monitor node on your
  production server,
* and many more smaller goodies.


=================
Table of Contents
=================

.. toctree::
   :maxdepth: 3

   prelude.rst
   toolbox.rst
   headquarters.rst
   plone_project.rst
   glossary.rst


===========
Quick start
===========

Note that we use 'boutique' as a sample company short name and 'ebar' as a sample project short name.
You should use id's in the same manner (lowcase, letters only).

#. Open Cloud Servers account at Rackspace Cloud and create a new server instance with CentOS 5.5. 
   Write down server's IP and root password.
#. Open account at Unfuddle and create a new project with Subversion repository.
#. Create project skeleton
    .. bash::

        # Prepare Unfuddle Subversion repository
        ~$ svn mkdir https://boutique.unfuddle.com/svn/boutique_ebar/{trunk,branches,tags} -m 'Added base folders'

        # Create project skeleton 
        ~$ cd ~/work
        work$ paster create -t niteoweb_project boutique.ebar --config=plone.form/zopeskel.cfg
        
        Selected and implied templates:
          ZopeSkel#basic_namespace            A basic Python project with a namespace package
          zopeskel.niteoweb#niteoweb_project  A NiteoWeb Plone project

        Variables:
          egg:      boutique.ebar
          package:  boutiqueebar
          project:  boutique.ebar
        Expert Mode? (What question mode would you like? (easy/expert/all)?) ['easy']: all
        Namespace Package Name (Name of outer namespace package) ['boutique']:
        Package Name (Name of the inner namespace package) ['ebar']:
        Version (Version number for project) ['0.1']:
        Description (One-line description of the project) ['NiteoWeb Plone project']: Example Plone Boutique project
        Long Description (Multi-line description (in ReST)) ['']: Imaginary presentation site for eBar Ltd.
        Author (Name of author for project) ['NiteoWeb Ltd.']: Plone Boutique Ltd.
        Author Email (Email of author for project) ['info@niteoweb.com']: info@ploneboutique.com 
        Keywords (List of keywords, space-separated) ['Python Zope Plone']: 
        Project URL (URL of the homepage for this project) ['http://docs.niteoweb.com/']: http://ebar.si
        Project License (Name of license for the project) ['GPL']: 
        Zip-Safe? (Can this project be used as a zipped egg? (true/false)) [False]: 
        Zope2 Product? (Are you creating a product for Zope2/Plone or an Archetypes Product?) [True]: 
        Plone Version (Plone version # to install) ['4.0rc1']: 
        collective.xdv version (Version of collective.xdv that you would like to use in your project. Leave blank for no xdv.) ['1.0rc9']: 
        Maintenance users (Usernames of users that will have access to your production server, separated with commas.) ['iElectric,Kunta,zupo']: 'bob,jane'
        Hostname (Domain on which this project will run on.) ['zulu.com']: ebar.si
        Maintenance hostname (Domain on which your main (maintenance) server is running.) ['ploneboutique.com']: 
        IP (IP of production server. Leave default if you don't have one yet) ['127.0.0.1']: 12.34.56.78
        Temporary root password (Temporary password for root user on production server. Leave default if you don't have one yet) ['root_password_here']: abcdefgh99
        Creating template basic_namespace
        Creating directory ./boutique.ebar
          Recursing into +namespace_package+
            Creating ./boutique.ebar/boutique/
        ...
        ...
        ...
        TODO (zadnje par vrstic outputa)
        
        # Checkout Subversion repository
        work$ cd ebar/
        ebar$ svn co https://boutique.unfuddle.com/svn/boutique_ebar/trunk ebar
        
        
        

        # Install/Upgrade ZopeSkel to latest version
        $ sudo easy_install -U ZopeSkel

        # Install/Upgrade zopeskel.niteoweb to latest version
        $ sudo easy_install -U zopeskel.niteoweb
        
        # Create project skeleton
        $ 
        
#. Build development environment


.. include:: ../HISTORY.txt


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`