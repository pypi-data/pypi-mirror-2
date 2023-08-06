Introduction
============
This is a very small and lightweight integration of OpenLayers and collective.geo.mapwidget.
Idea is to have a map content type to create full customizable maps with the collective.geo flexibility.
And the final goal is to store some javascript boilerplate on a content type to initiliaze the map.

As it requires writing some javascript with OpenLayers and jquery, it is not an 'end user' solution but a convenient and flexible way to integrate OpenLayers in plone.

.. contents::

Installation
============
Just a simple easy_install collective.geo.geopoint is enough.
Alternatively, buildout users can install collective.geo.geopoint as part of a specific project's buildout, by having a buildout configuration such as: ::

        [buildout]
        ...
        eggs =
            collective.geo.mapcontent
        ...
        [instance]
        ...
        zcml =
            collective.geo.mapcontent

How to use
===============
In the plone interface, just add a map.
Your mapid is : **mapcontent**.
Then, fill some javascript inside the content type 'javascript' text area to display the map using mapwidget::

    - set the box width and height
    - set the long/lat/zoom settings
    - set the layers

EG::

     jq('#mapcontent').css('height', '1024px');
     jq('#mapcontent').css('width', '1024px');
     var coords = {lon: 0.000000, lat: 0.000000, zoom: 10};
     cgmap.state = {'default': coords, 'mapcontent': coords};
     cgmap.extendconfig(
       {layers: [function() {
       return new OpenLayers.Layer.WMS("OpenLayers WMS",
                                       "http://vmap0.tiles.osgeo.org/wms/vmap0",
                                       {layers: 'basic'});}
                ]
       }, 'mapcontent');

Mapwidget will initialize the map with those settings for you.
And, remember, you are working with mapwidget.
This one wraps OpenLayers and here are some usefull tips:

    - :`cgmap.config['mapcontent'].map`: the current OpenLayers map instance
    - :`cgmap.config['mapcontent'].layers`: the list of function callbacks returning a layer
    - :`cgmap.state['mapcontent']`: the current long/lat/zoom settings (js mapping).

If you need to control the map afterwards, just register something when  document is ready.
EG::

     // add this in the /edit js textarea
     jq(document).ready(function() {
         cgmap['config']['mapcontent'].map.DOSOMETHING();
     });

Credits
==========
Companies
----------
|makinacom|_

  * `Planet Makina Corpus <http://www.makina-corpus.org>`_
  * `Contact us <mailto:python@makina-corpus.org>`_


Authors
----------
  - kiorky <kiorky@cryptelium.net>

Contributors
------------

.. |makinacom| image:: http://depot.makina-corpus.org/public/logo.gif
.. _makinacom:  http://www.makina-corpus.com

