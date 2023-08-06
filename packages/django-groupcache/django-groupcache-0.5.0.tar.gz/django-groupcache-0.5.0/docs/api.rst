Using Django-groupcache
=======================

What is a group?
----------------

As the name suggests, ``Django-groupcache`` is built around the notion of
groups. A group is simply a specification of how to compute a generation out of
a view call, while a generation is a cache entry you can change to invalidate
the cached responses to all view calls in the group.

For the sake of illustration, suppose we have a view that returns a number of
entries for a feed in either atom or RSS format, with a ``URLPattern`` similar
to this::

    (r'^feed/(?P<format>\w+)/(?P<feed_name>\w+)/(?P<num_entries>\d+)/$', 
      'myapp.views.view_feed')

Let's say we got two feeds, "politics" and "showbiz". We could access them like
this::

    /feed/atom/politics/10   # The latest 10 political entries as atom
    /feed/rss/showbiz/5      # The latest 5 showbiz entries as rss
    /feed/atom/showbiz/20    # The latest 20 showbiz entries as atom
    /feed/rss/politics/1     # The latest political entry as rss

If we would be to cache the view, we would probably want a way to
remove all the cached responses associated with a given feed: the pertinent
group would then rely solely on the feed name, and we would have::

    # Group of calls related to the political feed:
    /feed/atom/politics/10
    /feed/rss/politics/1

    # Group of calls related to the showbiz feed:
    /feed/rss/showbiz/5
    /feed/atom/showbiz/20

Using ``Django-groupcache``, we can then, in a single call, force the
invalidation of all caches entry for a given group.

.. _group-description:

Specifically, a group can be:

* a sequence of pertinent view arguments (like ``['feed_name']`` in
  our example)

* a dictionary mapping the pertinent view arguments to other names (like
  ``{'feed': 'feed_name'}``, see
  :func:`groupcache.decorators.cache_page_against_model` for an example the
  usefulness of this)

* a callable that will accept the same arguments as the view (minus the request
  object), and that will return a dictionnary uniquely representing the group::

   def feedgroup(format = None, feed_name = None, num_entries = None):
       return {'feed': feed_name}

* a simple string or unicode, used as a label (see
  for instance :func:`groupcache.decorators.cache_tagged_page`).

If you choose not to provide a group, default behavior is generally to assume
that all view arguments should be taken into account when computing the
generation.

.. admonition:: One important URLPatterns caveat: only named groups are supported!

   ``Django-groupcache`` tries to abide to `Django's design philosophies
   <http://docs.djangoproject.com/en/dev/misc/design-philosophies/>`_ as much as
   possible: loose-coupling and the DRY principle are important. Still, it needs
   to know a little bit more about views than the minimum that Django allows:
   thus, you need to exclusively employ `URL patterns with named groups
   <http://docs.djangoproject.com/en/dev/topics/http/urls/#named-groups>`_ on
   views you wish to "group cache".

Available View Decorators
-------------------------

.. function:: cache_versionned_page(group = None, cache_timeout = None, vary_on_view = True)
   :module: groupcache.decorators

   This is the most generic decorator of all; it's the one you should use
   whenever you have special needs that cannot be met by the ones
   below. Following our example above, it could be used like this::

    from groupcache.decorators import cache_versionned_page

    @cache_versionned_page(['feed_name'])
    def view_feed(request, 
                  format = 'atom', 
                  feed_name = None, 
                  num_entries = 10):
       ...
   
   Here, we specify that every call related to a given feed are part of a common
   group (that can be later uncached in a single operation), and that all calls
   to the view can be cached indefinitively. ``cache_timeout`` carries the usual
   meaning it has within the cache framework. while ``vary_on_view`` tells
   whether or not the generation should change with the view function. If you
   set it to ``False``, it means that the computed generation for two different
   views will be the same if applying the group to the view keywords will return
   the same value::

     from groupcache.decorators import cache_versionned_page

     @cache_versionned_page(group = {'id': 'object_id'}, 
                            vary_on_view = False)
     def first_view(request, 
                    object_id = None, some_argument = None):
        ...

     @cache_versionned_page(group = {'id': 'other_id'}, 
                            vary_on_view = False)
     def second_view(request, 
                     some_other_argument = None, other_id = None):
        ...

     # Calls to:
     #   first_view (request, object_id = '1')
     #   second_view(request, other_id  = '1')
     #
     # ... will end up sharing a common generation.
      

.. function:: cache_tagged_page(tag = None, cache_timeout = None)
   :module: groupcache.decorators

   Simple decorator that gives a way to attach a label to one or many
   views::

    from groupcache.decorators import cache_tagged_page

    @cache_tagged_page('feed-related')
    def view_feed_simple(request, feed_name = None):
       ...

    @cache_tagged_page('feed-related')
    def view_feeds_mashup(request, first_feed = None, second_feed = None):
       ...

   See also the companion function :func:`groupcache.utils.uncache_from_tag`.

