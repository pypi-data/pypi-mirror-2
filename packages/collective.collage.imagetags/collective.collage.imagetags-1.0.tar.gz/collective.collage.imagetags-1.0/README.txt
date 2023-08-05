Introduction
============
Adds a "Image tags" layout view in Collage to display object images 
tagged with collective.imagetags.

Layouts are registered only for objects providing the following interfaces:

* Products.ATContentTypes.interfaces.IATImage
* Products.ATContentTypes.interfaces.IATNewsItem

A special "Settings" viewlet is added in the Collage viewlet manager to
set the scale to use to show the tagged image.

Extending
=========
To provide this layout to your custom content types just copy the 
code below (as stated in browser/configure.zcml)::

    <browser:page
        name="tags"
        for="<your_interface_here>"
        permission="zope.Public"
        class="collective.collage.imagetags.browser.views.ImageTagsView"
        layer="Products.Collage.interfaces.ICollageBrowserLayer"
        />

If you want to use a special template, add a template "attribute". 
If not, a default template will be used from browser.views.ImageTagsView.

Features
========
- i18n support (English and Spanish translations)
- Tested in Plone 4.0b5 with Collage 1.3.0_b4
- Settings viewlet displays an inline z3c.form to set preferences for the layout
- Depends on Product.Collage and collective.imagetags. They will automatically fetch during buildout and installed during installation of this product.

To do
=====
- collective.collage.imagetags.scales vocabulary should dynamically calculate image scales of every image field in its context.
