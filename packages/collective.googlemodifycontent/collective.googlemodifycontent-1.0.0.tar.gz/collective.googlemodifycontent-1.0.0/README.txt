GoogleModifyContent
===================


About GoogleModifyContent
-------------------------

GMC extends the Plone content Edit function by adding the GoogleModify operation,
which only applies to documents stored on Google servers. 

GMC embeds the Google Docs application inside the Google Modify panel, allowing Plone users
to edit their documents directly from the Plone application.


Copyright and license
---------------------

Copyright (c) 2009 Federica D'Elia

This software is subject to the provisions of the GNU General Public License,
Version 2.0 (GPL).  A copy of the GPL should accompany this distribution.
THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
FOR A PARTICULAR PURPOSE

See the `LICENSE` file that comes with this product.


Requirements
------------

FileSystemStorage, GoogleAuthentication, GoogleSystemStorage and gdata-1.3.0
must be correctly installed.


Installation
------------

With buildout
-------------

This example speaks of itself::

  [buildout]
  parts =
     ...
     fss
  
  ...
  
  eggs =
      ...
      collective.googlesystemstorage
      collective.googleauthentication
      collective.googlemodifycontent
      iw.recipe.fss
      iw.fss
      ...
  
  ...
  
  zcml =
      ...
      collective.googlesystemstorage
      collective.googleauthentication
      collective.googlemodifycontent
      iw.fss
      iw.fss-meta
  
  ...
  
  [fss]
  recipe = iw.recipe.fss
  zope-instances =
       ${instance:location}
  
  storages =
      global / flat
      portale /portale site1 ${buildout:directory}/var/portale_fss_storage ${buildout:directory}/var/portale_fss_backup

  
Credits
-------

Main developer: D'Elia Federica <federica.delia@redturtle.it>
