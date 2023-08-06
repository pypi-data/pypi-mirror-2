Installing Django-groupcache
============================

Requirements
------------

``Django-groupcache`` requires ``Django >= 1``, and ``Python >= 2.5``
(Python 3 is not supported at this time).


Getting the Code
----------------

Using Setuptools
^^^^^^^^^^^^^^^^
If you have the `setuptools <http://pypi.python.org/pypi/setuptools>`_
package on your system, Django-groupcache is listed on `PyPI
<http://pypi.python.org/pypi/django-groupcache>`_, so getting the
latest stable code is as easy as doing, from the command line::

     easy_install django-groupcache

Using Mercurial
^^^^^^^^^^^^^^^
If you'd rather have the latest code, you can get it from the
`repository on Bitbucket
<https://bitbucket.org/syfou/django-groupcache>`_ using `Mercurial
<http://mercurial.selenic.com/>`_::

     hg clone https://bitbucket.org/syfou/django-groupcache

You will end up with a directory hierarchy looking like this::

     django-groupcache/
         docs/
         groupcache/
         MANIFEST.in
         README.rst
         setup.py

If you have ``setuptools``, you could then invoke, from the
``django-groupcache`` directory::

     python setup.py install

And having ``Django-groupcache`` available system-wide (as the
:mod:`groupcache` module). Alternatively, it's perfectly fine to just
copy (or link to) the ``groupcache`` directory to (from) the top of your
Django project.

Integrating to your Project
---------------------------
Once you got the code, using it is as simple as adding the reusable
:mod:`groupcache` app to your your ``INSTALLED_APPS`` settings::

    INSTALLED_APPS = (
        'django.contrib.auth',
        'django.contrib.contenttypes',
        ...
        'groupcache',   # <= The groupcache reusable app
        ...
    )

And you are done! There is no model to install, so performing
a database synchronization (``syncdb``) is not needed.

Of course, ``Django-groupcache`` is build on top of the `Django's
cache framework
<http://docs.djangoproject.com/en/dev/topics/cache/>`_. This means you
still have to configure the latter to suit your specific requirements
(``CACHE_BACKEND``, ``KEY_PREFIX``, etc), and all the settings will
apply, but it was carefully coded not to introduce any side-effects to the
expected cache behavior.

From there, you can :doc:`start using it <api>`.
