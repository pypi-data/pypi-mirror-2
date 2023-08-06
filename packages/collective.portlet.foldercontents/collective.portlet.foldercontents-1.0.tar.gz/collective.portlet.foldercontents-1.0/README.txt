Introduction
============

This package provides a portlet that lists your folder contents.


Overview
--------

The ``collective.portlet.foldercontents`` package adds a new Plone site portlet
called ``Folder Contents``. It gives you the ability to list contents of the folders
in your site. It also provides a way to display images which can be selected from 
your site content. And a bit more... See below for details.


Compatibility
-------------

This add-on was tested for Plone 3 and Plone 4.


Installation
------------

* to add the package to your Zope instance, please, follow the instructions found inside the
  ``docs/INSTALL.txt`` file
* then restart your Zope instance and install the ``Folder Contents portlet``
  package from within the ``portal_quickinstaller`` tool


Portlet Usage
-------------

The ``Folder Contents`` portlet owns a bunch of fields. Here we explain how it 
works, including the fields relations:

* ``Folder title as a portlet header``. If selected, the referenced folder title
  will be used as a portlet header, and the field ``Header`` will be ignored.
* ``Header``. Specifies the portlet header. If above option is selected then this
  field will be ignored.
* ``Folder description as a portlet body``. If selected, the referenced folder
  description will be used as a portlet body, and the field ``Portlet Body``
  will be ignored.
* ``Portlet Body``. Specifies portlet body. If above option is selected then
  this field will be ignored.
* ``Select folder``. You have to select folder from drop-down menu and portlet
  will display contents of this folder. If you don't see any folders there then
  you probably don't have any folders in your site. Also you may use search box
  to find required folder. Finally don't forget to press Apply button.
* ``Number of folder items to show``. Specifies the number of items to
  display in folder listing. Set 0 to show all items.
* ``Image``. If you need to display image in a portlet above folder listing then
  here you may select an image previously added in your site.
* ``Image Scale``. Specifies image scale for image selected in the field
  'Image'. You can specify here a specific custom scale that is defined in your
  custom content type of standard one that goes with Plone by default.
* ``Default Image Scale List``. Here you can pick one of the available scales.
  It will be used only if ``Image Scale`` field is empty. This field is only
  available in Plone >= 4 version where we have 'Imaging' control panel.
* ``HTML Class Name``. Specifies html class for portlet wrapper element. Usefull
  for custom portlet styling so that you can apply different styles for your
  folder contents portlets.
* ``More link``. If checked, '...more' link pointing to selected folder will
  be shown in portlet.


Live Examples
=============

* http://www.eatingdisordertreatment.net/
* http://www.eatingdisordertreatment.com/


Credits
=======


Companies
---------

|martinschoel|_

* `Martin Schoel Web Productions <http://www.martinschoel.com/>`_
* `Contact us <mailto:python@martinschoel.com>`_


Authors
-------

* Vitaliy Podoba <vitaliy@martinschoel.com>
* Sergiy Krasovkiy


Contributors
------------


.. |martinschoel| image:: http://cache.martinschoel.com/img/logos/MS-Logo-white-200x100.png
.. _martinschoel: http://www.martinschoel.com/
