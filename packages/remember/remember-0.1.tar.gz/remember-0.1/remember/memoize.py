"""Memoize callables."""

import functools
import json
import types

from remember import dicts
    
class Memoizer(object):
    """Memoize a callable's values.

    ``Memoizer`` is mainly meant for internal use. To memoize a callable,
    use the :func:`memoize` function.
    
    """
    def __init__(self, f, cache_size=None, allow_unhashable=True):
        if cache_size is None:
            self._cache = {}
        else:
            self._cache = dicts.LRUDict(cache_size)

        self._cache_size = cache_size
        self._allow_unhashable = allow_unhashable

        self._f = f
        
    def __call__(self, *args, **kwargs):
        key = args, dicts.FrozenDict.supply_dict(kwargs)

        if self._allow_unhashable:
            try:
                hash(key)
            except TypeError:
                return self._f(*args, **kwargs)

        if key not in self._cache:
            self._cache[key] = self._f(*args, **kwargs)

        return self._cache[key]

    def __get__(self, obj, type=None):
        # Define __get__ so we can memoize methods.
        return types.MethodType(self, obj, type)

    def __repr__(self):
        """Generate a repr for the memoized callable.
        
        If the object is a function (if its repr is "<function...", then a 
        new repr of the form <memoized function %s at 0x%X> is generated, 
        with %s being the name of the function. For other objects, the 
        callable's repr is used with no modification.
        
        """
        f_repr = repr(self._f)
        if f_repr.startswith("<function"):
             return "<memoized function %s at 0x%X>" % (self._f.__name__,
                                                        id(self))
        else:
            return f_repr

    def save(self):
        state = (self._cache_size, self._allow_unhashable,
                 self._cache.items())
        
        return dicts.FrozenDictJSONEncoder().encode(state)

    @classmethod
    def restore(cls, f, s):
        cache_size, allow_hashable, cache_items = json.loads(s)
        cache_items = _freeze(cache_items)

        self = cls(f, cache_size, allow_hashable)

        if cache_size is None:
            self._cache = dict(cache_items)
        else:
            self._cache = dicts.LRUDict(cache_size, cache_items)

        return self

def _freeze(items):
    for (args, kwargs), value in items:
        args = _lists_to_tuples(args)

        frozen_kwargs = dicts.FrozenDict((k, _lists_to_tuples(v))
                                          for k, v in kwargs.iteritems())
        
        value = _lists_to_tuples(value)
        yield (args, frozen_kwargs), value
        
def _lists_to_tuples(x):
    if isinstance(x, list):
        # XXX I don't like this recursion
        return tuple(_lists_to_tuples(item) for item in x)
    else:
        return x

        
class MethodMemoizer(object):
    """Memoize method calls separetly for each instance.

    This class is used to implement :func:`memoize_method`.

    """
    def __init__(self, f, cache_size=None, allow_unhashable=True):
        self._f = f
        self._cache_size = cache_size
        self._allow_unhashable = allow_unhashable

    def _unbound_method(self, *args, **kwargs):
        # possible bug if you pass self as a kwarg, but if you do 
        # that you deserve it. 
        return self._method(args[0])(*args[1:], **kwargs)
        
    def _method(self, obj):
        try:
            return obj._memoized_method_caches[self._f]
        except (AttributeError, KeyError) as e:
            if isinstance(e, AttributeError):
                obj._memoized_method_caches = {}
            
            method = functools.partial(self._f, obj)
            obj._memoized_method_caches[self._f] = Memoizer(method, 
                                                      self._cache_size, 
                                                      self._allow_unhashable)
            return obj._memoized_method_caches[self._f]

    def __get__(self, obj, type=None):
        if obj is None:
            return self._unbound_method

        return self._method(obj)
        
