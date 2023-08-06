Django-groupcache at a Glance
=============================

The Problem
-----------
Django has fair, straightforward caching support for views. Let's
say you have a `Book` model like this one::

   from django.db import models

   class Book(models.Model):
      author = models.CharField(max_length = 100)
      title  = models.CharField(max_length = 200)

Let's also say you wrote a view to display it, called `view_book`. It's
straighforward to apply the `cache_page` decorator to it::

    from django.http import HttpResponse
    from django.http.shortcuts import get_object_or_404
    from django.views.decorators.cache import cache_page

    @cache_page(3600) # Cache view result for one hour
    def view_book(request, pk):
       book = get_object_or_404(Book, pk = pk)
       return HttpResponse('author is: %s, title is: %s' % (
          book.author, book.title), 'text/plain')
    
Here, the ``cache_page`` decorator will automatically cache the view responses
for up to one hour, keyed off the request path. It's not bad, but there is a
flaw: what if the view gets cached for a given book, then the object gets
modified or removed?  Well, as all experienced Django user know, you will still
get the older, now incorrect view response for up to an hour: **there is no way
to invalidate the cache selectively**. Out of the box with Django, you can
either:

* *Suck it up*, and live with the delay, possibly decreasing the timeout.

* *Clear the whole cache* (or increment the global version if you are on Django
  >= 1.3), and live with the following spike in resources usage while all the
  popular view calls get re-cached.

* *Design your project around this limitation*, either by not using the cache at
  all on some views, or carefully dual-accessing the views on cached and
  non-cached paths depending on the situation.

.. admonition:: The truth is...

   When we have control over the objects used to render a view, we usually don't
   care when a cached view result is meant to expire, and a timeout is really
   not that helpful... What we really want is to render a view once and for all
   for the objects it relies on, cache it, and reuse it as long as those
   objects don't change, *then* have a way to invalidate it (and preferably only
   it).

The Solution
------------
This is where :mod:`Django-groupcache` comes to the rescue! You could redecorate
``view_book`` like this::

    from django.http import HttpResponse
    from django.http.shortcuts import get_object_or_404
    from groupcache.decorators import cache_page_against_model

    @cache_page_against_model(Book)
    def view_book(request, pk):
       book = get_object_or_404(Book, pk = pk)
       return HttpResponse('author is: %s, title is: %s' % (
          book.author, book.title), 'text/plain')

Responses from `view_book` would then be cached as usual, but will also be
automatically dropped from cache whenever the associated book would change.

It might seems like black magic, but it's really not. The crux to allow things
like this is called *generational* (AKA *generation-based*, *action-based*)
caching (`Google search
<http://www.google.com/search?q=generational+caching>`_). Basically, it's
nothing more than building a cache key indirectly, using the value (called a
*generation*) associated with a second cache key you can compute out of the view
arguments and possibly the view name. By recomputing this last key and changing
the associated generation, you can then invalidate all the cache entries
depending on it.

:mod:`Django-groupcache` provides a number of decorators and utilities to deal
flexibly and efficiently with generational caching of views.

:doc:`Proceed to installation <install>`, or :doc:`go read the gory
details on how to use it <api>`.

