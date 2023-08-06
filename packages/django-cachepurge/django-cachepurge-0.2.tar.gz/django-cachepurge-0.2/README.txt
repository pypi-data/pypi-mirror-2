=================
django-cachepurge
=================

.. contents::

What is it?
===========

This package allows django to purge HTTP cache when a model instance is changed
or deleted. It does this by sending "PURGE" requests to one or more upstream
HTTP cache (such as Squid or Varnish). This is inspired by Plone CacheFu
components.

Usage
=====

In settings.py put 'django_cachepurge' before any other application; else it may
fail to register some models::

      INSTALLED_APPS = (
         'django_cachepurge',
         ...
      )

Add the middleware::

     MIDDLEWARE_CLASSES = (
         ...
         'django_cachepurge.middleware.CachePurge',
     )

Define CACHE_URLS::

      CACHE_URLS = 'http://127.0.0.1:3128'

or if you have more than one cache::
       
      CACHE_URLS = ('http://127.0.0.1:3128',
                    'http://192.168.1.42:3128')

Models
------

Urls are extracted from models instances on post_save signal. Two sources are
used:

 - instance.get_absolute_url(), if it exists
 - instance.get_purge_urls(), if it exists. The application expects a list of
   absolute paths similar to what is provided by get_absolute_url().

Purge request is sent when response has been computed: if an exception occurs
the urls are not purged. Purge requests are asynchronous: worker threads handle
that so that we don't have wait to complete all requests before returning the
response.

Cache configuration
-------------------

The cache must be configured to accept and handle "PURGE" requests from the
server where the django application is hosted.

Homepage, code, bug tracker
---------------------------

- Homepage: http://launchpad.net/django-cachepurge
- Code repository: http://code.launchpad.net/django-cachepurge
- Report bugs at http://bugs.launchpad.net/django-cachepurge