def memoize(cache_size=None, allow_unhashable=True):
    """Decorate a callable to memoize its last ``cache_size`` hashable calls.

    Parameters:
        ``cache_size``  
            The maximum number of entries to store in the cache. If
            ``cache_size`` is not supplied, the number of entries to store is 
            not limited.
        ``allow_unhashable=True``
            If ``allow_unhashable`` is true (default), then in the
            case of unhashable arguments, the function is called and the
            result returned (with no memoization). If ``allow_hashable`` is
            false, ``TypeError`` is propogated. Note that no matter what, 
            the objects on which the methods are called must be hashable.

    You can use ``memoize`` with methods. The underlying function will be
    memoized with ``self`` passed as a normal argument. :func:`memoize_method` 
    can be useful in that it memoizes each bound method separately; in 
    that way it does not keep objects alive just because their method calls 
    are cached. ``memoize`` may be the better choice if you have defined 
    your own ``__hash__``/``__eq__`` and multiple instances of your class 
    can be equal to each other.
    
    Be careful with mutable return values. You will get the same object you 
    started with which--if you are mutating the object--isn't what you want.

    >>> from remember.memoize import memoize
    >>> @memoize()
    ... def put_in_list(x):
    ...     return [x]
    ...
    >>> y = put_in_list(5)
    >>> z = put_in_list(5)
    >>> z
    [5]
    >>> y.append(7)
    >>> z
    [5, 7]
    >>> put_in_list(5)
    [5, 7]
    
    """
    
    # We will create a new subclass of Memoizer for each instance so that we 
    # can set its docstring. I don't really like it, but I think it's the 
    # best idea.
       
    return functools.partial(Memoizer, cache_size=cache_size,
                             allow_unhashable=allow_unhashable)


def memoize_method(cache_size=None, allow_unhashable=True):
    """Decorate a callable to memoize its last cache_size hashable calls.

    Parameters are the same as :func:`memoize`. Note that ``cache_size`` is
    **per instance memoized**, not over all instances. While the methods 
    to the argument must be hashable, the actual object on which the 
    methods are called need not be.
    
    Warning: ``memoize_method`` creates a ``_memoized_method_caches`` 
    attribute on the objects whose methods it memoizes. Be sure not to 
    define one that interferes, to be careful using ``__slots__``, and 
    to keep this in mind if you're doing metaprogramming.
    
    ``memoize_method`` is seldom all that useful. Be very careful to be sure 
    you can memoize the method based on its non-``self`` arguments (This is 
    likely only if you have an immutable object or if your method should 
    really be a normal function.) If ``self`` is itself equatable/hashable in 
    non-default ways, you  probably want to use :func:`memoize` instead. If 
    you have mutable state affecting the results, you probably want to write 
    a pure function depending on that state, memoize that, and have your 
    method call it. 
    
    """
    return functools.partial(MethodMemoizer, cache_size=cache_size,
                             allow_unhashable=allow_unhashable)

                             
class memoized_property(object):
    """Make read-only properties with memoized results for each instance.
    
    It common use of properties are for read-only, once-executed values. 
    Code might look like::
        
        class C(object):
            def __init__(self):
                self._prop = None
            
            @property
            def prop(self):
                if self._prop is None:
                    self._prop = do_expensive_stuff()
                
                return self._prop
                
    ``memoized_property`` reduces this boilerplate some to::
    
        from remember.memoize import memoized_property
        
        class C(object):
            @memoized_property
            def prop(self):
                return do_expensive_stuff()
    
    Warning: ``memoized_property`` creates a ``_memoized_property_cache`` 
    attribute on the objects whose methods it memoizes. Be sure not to 
    define one that interferes, to be careful using ``__slots__``, and 
    to keep this in mind if you're doing metaprogramming.
    
    """
    def __init__(self, f):
        self.f = f
        
    def __get__(self, obj, type=None):
        if obj is None:
            return self
            
        try:
            return obj._memoized_property_cache[self.f]
        except (AttributeError, KeyError) as e:
            if isinstance(e, AttributeError):
                obj._memoized_property_cache = {}
                
            obj._memoized_property_cache[self.f] = result = self.f(obj)
            
            return result