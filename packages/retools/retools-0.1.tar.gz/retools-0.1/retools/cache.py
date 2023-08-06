"""Redis Caching

Redis caching using cache regions to simplify common expirations and group
function caches.

To indicate functions should use cache regions, apply the decorator::
    
    from retools.cache import cache_region
    
    @cache_region('short_term')
    def myfunction(arg1):
        return arg1

To configure the cache regions, setup the CacheRegion object::
    
    from retools.cache import CacheRegion
    
    CacheRegion.add_region("short_term", expires=60)

Using cache regions instead of individually specifying the expiration
allows for global changes of the expiration for batches of cached
functions as well as mass invalidation of a regions cached values.

"""
import cPickle
import time
from datetime import date

from retools import Connection
from retools.exc import CacheConfigurationError
from retools.lock import Lock
from retools.lock import LockTimeout
from retools.util import func_namespace
from retools.util import has_self_arg


class _NoneMarker(object):
    pass
NoneMarker = _NoneMarker()


class CacheKey(object):
    """Cache Key object
    
    Generator of cache keys for a variety of purposes once
    provided with a region, namespace, and key (args).
    
    """
    def __init__(self, region, namespace, key, today=None):
        today = today or str(date.today())
        self.lock_key = 'retools:lock:%s:%s:%s' % (region, namespace, key)
        self.redis_key = 'retools:%s:%s:%s' % (region, namespace, key)
        self.redis_hit_key = 'retools:hits:%s:%s:%s:%s' % (
            today, region, namespace, key)
        self.redis_miss_key = 'retools:misses:%s:%s:%s:%s' % (
            today, region, namespace, key)
        self.redis_keyset = 'retools:%s:%s:keys' % (region, namespace)


class CacheRegion(object):
    """CacheRegion manager and configuration object
    
    For organization sake, the CacheRegion object is used to configure
    the available cache regions, query regions for currently cached
    keys, and set batches of keys by region for immediate expiration.
    
    Caching can be turned off globally by setting enabled to False::
        
        CacheRegion.enabled = False
    
    """
    regions = {}
    enabled = True
    
    @classmethod
    def add_region(cls, name, expires, redis_expiration=60*60):
        """Add a cache region to the current configuration
        
        :param    name: The name of the cache region
        :param expires: The expiration in seconds.
        
        """
        cls.regions[name] = dict(expires=expires,
                                 redis_expiration=redis_expiration)
        
    @classmethod
    def _add_tracking(cls, pipeline, region, namespace, key):
        """Add's basic set members for tracking
        
        This is added to a Redis pipeline for a single round-trip to
        Redis.
        
        """
        pipeline.sadd('retools:regions', region)
        pipeline.sadd('retools:%s:namespaces' % region, namespace)
        pipeline.sadd('retools:%s:%s:keys' % (region, namespace), key)
    
    @classmethod
    def load(cls, region, namespace, key, regenerate=True, callable=None):
        """Load a value from Redis
        
        :param regenerate: If False, then existing keys will always be
                           returned regardless of cache expiration. In the
                           event that there is no existing key and no
                           callable was provided, then a NoneMarker will
                           be returned.
        
        """
        redis = Connection.get_default()
        now = time.time()
        region_settings = cls.regions[region]
        expires = region_settings['expires']
        
        keys = CacheKey(region=region, namespace=namespace, key=key)
        
        # Create a transaction to update our hit counter for today and
        # retrieve the current value.
        p = redis.pipeline(transaction=True)
        p.hgetall(keys.redis_key)
        p.get(keys.redis_hit_key)
        p.incr(keys.redis_hit_key)
        results = p.execute()
        result, existing_hits = results[0], results[1]
        if existing_hits:
            existing_hits = int(existing_hits)
        expired = True
        if result and now - float(result['created']) < expires:
            expired = False
        
        if (result and not regenerate) or not expired:
            # We have a result and were told not to regenerate so
            # we always return it immediately regardless of expiration, 
            # or its not expired
            return cPickle.loads(result['value'])
                
        if not result and not regenerate and not callable:
            # No existing value, but we were told not to regenerate it and
            # there's no callable, so we return a NoneMarker
            return NoneMarker
        
        # We either have a result and its expired, or no result
        # Does someone already have the lock? If so, return the value if
        # we have one
        if result and redis.exists(keys.lock_key):
            return cPickle.loads(result['value'])
        
        with Lock(keys.lock_key, expires=expires, timeout=60*60*24*7):
            # Did someone else already create it?
            result = redis.hgetall(keys.redis_key)
            if 'value' in result and now - float(result['created']) < expires:
                return cPickle.loads(result['value'])
            
            existing_hits = existing_hits or 0
            value = callable()
            
            p = redis.pipeline(transaction=True)
            p.getset(keys.redis_hit_key, 0)
            p.hmset(keys.redis_key, {'created': now, 
                                'value': cPickle.dumps(value)})
            cls._add_tracking(p, region, namespace, key)
            new_hits = int(p.execute()[0])
        
        misses = new_hits - existing_hits
        if misses:
            p = redis.pipeline(transaction=True)
            p.incr(keys.redis_hit_key, amount=existing_hits)
            p.incr(keys.redis_miss_key, amount=misses)
            p.execute()
        else:
            redis.incr(keys.redis_hit_key, amount=existing_hits)
        return value


