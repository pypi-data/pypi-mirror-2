Django-Multihost -- A simplified, flexible Django multi-host app
================================================================


Overview
--------

Django-Multihost is a Django middleware that overrides Site ORM functionality and gets the current Site from the Host header.  The code is loosely based on the work done by Bruce Kroeze here: `django-threaded-multihost <http://bitbucket.org/bkroeze/django-threaded-multihost/>`_.


Description
-----------

The MultiHostMiddleware class contained in this app has 2 tasks:

#.  Upon middleware __init__(), it overrides SiteManager.get_current() with a multihost-aware version that reads the ``Host`` header from the request and attempts to find a matching Site (caches it if cache is enabled).
#.  Upon middleware process_request(), it sets the request into ``threadlocal`` storage and then uses the new SiteManager.get_current() functionality to retrieve the Site matching the ``Host`` header and sets it into the request instance.  If a match is not found and MULTIHOST_AUTO_WWW is True (the default), it will attempt to modify the ``Host`` URL  to add/remove ``www.`` and attempt the lookup again.  If it still doesn't find a matching Site, it redirects to ``MULTIHOST_REDIRECT_URL``.


Requirements
------------

- Python 2.6 (May work with 2.3+, but untested - please report)
- Django 1.2.x (May work with 1.0+, but untested - please report)


Installation
------------

#. Copy or symlink the ``multihost`` package into your django project directory or install it by running one of the following commands:

    ``python setup.py install``

    or

    ``pip install django-multihost``
    
    or

    ``easy_install django-multihost``

#. Add ``MULTIHOST_REDIRECT_URL`` to ``settings.py``

#. Add ``multihost.middleware.MultiHostMiddleware`` to your ``MIDDLEWARE_CLASSES`` in at the end of the list.  If you find it isn't working, move it up the list order as there may be a middleware conflict.


Advanced Settings
----------------------

There are 4 settings that developers can use to override default functionality:

- ``MULTIHOST_REDIRECT_URL``: **required**; no default.  The default middleware request processing will redirect to this URL in the case of Site lookup failure.
- ``MULTIHOST_AUTO_WWW``: optional; defaults to True.  If the Site can't be found that matches the incoming Host header exactly, this will automatically try removing/adding ``www.`` and searching again.


Source
------

The latest source code can always be found here: `github.com/jaddison/django-multihost <http://github.com/jaddison/django-multihost/>`_


Credits
-------

Django-Multihost is maintained by `James Addison <mailto:code@scottisheyes.com>`_.


License
-------

Django-Multihost is Copyright (c) 2010, James Addison. It is free software, and may be redistributed under the terms specified in the LICENSE file. 


Questions, Comments, Concerns:
------------------------------

Feel free to open an issue here: `github.com/jaddison/django-multihost/issues <http://github.com/jaddison/django-multihost/issues/>`_