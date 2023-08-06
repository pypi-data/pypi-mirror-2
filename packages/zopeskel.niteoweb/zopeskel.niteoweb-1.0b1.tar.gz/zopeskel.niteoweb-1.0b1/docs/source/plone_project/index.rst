.. _plone-project:

##########################
Commercial Plone 4 project
##########################

************
Introduction
************

Now that you have come this far, this chapter should feel like a walk in the park. Without further ado, let's get started.

The guide is using an imaginary client ``eBar Ltd.`` that needs a website on ``ebar.si``. Imaginary Plone consultancy firm is still ``Plone Boutique Ltd.``.

*************
Code skeleton
*************

Unfuddle
========

Create a new project with Subversion repository (use ``ebar`` for project id). Give all your colleagues permissions on this project.

Now prepare your new Unfuddle Subversion repository by adding base folders:

   .. sourcecode:: bash

       ~$ svn mkdir http://boutique.unfuddle.com/svn/boutique_ebar/{trunk,branches,tags} -m 'Added base folders'

Cloud server
============

Login to ``manage.rackspacecloud.com`` and navigate to Cloud Server and click ``Add Server``. Choose ``CentOS 5.5`` for distro and ``265 MB`` for instance size. For ``Server Name`` enter ``ebar``.

Write down server's IP and root password. You'll need it for generating a project skeleton with ZopeSkel.

ZopeSkel
========

Prepare ZopeSkel
----------------

Install/Upgrade ZopeSkel to latest version.

   .. sourcecode:: bash

       $ sudo easy_install -U ZopeSkel
       
Install/Upgrade zopeskel.niteoweb to latest version.

   .. sourcecode:: bash

       $ sudo easy_install -U zopeskel.niteoweb


Generate code
-------------

