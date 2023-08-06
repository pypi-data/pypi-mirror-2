Introduction
============

.. image:: http://keul.it/images/plone/monet.mapsviewlet-0.5.0-02.png
   :alt: Monet Citypass preview
   :align: left
   :target: http://keul.it/images/plone/monet.mapsviewlet-0.5.0-01.png

Every Plone content, with a "*Location*" data can display a Google's Map inside a viewlet. The location data
must be a valid address that Google Maps service can understand (like "*Piazza Grande, Modena, Italy*").

The viewlet is placed (by default) below the content.

To finally enable the map you need also to access a new option under the "*Action*" menu. Use this
same option to disable the map.

You need to `configure the Google Key`__ in the *googlemaps_key* property under the *monet_properties*
sheet (added when you'll install the product).
If your Plone site can be reached from more than one hostname, add a key for every possible ones.

__ http://code.google.com/apis/maps/signup.html

KML
---

Also you can handle `KML`__ file using again the Google APIs.
You must simply add Plone files with KML extensions to the **related contents** section of a document
where the map is enabled.

__ http://code.google.com/apis/kml/documentation/whatiskml.html

When you have KML data to show, you can also use a new portlet that will help users to enable/disable
single KML data from the map.

.. Note::
   You can use and test KML features only with online site. When working locally all KML features simply
   don't work.

Other products
==============

Take a look also to `Maps`__ for basic Google Maps integration.

If you need something more professional (also with KML support) don't miss the `collective.geo`__ suite! 

__ http://plone.org/products/maps
__ http://plone.org/products/collective.geo/

Credits
=======

Developed with the support of `Rete Civica Mo-Net - Comune di Modena`__;
Rete Civica Mo-Net supports the `PloneGov initiative`__.

.. image:: http://www.comune.modena.it/grafica/logoComune/logoComunexweb.jpg 
   :alt: Comune di Modena - logo

__ http://www.comune.modena.it/
__ http://www.plonegov.it/

Authors
=======

This product was developed by RedTurtle Technology team.

.. image:: http://www.redturtle.it/redturtle_banner.png
   :alt: RedTurtle Technology Site
   :target: http://www.redturtle.it/

