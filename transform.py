"""Class to represent a rotational transofrm of the megaminx"""
import re

#re1 = re.compile(r'(\w)')
#re2 = re.compile(r':(\w)')

class Transform(dict):
    
    def transform(self, string):
        res = []
        for c in string:
            try:
                res.append(self[c])
            except(KeyError):
                res.append(c)
        return ''.join(res)
    
    def invert(self, string):
        res = []
        if not hasattr(self,'_inverse'):
            self._inverse = {}
            for k in self.keys():
                if len(k) > 1:
                    continue
                self._inverse[self[k]] = k
        for c in string:
            try:
                res.append(self._inverse[c])
            except(KeyError):
                res.append(c)
        return ''.join(res)
