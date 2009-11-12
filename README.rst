================
django-wellknown
================

Django application to provide easy administration of site-meta URIs. Includes robots.txt and crossdomain.xml.

http://tools.ietf.org/html/draft-nottingham-site-meta-03 

Requirements
============

python >= 2.5

django >= 1.0

django-robots (optional)

Installation
============

Be sure to add ``wellknown`` to ``INSTALLED_APPS`` in settings.py. Additionally, add the following entry to urls.py::

	urls(r'^', include('wellknown.urls')),

Run ``./manage.py syncdb``

Usage
=====

Preload cache
-------------

To load well-known URIs stored in the database::

	import wellknown
	wellknown.init()



django-robots
-------------

wellknown will defer to `django-robots <http://bitbucket.org/jezdez/django-robots/>`_ if it is installed. To use django-robots to render robots.txt, add ``robots`` to ``INSTALLED_APPS`` in settings.py. wellknown will take care of the rest.
