"""Version of a diskcache index optimised to lookup equivalent transformed states of the megaminx"""

from diskcache import Index
from .megaminx import Megaminx
import functools
m1 = Megaminx()
m2 = Megaminx()

caches = set()

def cached(cachename='_TransformIndex_cache'):
    global caches
    caches.add(cachename)
    def cached_internal(func):
        @functools.wraps(func)
        def wrapper(self,key):
            if not hasattr(self,cachename):
                self.__dict__[cachename] = {}
            cache = self.__dict__[cachename]
            if key in cache:
                #print('Read %s from cache' % key)
                return cache[key]
            val = func(self,key)
            cache[key] = val
            return val
        return wrapper
    return cached_internal

def clear_cache(func):
    @functools.wraps(func)
    def wrapper(self,*args,**kwargs):
        global caches
        for cache in caches:
            if hasattr(self,cache):
                del self.__dict__[cache]
        return func(self,*args,**kwargs)
    return wrapper

class TransformIndex(Index):

    # def __contains__(self,item):
    #     if Index.__contains__(self,item):
    #         return True
    #     if self._has_colour_variant(item):
    #         return True
    #     if self._has_transformed_variant(item):
    #         return True

    @cached()
    def __getitem__(self,key):
        try:
            value = Index.__getitem__(self,key)
            return value
        except(KeyError):
            pass
        value = self._get_colour_variant(key)
        if value is not None:
            return value
        value = self._get_transformed_variant(key)
        if value is not None:
            return value
        raise KeyError('No matching entry %s' % key)

    # def _has_colour_variant(self,item):
    #     global m2
    #     m = m2
    #     m.parse(item)
    #     xforms = m.get_colour_transforms()
    #     for xform in xforms:
    #         tstate = m.transformed_state(xform)
    #         if Index.__contains__(self,tstate):
    #             return True
    #     return False

    # def _has_transformed_variant(self,item):
    #     global m1
    #     m = m1
    #     m.parse(item)
    #     xforms = m.get_transforms()
    #     for xform in xforms:
    #         tstate = m.transformed_state(xform)
    #         if Index.__contains__(self,tstate):
    #             return True
    #         if self._has_colour_variant(tstate):
    #             return True
    #     return False

    #@cached
    @cached('_TransformIndex_colour_cache')
    def _get_colour_variant(self,key):
        global m2
        m = m2
        m.parse(key)
        xforms = m.get_colour_transforms()
        for xform in xforms:
            tstate = m.transformed_state(xform)
            try:
                value = Index.__getitem__(self,tstate)
                return xform.invert(value)
            except(KeyError):
                pass
        return None

    def _get_transformed_variant(self,key):
        global m1
        m = m1
        m.parse(key)
        xforms = m.get_transforms()
        for xform in xforms:
            tstate = m.transformed_state(xform)
            try:
                value = Index.__getitem__(self,tstate)
                return xform.invert(value)
            except(KeyError):
                pass
            value = self._get_colour_variant(tstate)
            if value is not None:
                return xform.invert(value)
        return None

    @clear_cache
    def __setitem__(self,key,value):
        return Index.__setitem__(self,key,value)
