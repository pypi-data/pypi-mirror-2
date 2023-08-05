"""Custom maps for special purposes.

"""

import collections
import itertools
import json

# These are the positions in the length-3 lists I am using to implement a 
# doubly linked list of keys in OrderedDict 
PREV, ITEM, NEXT = range(3)
class OrderedDict(collections.MutableMapping):
    """A mapping in which the keys are stored in the order they are inserted.
    
    ``remember.dicts.OrderedDict`` is intended to be a compatible 
    implementation with ``collections.OrderedDict``. In Python 2.7, 
    ``collections.OrderedDict`` is used to implement :class:`LRUDict`. 
    In 2.6, ``collections.OrderedDict`` does not exist.
    
    Known differences this class has from ``collections.OrderedDict``:    
     
     - There is no ``copy`` method or hooks for the ``copy`` module.
     - There is no ``__reduce__`` method for serialization purposes.
     - Calling ``__init__`` manually erases the old entries.
    
    Aside from these, this implementation passes the unit tests for 
    ``collections.OrderedDict``.
    
    """    
    def __init__(self, *args, **kwargs):
        # doubly linked list
        self._clasp = [] 
        self._clasp[:] = [self._clasp, None, self._clasp]
        
        self._d = {}
        
        # Mimic the constructor of dict. Blech.
        if args:
            if len(args) == 1:
                iterable = args[0]
            else:
                raise TypeError("%s expected at most 1 arguments, got %d" %
                                (self.__class__.__name__, len(args)))
                
            try:
                iterable.keys
            except AttributeError:
                for key, value in iterable:
                    self[key] = value
            else:
                for key in iterable.keys():
                    self[key] = iterable[key]

        self.update(kwargs)

    def __len__(self):
        return len(self._d)

    def __contains__(self, key):
        return key in self._d
        
    def __getitem__(self, key):
        node, value = self._d[key]
        return value
    
    def __setitem__(self, key, value):
        if key not in self._d:
            # If this is a new key, we have to put it in the linked list.
            prev = self._clasp[PREV]
            node = [prev, key, self._clasp]
            prev[NEXT] = self._clasp[PREV] = node
        else:
            node, old_value = self._d[key]
            
        self._d[key] = node, value
        
    def __delitem__(self, key):
        if key in self._d:
            node, value = self._d.pop(key)
            
            # snip!
            prev, _, next = node
            prev[NEXT] = next
            next[PREV] = prev
        else:
            raise KeyError(repr(key))

    def __iter__(self):
        prev, _, node = self._clasp
        while node is not self._clasp:
            yield node[ITEM]
            node = node[NEXT]
    
    def __eq__(self, other):
        if isinstance(other, OrderedDict):
            return all((s, self[s]) == (o, other[o]) 
                       for s, o in itertools.izip(self, other))
        return super(OrderedDict, self).__eq__(other)
        
    def __reversed__(self):
        # Iterate backwards through the keys.
        first = self._clasp[NEXT]
        node = self._clasp
        while node is not first:
            node = node[PREV]
            yield node[ITEM]
            
    def popitem(self, last=True):
        if last:
            it = reversed(self)
        else:
            it = iter(self)
            
        try:
            key = next(it)
        except StopIteration:
            # empty OrderedDict
            raise KeyError
            
        return key, self.pop(key)
             
    def __repr__(self):
        items = self.items()
        if not items:
            items = ""
            
        return "%s(%s)" % (self.__class__.__name__, items)

        
# Define BestOrderedDict to be my implementation if we don't have 
# collections.OrderedDict yet (i.e., if we're <2.7) and to be 
# collections' if it is there.
try:
    _BestOrderedDict = collections.OrderedDict
except AttributeError:
    _BestOrderedDict = OrderedDict
    
class LRUDict(collections.MutableMapping):
    """Keep a mapping storing only the last ``size`` accessed items.

    ``LRUDict`` works much like a normal dict except that if it grows to be
    larger than ``size`` items, adding new items will result in the least-
    recently-acessed item to be removed. Getting or setting an item in any way
    refreshes an item as recently used.

    Other than the first argument ``size``, all arguments to ``LRUDict`` are
    passed on to ``OrderedDict``, which is a ``collections.OrderedDict`` if 
    available and :class:`remember.dicts.OrderedDict` otherwise.

    """
    def __init__(self, size, *args, **kwargs):
        self._d = _BestOrderedDict(*args, **kwargs)
        self._size = size
        self._prune()
        
    def _prune(self):
        while len(self._d) > self._size:
            self._d.popitem(last=False)
        
    def __getitem__(self, key):
        value = self._d.pop(key)
        self._d[key] = value
        return value
    
    def __setitem__(self, key, value):
        if key in self._d:
            del self._d[key]
        self._d[key] = value
        self._prune()
        
    def __delitem__(self, key):
        del self._d[key]
        
    def __iter__(self):
        """Iterate over the keys from least recently used to most."""
        # Accessing items as we iterate will change the order, so we retrieve
        # all the keys ahead of time.
        return iter(self._d.keys())

    def __len__(self):
        return len(self._d)

    def __repr__(self):
        return "%s(%s, %s)" % (self.__class__.__name__,
                               self._size, self._d.items())

                               
class FrozenDict(collections.Mapping):
    """A hashable, immutable mapping type.

    The arguments to ``FrozenDict`` are processed just like those to ``dict``.

    """
    def __init__(self, *args, **kwargs):
        self._d = dict(*args, **kwargs)
        self._hash = None

    @classmethod
    def supply_dict(cls, d):
        """Make a FrozenDict from a regular dict.

        Given a dict, ``supply_dict`` uses it as the basis for the 
        ``FrozenDict`` returned. If you use ``supply_dict``, *ensure that 
        you do not ever mutate the* ``dict`` *object passed*.  

        This method is what we in the biz like to call "premature 
        optimization".

        """
        frozen_dict = cls()
        frozen_dict._d = d
        return frozen_dict

    def __iter__(self):
        return iter(self._d)

    def __len__(self):
        return len(self._d)

    def __getitem__(self, key):
        return self._d[key]

    def __hash__(self):
        if self._hash is None:
            self._hash = 0
            for key, value in self.iteritems():
                self._hash ^= hash(key)
                self._hash ^= hash(value)
                
        return self._hash

    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, self._d)


class FrozenDictJSONEncoder(json.JSONEncoder):
    """A JSON encoder that can encode a  :class:`FrozenDict` as a JSON object."""
    def default(self, o):
        if isinstance(o, FrozenDict):
            return dict(o)
        return json.JSONEncoder.default(self, o)
