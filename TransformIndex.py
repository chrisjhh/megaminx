"""Version of a diskcache index optimised to lookup equivalent transformed states of the megaminx"""

from diskcache import Index
from .megaminx import Megaminx
m1 = Megaminx()
m2 = Megaminx()

class TransformIndex(Index):

    # def __contains__(self,item):
    #     if Index.__contains__(self,item):
    #         return True
    #     if self._has_colour_variant(item):
    #         return True
    #     if self._has_transformed_variant(item):
    #         return True

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
