.. zopeskel.niteoweb documentation master file, created by
   sphinx-quickstart on Mon Feb  8 19:10:04 2010.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Plone Boutique Guide!
================================

:Author: NiteoWeb Ltd.
:Latest version: |release|
:Generated: |today|
:Framework: Plone 4
:URL: http://ploneboutique.com
:Source: http://svn.plone.org/svn/collective/zopeskel.niteoweb

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

=======
Summary
=======

    This is a guide for Plone developers, integrators and administrators who are overwhelmed with the amount of moving parts building up Plone. This guide makes development and deployment choices instead of you, ensuring you a smooth path from first code modifications to a properly deployed Plone 4 site on the cloud.

========
Overview
========

    At the end of this journey you'll have a Plone 4 project with:

    * latest collective.xdv with sample rules.xml and template.html,
    * versions.cfg that pins all your eggs to specific versions to ensure
      repeatability,
    * development.cfg that builds a development environment,
    * production.cfg that builds a production environment with ZEO,
    * test_setup.py that shows you how to write tests for your project,
    * fabfile.py with Fabric commands to automatically deploy your code and data
      to a Rackspace Cloud server instance running CentOS,
    * Sphinx documentation for your project,
    * nginx.conf template to setup the Nginx web-proxy in front of your Zope,
    * basic iptables configuration to deny access on all ports but the ones you
      actually use,
    * and many more.

.. image:: end_product.png
    :width: 100%


=================
Table of Contents
=================

.. toctree::
   :maxdepth: 3

   prelude/index.rst
   toolbox/index.rst
   headquarters/index.rst
   plone_project/index.rst
   quick.rst

.. include:: ../HISTORY.txt


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
