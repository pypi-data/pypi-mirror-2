Introduction
============

inqbus.bannerrotation simple, ajax based bannerrotation viewlet for
plone. It uses the jQuery Cycle Plugin and its original implementation
can be found here: http://jquery.malsup.com/cycle/

The Viewlet automaticly take the images out of a predefined folder
`(Default: banners)`. This have the benifit to define several
bannerrotations for several parts of the website. Just add another
banners folder at the possition you want. It automaticly takes the
next bannersfolder, he find upwards the way to plonesites root folder.

Installing
==========

Installing without buildout
---------------------------

Install this package in either your system path packages or in the
lib/python directory of your Zope instance. You can do this using
either easy_install or via the setup.py script.

Installing with buildout
------------------------

If you are using `buildout_`, just add it to your eggs and your zcml
in the instance part:

    [instance]
    eggs = inqbus.bannerrotation
    ...
    zcml = inqbus.bannerrotation

inqbus.bannerrotation use a z3c.form view for the configlet. To make
sure you get the right versions, you might want to add the following
into your buildout.cfg to:

    [buildout]
    ...
    extentds =
    ...
    http://good-py.appspot.com/release/plone.app.z3cform/0.5.0

Now, just run ''bin/buildout'' in your instance rootfolder to
get the package and all of it dependencies. You can now install it via
the quickinstaller.

.. _buildout: http://pypi.python.org/pypi/zc.buildout

Configuration
=============

At the moment, there are two ways to configure the viewlet. The first
and more comfortable way is to go to plone control_panel and choose
'Bannerrotation Viewlet'. The other way to configure it is via a
propertysheet, which can be found in the ''Zope Management Interface''
under 'portal_properties' > 'bannerrotation_properties'.

You are able to edit the following parameter:

**Effect**
    Specify the effect while changing the image. There are 28 possible
    values. `(Default: fade)`   
**Timeout**
    Specify the time between the imagechanges in milliseconds.
    `(Default: 6000)`
**Speed**
    Specify the animationspeed in milliseconds. `(Default: 1000)`
**Enabled**
    Enable or disable the bannerrotation `(Default: True)`
**Random**
    Enable or disable randomization of the images. `(Default: False)`
    
The following option is only editable via ZMI:

**banner_source_id**
    Define the id of the folder, that should be taken as sourcefolder.
    `(Default: banners ~ this folder is automaticly created )`

Copyright and Credits
=====================

jQuery Cycle is developed and maintained by M. Alsup and is
dual-licensed under MIT and GPL: http://jquery.malsup.com/cycle/

The Author of inqbus.bannerrotation: Max Brauer (max.brauer@inqbus.de)