==================
django-cache-utils
==================

django-cache-utils provides some utils for make cache-related work easier:

* django memcached cache backend with group O(1)
  invalidation ability, dog-pile effect prevention using MintCache algorythm
  and project version support to allow gracefull updates and multiple django
  projects on same memcached instance.
  Long keys (>250) are truncated and appended with md5 hash.
* ``cached`` decorator. Can be applied to function, method or classmethod.
  Supports bulk O(1) cache invalidation and meaningful cache keys.
  Takes function's arguments and full name into account while
  constructing cache key.

Installation
============

::

    pip install django-cache-utils

and then::

    # settings.py
    CACHE_BACKEND = 'cache_utils.group_backend://localhost:11211/'

Usage
=====

::

    from django.db import models
    from cache_utils.decorators import cached

    class CityManager(models.Manager):

        # cache a method result. 'self' parameter is ignored
        @cached(60*60*24, 'cities')
        def default(self):
            return self.active()[0]

        # cache a method result. 'self' parameter is ignored, args and
        # kwargs are used to construct cache key
        @cached(60*60*24, 'cities')
        def get(self, *args, **kwargs):
            return super(CityManager, self).get(*args, **kwargs)


    class City(models.Model):
        # ... field declarations

        objects = CityManager()

        # an example how to cache django model methods by instance id
        def has_offers(self):
            @cached(30)
            def offer_count(pk):
                return self.offer_set.count()
            return history_count(self.pk) > 0

    # cache the function result based on passed parameter
    @cached(60*60*24, 'cities')
    def get_cities(slug)
        return City.objects.get(slug=slug)


    # cache for 'cities' group can be invalidated at once
    def invalidate_city(sender, **kwargs):
        cache.invalidate_group('cities')
    pre_delete.connect(invalidate_city, City)
    post_save.connect(invalidate_city, City)

Notes
=====

django-cache-utils use 2 reads from memcached to get a value if 'group'
argument is passed to 'cached' decorator::

    @cached(60)
    def my_func(param)
        return ..

    @cached(60, 'my_group')
    def my_func2(param)
        return ..

    # 1 read from memcached
    value1 = my_func(1)

    # 2 reads from memcached + ability to invalidate all values at once
    value2 = my_func2(2)

Running tests
=============

Add ``'cache_utils'`` to ``INSTALLED_APPS`` and run ``./manage test cache_utils``.
