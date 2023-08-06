Introduction
============

Integration of `jQuery virtual tour`_ in Django.

One model stores panoramic photo while a number of other models represents
clickable areas in the panorama. Included areas can show HTML block (using
tinymce) or display another url in a iframe.

gisa.buildingmaps integrates with this application giving one extra area to
allow navigating locations (virtual tour experience).

Install
=======
- Install django-panorama egg with pip, buildout, or whathever
- Add 'panorama' to your INSTALLED_APPS
- Add panorama urls to your project urls:
	(r'^panoramas/', include('panorama.urls')),
- Run syncdb
- Overwrite panoramas default template: templates/panorama/base.html

This app uses django-multilingual. For this to work, you need to define
available languages in your settings.py. Example:
	LANGUAGES = (
	  ('en', 'English'),
	  ('eu', 'Euskara'),
	  ('es', 'Castellano'),
	)

	DEFAULT_LANGUAGE = 1 # for django-multilingual, set first language (eu) as default

Usage
=====

To show a panorama model in templates:

    {% load panorama %}
    {% show_panorama panorama_object %}

You can also define a starting position to the panorama, in pixels from the
right:

    {% show_panorama panorama_object 100%}


.. _jQuery virtual tour: http://www.openstudio.fr/jQuery-virtual-tour.html?lang=en
