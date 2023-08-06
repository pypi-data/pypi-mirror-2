.. _toolbox:

#######
Toolbox
#######

******************
Developer machines
******************

Whatever system you are using (hopefully not Windows) you need the following tools installed on your system:

- a decent code editor (Kate on Kubuntu, TextMate on OSX, vim, emacs, etc.)
- subversion
- python 2.6
- whatever you need to be able to run buildout (``build-essentials`` package on Ubuntu, *XCode* on OSX, etc.)

*************************
Outsourcing core services
*************************

Let's say you charge $50 per hour for your work. If you have only a few hours of maintenance per year to do on your email/issuer-tracker/subversion server, you've already spent more than you would have if you'd paid someone else to take care of these services. And you'll have far more than 2 hours per year of maintenance work. Plus, your multi-purpose server will surely go down exactly when you are relaxing on some beach. Every single time.

Subversion repository and issuer tracker
========================================

I'd recommend using Unfuddle as you get both of the above mentioned in on place. Commit messages can be nicely linked to issues and vice-versa. Also, they offer free plans for small projects, after that the plans start at $9/month. It has less features and cool factor than github or bitbucket, but for starters it's ok. It's simple, fast enough and has not had any serious downtime for the past 3 years.

.. image:: unfuddle.png
    :width: 600


Email
=====

Use Rackspace Email. I've learned the hard way that saving money when choosing email provider is plain stupid. A quality one ensures your emails get delivered on time, every time and into one's inbox instead of SPAM folder.
They are a bit on the upper with the price being $2 per mailbox per month, but it's worth it. 

Since mailboxes have their price, think before you create a new one. Normally having one mailbox for your info@ email and one for each employee is enough. If you need additional email addresses sort it out with aliases. Aliases are free and you can add an unlimited amount of them.

Some may say why not use Gmail which is free for up to 50 mailboxes? Well their support record is't really what is should be for such a critical service. It's logical if you consider that email isn't their primary business and they can decide to stop providing the service any time. 

.. image:: email.png
    :width: 600


Backups and archiving
=====================

The recommendation here is JungleDisk. It's basically the same as DropBox, but with data encryption. For starters you can easily use Desktop Edition, which costs $3/month plus $0.15 per GB/month. Cheap enough.

.. note::
    
    JungleDisk allows you to choose where you want to store your data, Rackspace Cloud or Amazon S3. Both options cost the same for 1GB/month of storage, but Amazon S3 also charges for incoming and outgoing bandwidth. Ergo, Rackspace Cloud is a better pick here, obviously.

With JungleDisk you have 3 options to chose from:
    - Simple Backup (daily backs up a folder on your machine)
    - Online Disk (file are stored on an online disk and do not take up space on your local disk)
    - Sync Folder (same funcitonality as dropbox, you have access to files even when offline)
    
SyncDisk
--------

This is a folder in your home folder which you and your colleagues use to share frequently used files. Use JungleDisk Desktop software to Sync Folder called SyncDisk and limit it to about 2GB or so. Normally you would want to have it at ``/home/bob/SyncDisk`` or ``/Users/bob/SyncDisk``.

The name *SyncDisk* indicates that it's functionality is the same as DropBox's.

Database containing passwords stored with KeePass should be contained in SyncDisk so all changes are immediately propagated to your colleagues' KeePasses.

OnlineDisk
----------

This is a JungleDisk online disk that you use as an archive. Old documents and files, backups, archives. Since this data is not on you local disk you are not limited by your machine's capacity. Note that you don't have access to this files
unless you have internet connections. Emergency files and documents should be stored in SyncDisk.

Sum
===

Following the advice and creating a micro account at Unfuddle, creating 3 mailboxes at Rackspace Email and setting up a cca. 8GB online disk at JungleDisk, your monthly running costs are $19 ($9 + $6 + $4). A small price to pay for having a good night sleep, every night.

*********
Passwords
*********

Always use at least semi-strong passwords (at least 8 characters, letters and numbers, etc.)

Never ever keep passwords in plain-text form. Always use a password manager. Seriously.

The easiest way to do it is to use KeePass. It works on all major platforms and is easy to use.

Put it's database into SynxBox and share it with all your colleagues. This way whenever someone adds a new password, others get to see it almost immediately.

***********
Public keys
***********

Using passwords to connect to production servers is bad. Google it a bit, using `Public Key Authentication`_ is several orders of magnitude more secure and convenient.

All developers need to create their personal keys and upload them to SyncDisk.

***********************
Virtual Private Network
***********************

.. toctree::
   :maxdepth: 3

   vpn.rst
   
   
.. URLs for links in content.

.. _Public Key Authentication: http://sial.org/howto/openssh/publickey-auth/
   