Run ZopeSkel to generate a skeleton based on niteoweb_project template (the one used for all Plone Boutique projects). 

   .. sourcecode:: bash

        $ cd ~/work
        $ paster create -t niteoweb_project boutique.ebar

        Expert Mode? (What question mode would you like? (easy/expert/all)?) ['easy']: easy
        Description (One-line description of the project) ['Plone Boutique commercial project for eBar.si']:                                      
        Hostname (Domain on which this project will run on.) ['ebar.si']: ebar.si
        IP (IP of production server. Leave default if you don't have one yet) ['87.65.43.21']: <server_ip>
        Temporary root password (Temporary password for root user on production server. Leave default if you don't have one yet) ['root_password_here']: ebarM4Q8fsN90
        Maintenance users (Usernames of administrators that will have access to your production server, separated with commas.) ['bob,jane']: bob,jane
        Headquarters hostname (Domain on which your Headquarters server is running.) ['ploneboutique.com']: ploneboutique.com
        Maintenance IP (IP on which your Headquarters server is listening.) ['12.34.56.78']: <headquarters_ip>
        Office IP (Your office IP that you use daily and can VPN to) ['12.34.56.78']: <your_office_ip>

Commit project skeleton
-----------------------

Ok, skeleton is ready. Commit it to Subversion and continue working on it:

   .. sourcecode:: bash
   
        # Checkout Unfuddle's Subversion repository for this project
        work$ cd boutique.ebar/
        boutique.ebar$ svn co http://boutique.unfuddle.com/svn/boutique_ebar/trunk ./

        # Commit code skeleton
        boutique.ebar$ rm -rf src/boutique.ebar.egg-info
        boutique.ebar$ svn add *
        boutique.ebar$ svn ci -m "added project skeleton"
        
        # Set svn:ignore, instructions how to do this are also in svnignore files 
        boutique.ebar$ svn propset svn:ignore -F svnignore ./
        boutique.ebar$ svn propset svn:ignore -F docs/svnignore ./docs
        boutique.ebar$ svn propset svn:ignore -F etc/svnignore ./etc
        boutique.ebar$ svn up
        boutique.ebar$ svn ci -m "set svn:ignore"


*****************
Plone Development
*****************

Development environment
=======================

Use zc.buildout to prepare your development environment for you.

   .. sourcecode:: bash
   
        # Create symlink to development.cfg so you don't have to append '-c buildout.cfg' all the time
        boutique.ebar$ ln -s development.cfg buildout.cfg
        boutique.ebar$ svn add buildout.cfg
        boutique.ebar$ svn ci -m "added soft-link to development.cfg"
   
        # Make an isolated Python environment
        boutique.ebar$ virtualenv -p python2.6 --no-site-packages ./
   
        # Bootstrap zc.buildout
        boutique.ebar$ bin/python bootstrap.py
        
        # Build development/deployment environment
        boutique.ebar$ bin/buildout

.. note::        

    Pin down egg versions by copying the last lines of output into versions.cfg. This makes sure that if you run this buildout in a year you will get the same versions of packages.


Start it up!
============

You are now ready to start Zope in development mode, create your first Plone site and hack away::

    boutique.ebar$ bin/zope fg

.. warning:: For Nginx rewriting to work correctly your Plone's id needs to match your project's package name, e.g. ``ebar``. 

Plone Development
=================

You are now ready to start customizing Plone to your needs. 

Properties
----------

Open src/boutique/ebar/profiles/default/properties.xml and set some site properties. Read more about these XMLs: (TODO: links and pointers to GenericSetup documentation)

- http://plone.org/documentation/kb/genericsetup
- http://plone.org/documentation/manual/developer-manual/generic-setup


Theming
-------

Add your custom CSS and JS to ``ebar.css`` and ``ebar.js`` that you have in ``src/boutique/ebar/skins/ebar_css/ebar.css`` and ``src/boutique/ebar/skins/ebar_js/ebar.js``. Both files are already registered with Plone, for your convenience. Plone theming is a broad subject and is out of scope of this guide. Read more about theming:

- http://plone.org/products/collective.xdv/documentation/reference-manual/theming
- http://plone.org/documentation/kb/advanced-xdv-theming

Testing your code
=================

Test if your product is correctly installed in Plone by running ``bin/test -s boutique.ebar``. Testing your Plone codeis a broad subject and is out of scope of this guide. Read more about testing: 

- http://plone.org/documentation/manual/developer-manual/testing
- http://plone.org/documentation/kb/testing


****************
Plone Deployment
****************

Now here is where true fun begins and the value of zopeskel.niteoweb ZopeSkel template shows it's value. You will deploy your Plone site to a Rackspace Cloud server running CentOS in a matter of minutes without ever connecting to the server.

Copy over public keys
=====================

.. sourcecode:: bash

    boutique.ebar$ cp ~/SyncDisk/public_keys/*.pub ./keys


Bootstrap the server
====================

Re-generate Fabric command file and deploy on server.

.. sourcecode:: bash

    boutique.ebar$ bin/buildout
    boutique.ebar$ bin/deploy


Set local DNS settings
======================

You don't have to use DNS yet, having IP's mapped to hostnames in your local machine is enough for now. Adding the lines below to ``/etc/hosts`` does the trick. Note that you may have to restart your browser for changes to be applied::

    boutique.ebar$ sudo nano /etc/hosts
        
.. sourcecode:: bash

        <server_ip> ebar.si

You should be able to open http://ebar.si/ in your browser and see a your Plone site.

Redeploy
========

Every time you do changes to your code, configuration or data, you simply use one of Fabric commands to perform deployment or update on the server:

.. sourcecode:: bash

    boutique.ebar$ bin/fab reload_nginx_config
    boutique.ebar$ bin/fab update_static_files
    boutique.ebar$ bin/fab update_code
    boutique.ebar$ bin/fab run_buildout
    boutique.ebar$ bin/fab upload_data
    boutique.ebar$ bin/fab download_data
    boutique.ebar$ bin/fab restart supervisor_command