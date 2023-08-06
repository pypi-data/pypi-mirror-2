Schools Plone Theme
===================

Schools Plone Theme is a free Theme for Plone 4.

Features
--------

* Carousel Banner
 
  Schools Plone Theme can contain carousel banner(s) on the front page. Changeable set of rotating banners can be added to 
  the Schools's front page with help of Products.Carousel, that is installed automatically with quintagroup.theme.schools. 
  Banner images rotate every several seconds, besides site visitor can browse any of them by covering the corresponding pager.

  To create a banner on the front page - go to the 'Configure banners' menu in the task bar. Set carousel options and select 
  'Carousel Banner' from 'Add new...' drop-down menu. Upload image that will be used as one rotating banner, type its title and 
  text (will be displayed under the image), and provide web address image title will be linked to. Add as many carousel banners
  as you need. 

  There are 4 demo images that might be used as demo banners - see 'src' folder within theme package (quintagroup -> theme -> schools).

* Additional Portlet Manager
 
  New portlet manager was added to the site top right area that allows adding any type of portlet there. There is one static text 
  portlet added to the top area by default theme settings.
 
* Top Area Hight
 
  Schools Plone Theme top area includes logo on a top background image and a portlet manager. Top background image and portlet column 
  should have the same height according to theme design. In case you add more portlets - you should upload higher top background
  image and customize logoWrapperMinHeight property (with default 107px value) that control top area height. All this can be done via 
  ZMI: logoWrapperMinHeight property (ZMI -> portal_skins -> schools_styles -> base_properties), top background image (ZMI -> portal_skins
  -> schools_images -> top_bg.jpg) .  

* Site Width

  Site width can be set by defining pageWidth property value in base_properties (Schools Plone Theme is optimized for 1024px screen width).

* Configurable columns width, defined by 'columnOneWidth' and 'columnTwoWidth' values in base_properties. If you change these fields value
  don't forget to update the corresponding 'columnOneWidthInt' and 'columnTwoWidthInt' values: values in those two cells must be identical
  for proper theme look.
  
Recommended
-----------

This version of Schools Theme was developed and tested on Plone 4 (python-2.6.4, Zope-2.12.10).

Dependency
----------

* Products.Carousel (quintagroup.theme.schools 4.2 was tested with Products.Carousel 2.1b3). 

Home Directory
--------------

http://skins.quintagroup.com/schools

Authors
-------

* Volodymyr Rudnytskyi
* Serhiy Valchuk  
* Taras Peretiatko 

&copy; "Quintagroup":http://quintagroup.com, 2006-2011


