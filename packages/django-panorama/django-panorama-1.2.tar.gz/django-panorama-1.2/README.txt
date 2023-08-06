Introduction
============

Integration of `jQuery virtual tour`_ in Django.

One model stores panoramic photo while a number of other models represents
clickable areas in the panorama. There are currently three types of
clickable areas:

Panorama Link
    Link to another panorama, to allow virtual tour navigation.
Note
    Show a ajax popup with HTML block (using tinymce)
External link
    Display another url in a iframe.

Install
=======

- Install django-panorama egg with pip, buildout, or whatever.
- Add 'panorama' to your INSTALLED_APPS
- Add panorama urls to your project urls: ``(r'^panoramas/', include('panorama.urls')),``
- Run syncdb
- Overwrite panoramas default template: templates/panorama/base.html

This app uses django-multilingual-ng and django-tinymce. They must be
installed and configured for this app to work.

Migrations
----------

If you are upgrading from 1.1 or before, database migration is required.

Django-panorama uses South to keep in sync database and models, so it's
recommended to add 'south' to your INSTALLED_APPS.

Settings
========

No required configuration. There are some optional configuration
parameters to control behaviour of panorama display. You can place the
following variables in your project's settings.py:

PANORAMA_VIEWPORT_WIDTH
    Width of the panorama window

    Value: width in pixels.
    Default: 600

PANORAMA_SPEED
    Speed of the panorama rotation.
   
    Value: number; higher values means slower :-P
    Default: 20000

PANORAMA_DIRECTION
    Starting direction of the rotation.
   
    Value: ['left','right']
    Default: 'left'

PANORAMA_CONTROL_DISPLAY
    Display rotation controls?
   
    Value: ['auto', 'yes', 'no']
    Default: 'auto'

PANORAMA_START_POSITION
    Starting position of the panorama.
   
    Value: position in pixels.
    Default: 0

PANORAMA_AUTO_START
    Start rotation automatically?
   
    Value: True, False
    Default: False

PANORAMA_MODE_360
    Loop over the panorama?
   
    Value: True, False
    Default: True

Integration
===========

To show a panorama model in templates::

    {% load panorama %}
    {% show_panorama panorama_object %}

Javascript
----------

This app needs the following javascript libraries loaded: jquery, jquery.panorama,
jquery.fancybox and jquery.advanced-panorama. All are bundled with this
app; to load the first three you can use the panorama_js templatetag::

    {% panorama_js %}

jquery.advanced-panorama case is different, it's loaded automatically and
resides in ``/static/panorama/js/jquery.advanced-panorama.js``.

Admin interface uses OpenLayers, also bundled with this app. Can be
found in ``/static/panorama/js/OpenLayers.js``.

CSS
---

Sample css and media is provided. Load with::

    <link rel="stylesheet" href="{{STATIC_URL}}panorama/jquery.panorama.css" />
    <link rel="stylesheet" href="{{STATIC_URL}}panorama/jquery.fancybox-1.3.4.css" />

Configuration
-------------

Configuration options can be overwritten through context. For example::

    {% with position=800 viewport_width=400 %}
        {% show_panorama panorama_object %}
    {% endwith %}


.. _jQuery virtual tour: http://www.openstudio.fr/jQuery-virtual-tour.html?lang=en
