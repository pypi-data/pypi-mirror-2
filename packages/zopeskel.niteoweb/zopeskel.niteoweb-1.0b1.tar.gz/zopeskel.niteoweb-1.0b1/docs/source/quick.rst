###########
Quick start
###########

Note that we use ``boutique`` as a sample company short name and ``ebar`` as a sample project short name.
You should use ids in the same manner (lower-case, letters only).

#. Create a Cloud Servers account at Rackspace Cloud and create a new server instance with CentOS 5.5. 
   Write down server's IP and root password.
#. Create an account at Unfuddle and create a new project with Subversion repository.
#. Prepare Unfuddle Subversion repository

   .. sourcecode:: bash

       ~$ svn mkdir http://boutique.unfuddle.com/svn/boutique_ebar/{trunk,branches,tags} -m 'Added base folders'

#. Prepare ZopeSkel

   .. sourcecode:: bash

       # Install/Upgrade ZopeSkel to latest version
       ~$ sudo easy_install -U ZopeSkel
       
       # Install/Upgrade zopeskel.niteoweb to latest version
       ~$ sudo easy_install -U zopeskel.niteoweb


#. Create project skeleton. Replace boutique.ebar with your custom string. Example: yourcompany.firstcustomer.

   ::

       ~$ cd ~/work
       work$ paster create -t niteoweb_project boutique.ebar --config=boutique.ebar/zopeskel.cfg
           
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
       collective.xdv version (Version of collective.xdv that you would like to use in your project.)['1.0rc9']: 
       Hostname (Domain on which this project will run on.) ['zulu.com']: ebar.si
       Maintenance users (Usernames of users that will have access to your production server, separated with commas.) ['iElectric,Kunta,zupo']: 'bob,jane'
       Maintenance hostname (Domain on which your main (maintenance) server is running.) ['niteoweb.com']: ploneboutique.com
       Maintenance email (Email on which you receive system notifications from production servers.) ['maintenance@niteoweb.com']: maintenance@ploneboutique.com
       IP (IP of production server. Leave default if you don't have one yet) ['12.34.56.78']: <IP you wrote down above>
       Temporary root password (Temporary password for root user on production server. Leave default if you don't have one yet) ['root_password_here']: <root password you wrote down above>
       Creating template basic_namespace
       Creating directory ./boutique.ebar
       ...
       ...
       ...
       Running /Library/Frameworks/Python.framework/Versions/2.6/Resources/Python.app/Contents/MacOS/Python setup.py egg_info

#. Checkout Subversion repository, commit project skeleton and set ``svn:ignore`` for files and folders that should not be in code repository.

   .. sourcecode:: bash
   
        # Checkout Unfuddle's Subversion repository for this project
        work$ cd boutique.ebar/
        boutique.ebar$ svn co http://boutique.unfuddle.com/svn/boutique_ebar/trunk ./

        # Commit code skeleton
        boutique.ebar$ svn add *
        boutique.ebar$ svn ci -m "added project skeleton"
        
        # Set svn:ignore, instructions how to do this are also in svnignore file itself
        boutique.ebar$ svn propset svn:ignore -F svnignore ./
        boutique.ebar$ svn propset svn:ignore -F docs/svnignore ./docs
        boutique.ebar$ svn propset svn:ignore -F etc/svnignore ./etc
        boutique.ebar$ svn up
        boutique.ebar$ svn ci -m "set svn:ignore"        
        
#. Build development environment

   .. sourcecode:: bash
   
        # Create symlink to development.cfg so you don't have to append '-c buildout.cfg' all the time
        boutique.ebar$ ln -s development.cfg buildout.cfg
        boutique.ebar$ svn add buildout.cfg && svn ci -m "added soft-link to development.cfg"
   
        # Make an isolated Python environment
        boutique.ebar$ virtualenv -p python2.6 --no-site-packages ./
   
        # Bootstrap zc.buildout
        boutique.ebar$ bin/python bootstrap.py
        
        # Build development environment
        boutique.ebar$ bin/buildout

#. Pin down egg versions by copying version pins outputted by buildout. Search for
   ``*************** PICKED VERSIONS ****************`` and copy all lines except ``[versions]``
   to your ``versions.cfg`` file under ``Bindings outputted by buildout.dumppickedversions for development.cfg``.

#. Start Zope in debug mode and point your browser to http://localhost:8080 to confirm that it starts properly.
   Create a Plone site with id ``ebar`` and select ``boutique.ebar`` extension profile to confirm that your package
   installs correctly into Plone.

   .. sourcecode:: bash
   
        boutique.ebar$ bin/zope fg
        # stop with Ctrl+c

#. Let's build a production environment so we get deployment tools prepared for us and test that production services are working. When done, point your browser to ``http://localhost:11401/ebar`` to confirm that Plone is running.

   .. sourcecode:: bash
   
        # build production environment
        boutique.ebar$ bin/buildout -c production.cfg
        boutique.ebar$ bin/zeo start
        boutique.ebar$ bin/zope1 start
        
        # test in browser
        
        boutique.ebar$ bin/zope1 stop
        boutique.ebar$ bin/zeo stop
        
#. We're now ready to deploy this Plone site to a Rackspace Cloud server. If you haven't already done so, now is the time to create one and write down it's IP and root password into production.cfg. You also need to put your maintenance users' public keys in to ``./keys``. Filenames should match each user's id. 

   .. sourcecode:: bash
   
        # for each maintenance user, add their public key; filename must match user's id
        boutique.ebar$ nano keys/bob.pub
        boutique.ebar$ nano keys/jane.pub
        
        # re-run buildout to update deployment tools with server IP and root password
        boutique.ebar$ bin/buildout -c production
   
        # bootstrap CentOS server and deploy your Plone site
        boutique.ebar$ bin/fab deploy

#. This should be it! Add ``<server_ip> <hostname>`` line to your ``/etc/hosts`` file and point your browser to ``http://<hostname>``. You should see your Plone 4 project, deployed on a cloud server.
