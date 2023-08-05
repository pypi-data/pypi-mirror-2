Introduction
============

This package provides a method to configure an application via standard
``.ini`` files. This is convenient for site admins since they are more
likely to be familiar with ini files than with ZCML.


Creating config files
=====================
There are two ways to tell a Zope instance which configuration files to
load: zcml statements and the APPCONFIG environment variable. zcml statements
are processed first, making it possible to override standard configuration.

The zcml syntax looks like this::

  <configure xmlns="http://namespaces.zope.org/zope">
    <include package="z3c.appconfig" file="meta.zcml"/>
    <appconfig file="default.ini" />
  </configure>

This will load the contents of ``default.ini`` and merge it into the
application configuration.

If an APPCONFIG environment variable is set and points to a file
its contents will be merged into the application configuration. This is done
last, allowing you to override application defined defaults. For example::

   $ APPCONFIG=etc/mysite.ini bin/instance fg


Accessing configuration
=======================

The configuration data can be accessed from your code via a IAppConfig utility.
This utility is essentially a standard python dictionary which stores all
configuration data. For example lets use a very simple configuration file::

   [site]
   title = My lovely site

You can access the title from python with code like this::

   from zope.component import getUtility
   from z3c.appconfig.interfaces import IAppConfig

   appconfig=getUtility(IAppConfig)
   print "Site title is: %s" % appconfig["site"]["title"]

