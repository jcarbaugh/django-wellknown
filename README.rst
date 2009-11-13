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

Register resources
------------------

::

	import wellknown
	wellknown.register('host-meta', ...)

The first argument is the path that will be exposed for the resource. A path of ``host-meta`` will map to::

	http://example.com/.well-known/host-meta

At least one of the following arguments is required:

* ``content``: a string or unicode representation of the resource, cached on startup
* ``template``: the path to a template that will be rendered for the resource, rendered and cached on startup
* ``handler``: a handler method that will be used to render the resource, invoked on each request

Handler methods must have the following signature and return a string or unicode object::

	def handler(request, *args, **kwargs):
		pass

The register method takes one optional parameter, ``content_type``. This is the content type that will be used to return the rendered resource. The following rules are used to determine the content_type to use:

#. if a content_type parameter was passed to register, use it
#. attempt to infer content_type from the path using the mimetypes package
#. use ``text/plain`` if no content_type can be guessed

Model resources
---------------

Resources may be stored in the database to make it easy for non-technical users to edit. The following fields are available on a Resource:

* ``path``: the path that maps to the resource
* ``content``: the content that will be served when the resource is requested
* ``content_type``: the content_type with which the content will be returned, defaults to ``text/plain``

When a resource is saved, it is updated in the cache. To load resources into the cache at run-time::

	import wellknown
	wellknown.init()

This method should be called once when the web application is started.

django-robots
-------------

wellknown will defer to `django-robots <http://bitbucket.org/jezdez/django-robots/>`_ if it is installed. To use django-robots to render robots.txt, add ``robots`` to ``INSTALLED_APPS`` in settings.py and wellknown will take care of the rest.
