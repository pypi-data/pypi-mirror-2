===========
bda.zeopack
===========

Overview
========

Packs one or more databases/ storages on one or more ZEO-Servers (Zope Database 
Storages on Zope Enterprise Objects Server). 

Compatibility
=============

Tested with eggs releaes of ZODB2 >=3.8 and Zope 2.9, 2.10 (latest) as 
tgz-release.   

Installation
============

Install it using ``easy_install`` or ``zc.buildout``. Example for zc.buildout::

 [buildout]
 parts = zeopack

 [zeopack]
 recipe = repoze.recipe.egg:scripts
 eggs = bda.zeopack
 
If youre using Zope with a version below 2.11 (like 2.10 or 2.9) the buildout 
gets a bit more complex::

 [buildout]
 parts = zope zeopack

 [zope]
 recipe = plone.recipe.zope2install
 url = http://www.zope.org/Products/Zope/2.9.11/Zope-2.9.11-final.tgz
 # url = http://www.zope.org/Products/Zope/2.10.9/Zope-2.10.9-final.tgz
 fake-zope-eggs = true
 additional-fake-eggs = ZEO

 [zeopack]
 recipe = repoze.recipe.egg:scripts
 eggs = bda.zeopack 
 initialization = sys.path.append('${zope:location}/lib/python')
 
Usage
=====

Create a configuration file. If no location is given as first argument 
bda.zeopack consider the file at ``/etc/zeopack.cfg``.

The format of the file follows Python ConfigParser format. It looks like::

 [MY.DOMAIN.TLD_OR_IP_ADDRESS:PORT]
 day = NUMBER_OF_DAYS_TO_KEEP
 storages = 
     STORAGENAME 
     STORAGENAME 

Example::

 [127.0.0.1:8100]
 days = 1
 storages =
     storage1
     storage2
     storage4

 [127.0.0.1:8200]
 days = 7
 storages =
     project1
     project2

 [storage.bluedynamics.com:8100]
 days = 1
 storages =
     root1
     mountr1m1
     mountr1m2
     root2
     mountr2m1
  ...
  
Todo:
=====

* better parsing of argv
* support authentication
* pipe file via stdin instead of filename   

  
Credits
=======

  * Copyright 2008-2010, BlueDynamics Alliance Austria
  
  * Concept and code
    * Jens W. Klein <jens@bluedynamics.com>, Klein & Partner KG

