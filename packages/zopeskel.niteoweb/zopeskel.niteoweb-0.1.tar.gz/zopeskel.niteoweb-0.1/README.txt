Starting, deploying and maintaining Plone 4 projects made easy
==============================================================

zopeskel.niteoweb is collection of ZopeSkel templates to help you standardize
and automate the task of starting, deploying and maintaining a new Plone
project. Its particularly helpful for less experienced Plone developers as 
they can get a properly structured and deployed Plone 4 project in no time.
A complete tutorial on how to use these templates for your own projects is
at http://ploneboutique.com.

It will help you to automate and standardize:

* Starting a new Plone 4 project that includes old- and new-style python,
  zope page template and css overrides, collective.xdv, etc.
* Adding your own functionalities and look to Plone 4.
* Staging and deploying your Plone 4 project on Rackspace Cloud server instance
  running CentOS, with Nginx in front and secured with iptables firewall
  (only $11 per month per instance!)
* Maintaining and upgrading your Plone 4 project on the production server.


By default the Plone 4 project you create with these templates is equiped with:

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
  to a Rackspace
  Cloud server instance running CentOS,
* Sphinx documentation for your project,
* nginx.conf template to setup the Nginx web-proxy in front of your Zope,
* basic iptables configuration to deny access on all ports but the ones you
  actually use,
* munin-node.conf template to setup Munin system monitor node on your
  production server,
* and many more smaller goodies.


Installation
============

Installation is simple, just run 'sudo easy_install zopeskel.niteoweb' and
you're good to go. Go where? To http://ploneboutique.com.


Assumptions
===========

Out-of-the-box, this package is intended for NiteoWeb's internal projects. 
However, at http://ploneboutique.com you'll find a comprehensive guide on how
to use these templates for your own projects.


To do
=====

- patch iostat munin plugin
- munin plugins for Zope
- audit iptables
- audit sudoers
- audit sshd_config
- bash_logout
- yum-security email notification
- investigate and fix fabric errors 'err: /bin/bash: /home/zupo/.bash_profile: Permission denied'

Contributors
============

- Nejc 'zupo' Zupan, NiteoWeb Ltd.
- Domen 'iElectric' Kožar, NiteoWeb Ltd.

