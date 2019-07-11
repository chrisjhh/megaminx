"""Class to represent a rotational transofrm of the megaminx"""
import re

class Transform(dict):
    
    def transform(self, string):
        s = re.sub(r'(\w)',r':\1',string)
        for k in self.keys():
            if len(k) > 1:
                continue
            s = re.sub(':%s' % k, self[k],s)
        s = re.sub(r':(\w)',r'\1',s)
        return s
    
    def invert(self, string):
        s = re.sub(r'(\w)',r':\1',string)
        for k in self.keys():
            if len(k) > 1:
                continue
            s = re.sub(':%s' % self[k], k, s)
        s = re.sub(r':(\w)',r'\1',s)
        return s