def invalidate_region(region, clear=False):
    """Invalidate all the namespace's in a given region

    clear
        Whether the values should be removed entirely, or merely
        invalidated.

    """
    redis = Connection.get_default()
    namespaces = redis.smembers('retools:%s:namespaces' % region)
    if not namespaces:
        return None
    
    # Locate the longest expiration of a region, so we can set
    # the created value far enough back to force a refresh
    longest_expire = max([x['expires'] for x in CacheRegion.regions.values()])
    new_created = time.time() - longest_expire - 3600
    
    for ns in namespaces:
        cache_keyset_key = 'retools:%s:%s:keys' % (region, ns)
        keys = set(['']) | redis.smembers(cache_keyset_key)
        p = redis.pipeline(transaction=True)
        for key in keys:
            cache_key = 'retools:%s:%s:%s' % (region, ns, key)
            if not redis.exists(cache_key):
                p.srem(cache_keyset_key, key)
            if clear:
                p.srem(cache_keyset_key, key)
                p.delete(cache_key)
            else:
                p.hset(cache_key, 'created', new_created)
        if clear:
            p.srem('retools:%s:namespaces' % region, ns)
        p.execute()


def invalidate_function(func, deco_args=None, *args):
    """Invalidate the cache for a function

    func
        The function that was decorated by cache_region.
    
    deco_args
        Argument list passed to decorator for differentiation.

    args
        Arguments the decorator + function was called with that should
        be invalidated. If the args is just the differentiator for the
        function, or not present, then all values for the function
        will be invalidated.
    
    Example::
        
        @cache_region('short_term', 'small_engine')
        def local_search(search_term):
            # do search and return it
        
        @cache_region('long_term')
        def lookup_folks():
            # look them up and return them
        
        # To clear local_search for search_term = 'fred'
        invalidate_function(local_search, 'small_engine', 'fred')
        
        # To clear all cached variations of the local_search function
        invalidate_function(local_search, 'small_engine')
        
        # To clear out lookup_folks
        invalidate_function(lookup_folks)
    
    """
    deco_args = deco_args or []
    redis = Connection.get_default()
    region = func._region
    namespace = func._namespace
    
    # Get the expiration for this region
    new_created = time.time() - CacheRegion.regions[region]['expires'] - 3600
    
    if args:
        try:
            cache_key = " ".join(map(str, args))
        except UnicodeEncodeError:
            cache_key = " ".join(map(unicode, args))
        redis.hset('retools:%s:%s:%s' % (region, namespace, cache_key),
                   'created', new_created)
    else:
        cache_keyset_key = 'retools:%s:%s:keys' % (region, namespace)
        keys = set(['']) | redis.smembers(cache_keyset_key)
        p = redis.pipeline(transaction=True)
        for key in keys:
            p.hset('retools:%s:%s:%s' % (region, namespace, key), 'created',
                   new_created)
        p.execute()
    return None


def cache_region(region, *deco_args):
    """Decorate a function such that its return result is cached,
    using a "region" to indicate the cache arguments.

    Example::

        from retools.cache import cache_region
        
        @cache_region('short_term', 'load_things')
        def load(search_term, limit, offset):
            '''Load from a database given a search term, limit, offset.'''
            return database.query(search_term)[offset:offset + limit]
    
    The decorator can also be used with object methods.  The ``self``
    argument is not part of the cache key.  This is based on the 
    actual string name ``self`` being in the first argument 
    position::

        class MyThing(object):
            @cache_region('short_term', 'load_things')
            def load(self, search_term, limit, offset):
                '''Load from a database given a search term, limit, offset.'''
                return database.query(search_term)[offset:offset + limit]
    
    Classmethods work as well - use ``cls`` as the name of the class argument,
    and place the decorator around the function underneath ``@classmethod``::
    
        class MyThing(object):
            @classmethod
            @cache_region('short_term', 'load_things')
            def load(cls, search_term, limit, offset):
                '''Load from a database given a search term, limit, offset.'''
                return database.query(search_term)[offset:offset + limit]
    
    :param region: String name of the region corresponding to the desired
      caching arguments, established in :attr:`.cache_regions`.
      
    :param \*deco_args: Optional ``str()``-compatible arguments which will
      uniquely identify the key used by this decorated function, in addition
      to the positional arguments passed to the function itself at call time.
      This is recommended as it is needed to distinguish between any two
      functions or methods that have the same name (regardless of parent
      class or not).
      
    .. note::

        The function being decorated must only be called with
        positional arguments, and the arguments must support
        being stringified with ``str()``.  The concatenation
        of the ``str()`` version of each argument, combined
        with that of the ``*args`` sent to the decorator,
        forms the unique cache key.

    .. note::
    
        When a method on a class is decorated, the ``self`` or ``cls``
        argument in the first position is
        not included in the "key" used for caching.
    
    """
    def decorate(func):
        namespace = func_namespace(func, deco_args)
        skip_self = has_self_arg(func)
        def cached(*args):
            if region not in CacheRegion.regions:
                raise CacheConfigurationError(
                    'Cache region not configured: %s' % region)
            if not CacheRegion.enabled:
                return func(*args)
            
            if skip_self:
                try:
                    cache_key = " ".join(map(str, args[1:]))
                except UnicodeEncodeError:
                    cache_key = " ".join(map(unicode, args[1:]))
            else:
                try:
                    cache_key = " ".join(map(str, args))
                except UnicodeEncodeError:
                    cache_key = " ".join(map(unicode, args))
            def go():
                return func(*args)
            return CacheRegion.load(region, namespace, cache_key, callable=go)
        cached._region = region
        cached._namespace = namespace
        return cached
    return decorate
