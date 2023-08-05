===========
aws.pdfbook
===========

Description
===========

``aws.pdfbook`` is a product that adds a new style to a Plone 3.x portal.  It
creates a new skin selection to the 'portal_skins' tool (called PDFBook), and
registers a custom stylesheet (called pdfbook.css) with the 'portal_css' tool.


Requirements
============

The following softwares should be installed:

* Plone 3 or 4
* recode (optional)
* htmldoc (required)

Installation
============

In your ``buildout.cfg`` file::

  [buildout]
  ...
  eggs =
    ...
    aws.pdfbook

* The site charset is ``utf-8``
* The server buffer for downloading has 40000 bytes.

.. note::

   increasing the buffer size may speed up download but at the expense of a
   bigger memory footprint.

Otherwise you can change these default values in your ``zope.conf`` or in
``buildout.cfg`` like this::

  [instance]
  recipe = plone.recipe.zope2instance
  ...
  zope-conf-additional =
    ...
    <product-config pdfbook>
    # Your site charset (default: utf-8)
    site-charset utf-8
    # The download buffer bytes size (default: 40000)
    download-buffer-size 40000
    </product-config>
    ...

In Plone go to the 'Site Setup' page and click on the 'Add/Remove Products'
link.

Choose ``aws.pdfbok`` (check its checkbox) and click the 'Install' button.

The go **as soon as possible** to the **PDF Book** configuration panel and
configure according to your system settings and your layout preferences.

More particularly, you may change default ``pdfbook`` options. See the `pdfbook
documentation <http://www.htmldoc.org/documentation.php/toc.html>`_ for the
various available options.

Other setups
------------

It is strongly recommanded to use linking with UID in your visual editor
preferences. Otherwise images may not display in topics prints.

Developers
==========

Add a template for your content types.

Assuming you have a personal content type that implements the
``myproduct.interfaces.IMyContentType`` interface, You must add a view like this one::

  <browser:page
     name="printlayout"
     for="myproduct.interfaces.IMyContentType"
     layer="aws.pdfbook.interfaces.IAWSPDFBookLayer"
     permission="zope.Public"
     template="templates/mycontenttype.pt"
     />

Keep the following attributes as above:

* ``name="printlayout"``
* ``layer="aws.pdfbook.interfaces.IAWSPDFBookLayer"``
* ``permission="zope.Public"``

Examples for standard content types are provided in the
``browser/transformers.zcml`` configuration and associated files.

Otherwise ``aws.pdfbook`` provides a default template that may or may not fit
with paper layout.

If the default layout for personal or third party content types is somehow
awful, you may blacklist such content types in the configuration panel.

To do
=====

This version is still alpha. Thus has some todos like:

* unit tests to add
* internationalize and translate the forms
* cleanup old useless code from ``Products.PDFBook`` by John Doe.

Credits
=======


* Original version for Plone 2.x by `John Doe <john.doe@dev.null>`_
* Plone 3.x support by `Gilles Lenfant <mailto:gilles.lenfant@amterway.fr>`_ for
  `Alter Way Solutions <http://www.alterway.fr>`_
* Sponsored by `Materis <http://www.materis.com/>`_

.. image:: http://www.materis.com/template/imgs_fr/logo.gif
   :align: center
