=====================
 anz.cas README
=====================

:author:    jiangdongjin
:contact:   eastxing@gmail.com
:date:      2010/07/09
:abstract: This is an Python implementation of the server-end of JA-SIG's
           CAS `protocol <http://www.jasig.org/cas/protocol>`_, providing
           a cross-domain single sign-on solution for web applications.

.. contents::
.. sectnum::

Introduction
============
anz.cas implement a new PAS plugin 'Anz Central Auth Service'. It enabling
you to turn your Plone site into a CAS server.

Overview
========
**anz.cas gives you:**

- A stand-alone central login page where the user enters their credentials.
- A mechanism for validating the user's credentials against various
  backends (make use of PAS's authentication plugins).
- A back-end validator where CAS-enabled client applications connect to
  check whether the current user is authenticated (if the user has already
  been authenticated with the CAS server, then they are permitted to
  proceed, otherwise they are redirected to the CAS server's login page for
  authentication).
- Almost full compatibility with the open, multi-platform CAS protocol.

**Why you would want/need this:**

- CAS allows you to share authentication across domains.
- The user only sees the login page once -- the first time they try to
  access any one of your CAS-protected services, and never again until
  they log out or their single-sign on session expires.
- Client applications never see the user's actual credentials.

Credits
========
Thanks to those guys who developed the following products, without your
works anz.cas will never happen.

- CAS_

.. _CAS: http://www.jasig.org/cas

Comparison with JA-SIG's CAS
============================

Advantages
----------
- anz.cas is designed to be simple to set up and configure by a Zope/Plone
  user (which is quite the opposite from it's popular official java cousin,
  the JA-SIG CAS Server).
- With JA-SIG CAS Server, you should do more work to integrate your
  Zope/Plone sites with it. With anz.cas you can reduce your software stack.
- You can make full use of now existed PAS authentication plugins to do
  authenticate work for you.

Disadvantages
-------------
- As the official implementation, JA-SIG CAS Server is stable, solid and
  popular used. anz.cas is in the opposite, I hope you guys can give me
  some feedbacks to make it better :).

Requirements
============
- Plone 3.0 or later
- ZODB3>=3.8.3 (test under 3.8.3 only)
- zope.proxy>=3.4.1 (test under 3.4.1 only)
- zope.bforest
- uuid

Installation
============
To install anz.cas into the global Python environment (or a
workingenv), using a traditional Zope 2 instance, you can do this:

* When you're reading this you have probably already run 
  ``easy_install anz.cas``. Find out how to install setuptools
  (and EasyInstall) here:
  http://peak.telecommunity.com/DevCenter/EasyInstall

* Create a file called ``anz.cas-configure.zcml`` in the
  ``/path/to/instance/etc/package-includes`` directory.  The file
  should only contain this:

::

    <include package="anz.cas" />

Alternatively, if you are using zc.buildout and the
plone.recipe.zope2instance recipe to manage your project, you can do this:

* Add ``anz.cas`` to the list of eggs to install, e.g.:

::

    [buildout]
    ...
    eggs =
        ...
        anz.cas
       
* Tell the plone.recipe.zope2instance recipe to install a ZCML slug:

::

    [instance]
    recipe = plone.recipe.zope2instance
    ...
    zcml =
        anz.cas
      
* Re-run buildout, e.g. with:

::

    $ ./bin/buildout
        
You can skip the ZCML slug if you are going to explicitly include the
package from another package's configure.zcml file.

Then go into your Plone site install "anz.cas" product by quick_installer
or portal_setup.

How to use anz.cas
==================
anz.cas is designed to be easy to set up and customize.

Create a Plone site as 'CAS Server'
-----------------------------------
For the security consideration, I strongly recommend you to create an
dedicated Plone site to serve as a 'CAS Server'. In this site you should
install 'anz.cas' and configure it. Assume the site named 'cas'.

Setting up your Plone site behind Apache with SSL
-------------------------------------------------
As the CAS protocol, for the security consideration, all the communication
with CAS Server are over SSL. How to do that is out of the scope,
`this <http://plone.org/documentation/kb/apache-ssl/>`_ doc will guide you.

**Note:**
You can left this behind now, go through the following steps to
experience anz.cas quickly.

Customize central login page
----------------------------
anz.cas use Plone stock **login_form** as the central login page, you can
skinned it whatever you want.

Configure your authentication mechanism
---------------------------------------
anz.cas make use of PAS authentication plugins to do authenticate work, so
you can configure PAS to act as you want.

Create 'Anz Central Auth Service' plugin
----------------------------------------
Go to ZMI \\cas\\acl_users, add an 'Anz Central Auth Service'
instance, choose any Id you like, we input 'anz_cas' for example.

Configure 'Anz Central Auth Service' plugin
-------------------------------------------
1. Go to \\cas\\acl_users\\anz_cas, in 'Active' tab active the only one
   interface -- IChallengePlugin.

   Click 'Challenge' to configure 'Challenge Plugins', move 'anz_cas'
   to the top.

2. Go to 'Properties' tab to configure CAS related properties. 

==============  ===========  ==============  ==============================
Property        Required     Default value   Note
requireSecure   False        True            Boolean variable denoting
                                             whether secure connection is
                                             required or not.

                                             **Note:**
                                             If you want to experience
                                             anz.cas under non-ssl
                                             environment, you should set it
                                             to False.
loginPagePath   True         login_form      Where to send people for
                                             logging in, default is
                                             Plone's stock 'login_form'.
==============  ===========  ==============  ==============================

Services Management
-------------------
By default there are no restrictions and any service at any URL may
authenticate via CAS. This may be undesirable for a number of reasons, so
anz.cas provides a Services Management administrative tool to control what
services may use the CAS server and in particular what those services can
do with CAS.

- In 'Services' tab list all the current registered services, you can
  choose several or all of them to remove.
- Click 'Add a service' link to register a new service.

================  ========  =============  ================================
Field name        Required  Default value  Note
ID                True                     An identify of the registered
                                           service, it must equal to
                                           **serviceUrl** configured in
                                           CAS client. CAS will redirects
                                           to here after login.
Name              False                    Name of the registered service.
Description       False                    Description of the registered
                                           service.
Enabled           False     True           If this service currently
                                           allowed to use CAS?
SSO Enabled       False     True           If this service participate in
                                           the SSO session?
Anonymous Access  False     False          If the service is allowed
                                           anonymous or privileged access
                                           to user information?
Allowed to Proxy  False     True           If this application allowed to
                                           participate in the proxying
                                           capabilities of CAS?
================  ========  =============  ================================

- Click a registered service's id to modify it.

**Note:**
If no registered services, there are no restrictions and any service at any
URL may authenticate via CAS.

Configure CAS client
--------------------
Configure the **casServerUrlPrefix** of your CAS clients to our new added
plugin instance, eg.
https://{your cas server domain}:{port}/cas/acl_users/anz_cas.

Security Policy
===============
anz.cas uses tickets to implement supported authentication protocols, so it
follows that ticket behavior determines most aspects of security policy. In
current implementation, anz.cas provides for the following:

- Ticket-granting tickets (TGT) that expire after more than 2 hours from
  its creation time.
- One-time-used service tickets (ST) that must be validated within 5
  minutes.

More security policy will be added later.

ToDo
====
- Add automation tests ( I really don't know how to automation test this
  kind of package :) )
- More compatibility with CAS protocol.
