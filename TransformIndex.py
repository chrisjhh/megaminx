"""Version of a diskcache index optimised to lookup equivalent transformed states of the megaminx"""

from diskcache import Index
from .megaminx import Megaminx
import functools
m1 = Megaminx()
m2 = Megaminx()

def cached(func):
    @functools.wraps(func)
    def wrapper(self,key):
        if not hasattr(self,'_TransformIndex_cache'):
            self._TransformIndex_cache = {}
        if key in self._TransformIndex_cache:
            #print('Read %s from cache' % key)
            return self._TransformIndex_cache[key]
        val = func(self,key)
        self._TransformIndex_cache[key] = val
        return val
    return wrapper

def colour_cached(func):
    @functools.wraps(func)
    def wrapper(self,key):
        if not hasattr(self,'_TransformIndex_colour_cache'):
            self._TransformIndex_colour_cache = {}
        if key in self._TransformIndex_colour_cache:
            #print('Read %s from cache' % key)
            return self._TransformIndex_colour_cache[key]
        val = func(self,key)
        self._TransformIndex_colour_cache[key] = val
        return val
    return wrapper

def clear_cache(func):
    @functools.wraps(func)
    def wrapper(self,*args,**kwargs):
        if hasattr(self,'_TransformIndex_cache'):
            #print("Clearing cache")
            del self._TransformIndex_cache
        if hasattr(self,'_TransformIndex_colour_cache'):
            #print("Clearing cache")
            del self._TransformIndex_colour_cache
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

    @cached
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
    @colour_cached
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
