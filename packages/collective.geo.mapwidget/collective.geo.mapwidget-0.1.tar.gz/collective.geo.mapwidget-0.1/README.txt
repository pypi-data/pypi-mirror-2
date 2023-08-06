Introduction
============

collective.geo.mapwidget provides some handy page macros and adapters to easily manage
multiple maps on one page.


Requirements
------------
* Plone >= 4.0
* plone.app.z3cform
* collective.z3cform.colorpicker
* collective.geo.openlayers
* collective.geo.settings

Installation
============
You can install collective.geo.mapwidget as part of a specific project's buildout, by having a buildout configuration such as: ::

        [buildout]
        ...
        eggs = 
            collective.geo.mapwidget
        ...
        [instance]
        ...
        zcml = 
            collective.geo.mapwidget

Install this product from the Plone control panel.


Contributors
============

* Gerhard Weis - gweis
* Giorgio Borelli - gborelli
* Silvio Tomatis - silviot
* David Breitkreutz - rockdj
