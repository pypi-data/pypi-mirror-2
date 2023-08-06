Configuration and use
=====================

In this part of the dokumentation, I will show you `how to install`_
the package, `how to use`_ it and its default configurations and `how to
configure`_ it for your own needs. 

How to install
------------------

To install it via Buildout, just add it to your buildout.cfg to the
eggs in the buildout part and to zcml in the instance part:

.. code-block:: ini

  [buildout]
  ...
  eggs =
      inqbus.bannerrotation
  
  [instance]
  ...
  zcml =
      inqbus.bannerrotation
      
After that, run buildout:

.. code-block:: sh
   
   ~$ bin/buildout

Finaly, just go to the portal_quickinstaller and install the package.

How to use
----------

During the install process, an empty `banners` folder is created at your
plones siteroot. If you want to use an other folder, instead of
`banners`, just read `how to configure the banner_source_id`_. As long
as this folder is empty, you will see some dummy images. To change
that: simply upload your images into the folder.

You can also use different pictures at different places of your site.
To do this, just add an folder with the choosen
source_folder_id`(Defaultvalue: banners)` into the place where you
want to see other images. Every content at the same hierarchies level
and all of there childs will see, based on acquisition, the images in
the nearest banners folder. If you want to learn more about, how this
is used, `read on here`_.

.. _read on here: details.html#get_active_banners_folder

How to configure
----------------

To specify the portlet for your needs, you can change some of the
properties in `bannerrotation_properties`. You are able to find those
via ZMI at `portal_properties`

.. _how to configure the banner_source_id:

**banner_source_id**
  *string*, containing the id of the folder, used as source folder for
  the images `(Default: banners)`

**enabled**
  *boolean*, enable or disable the viewlet `(Default: true)`
  
**effect**
  *string*, specify the changing effect of the bannerrotation.
  Possible values are: blindX, blindY, blindZ, cover, curtainX,
  curtainY, fade, fadeZoom, growX growY, none, scrollUp, scrollDown,
  scrollLeft scrollRight, scrollHorz, scrollVert, shuffle, slideX,
  slideY, toss, turnUp, turnDown, turnLeft, turnRight, uncover, 
  wipe and zoom. For more information please visit the page of the
  maintainer from `jQuery Cycle Plugin`_ `(Default: fade)`
  
.. _jQuery Cycle Plugin: http://www.malsup.com/jquery/cycle/

**random**
  *boolean*, set to true, if you want to randomize the images. The
  first image will also be choosen randomly, so if you have no
  javascript you will also get so see an another image, every time you
  reload the browser `(Default: false)`

**timeout**
  *int*, specify the time between the imagechanges. The time have to
  be set in milliseconds `(Default: 6000)`

**speed**
  *int*, specify the time of the changinganimation. The time have to
  be set in milliseconds `(Default: 1000)`