.. function:: cache_page_against_model(model, cache_timeout = None, to_fields = None)
   :module: groupcache.decorators

   If you have a view that has a one-to-one relationship to a given model in
   your database (to be precise, a given view that requests exactly one entity
   of a given model for any call), this decorator allows you to cache the
   response, yet automatically invalidate it when the associated entity changes.

   Unless told otherwise, it assumes that all the view keywords correspond to
   identically-named fields in the model. If it's not the case, you should
   provide the ``to_fields`` argument, which is a :ref:`special-purpose group
   <group-description>` that specify how to map model fields to views
   keywords. Unlike a generic group, ``to_fields`` cannot be a callable: it
   should either be a sequence or a dictionnary.

   Suppose you have a model, called ``MyModel``, and a view that displays it,
   called ``view_my_model``, accepting two keywords: a model id
   (corresponding to MyModel's primary key), and a view mode. Here is how to use
   the decorator::

    from django.http.shortcuts import get_object_or_404
    from groupcache.decorators import cache_page_against_model

    @cache_page_against_model(MyModel, to_fields = {'pk': 'model_id'})
    def view_my_model(model_id = None, view_mode = 'plain'):
       obj = get_object_or_404(MyModel, pk = model_id)
       ...

   This decorator provides the functionality the author was after in the first
   place when writing ``Django-groupcache``.

.. function:: cache_page_against_models(first_model, second_model, ..., last_model, cache_timeout = None)
   :module: groupcache.decorators

   This is a blunter instrument than ``cache_page_against_model``, but still
   useful: the response of a view decorated with ``cache_page_against_models``
   will get cached, and automatically uncached whenever any entity of one of the
   listed models will get modified or removed.

.. _utilities-description:

Utilities
---------

.. function:: uncache(view_name, **view_keywords)
   :module: groupcache.utils

   Gives a mechanism to manually invalidate all the view responses
   sharing a given generation::

    # myapp/views.py

    from groupcache.decorators import cache_versionned_page

    @cache_versionned_page()
    def my_view(request, some_param = None):
       ...

   You can then call, from anywhere else::

    from groupcache.utils import uncache

    # Make sure the response to the call to my_view 
    # with 'some value' as param will be regenerated 
    # on next call.
    uncache('myapp.views.my_view', some_param = 'some value')

.. admonition:: Uncaching operates on groups of view calls, not single ones

   All uncaching utililities from the :mod:`groupcache.utils` module will not
   only invalidate the response for the precise call you give, but also for all
   the calls "from the same groups", sharing a given generation.

.. function:: uncache_from_path(path)
   :module: groupcache.utils

   Shorthand to :func:`groupcache.utils.uncache`, that resolves the view name
   and keywords from a request path first using
   ``django.core.urlresolvers.resolve``.

.. function:: uncache_from_tag(tag)
   :module: groupcache.utils

   Helper to :func:`groupcache.decorators.cache_tagged_page`. Shorthand to
   uncache all responses for tagged views::

     from groupcache.decorators import cache_tagged_page

     @cache_tagged_page('my tag')
     def my_view(request, some_id = None):
        ...

     # Then, from anywhere else:
     from groupcache.utils import uncache_from_tag    
     uncache_from_tag('my tag')

Final Considerations
-------------------- 

- ``Django-groupcache`` is cleanly build on top of the `Django
  cache framework <http://docs.djangoproject.com/en/dev/topics/cache/>`_,
  and no `monkey-patching <http://en.wikipedia.org/wiki/Monkey_patch>`_ or
  access to APIs marked as private takes place: 

    * The cache behavior will changes with the specifics of the version of
      Django you will use, and the full extent of what the framework has to
      offer in term of view caching will still work with group caching (such as
      ``vary_headers``, distinct caching on different languages, etc.).

    * Nothing prevents you from using the normal cache mechanisms (such as the
      ``cache_page`` decorator) along what ``Django-groupcache`` offers: there
      will exhibit no performance hit or changes in behavior.

    * The app should prove relatively robust against future changes to the
      framework.

- When using :func:`groupcache.utils.uncache`, it's perfectly fine to employ a
  named URL pattern as the ``view_name``. It should be understood, though, that
  it's the view function that is ultimately decorated, **not** the named
  pattern: there is no way to selectively uncache responses based on different
  view names resolving to a single view function.

- You can safely use :func:`groupcache.utils.uncache` or
  :func:`groupcache.utils.uncache_from_path` against every view decorated with
  any of the decorators from the ``groupcache.decorators`` module.

- Compared to plain view caching, the implemented group caching strategy induces
  a slight performance hit, due mainly to the dual cache lookup. In our
  experience, It's still a lot less expensive than a full view call to
  any non-trivial view.
