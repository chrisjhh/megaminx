"""Class to represent a rotational transofrm of the megaminx"""
import re

re1 = re.compile(r'(\w)')
re2 = re.compile(r':(\w)')

class Transform(dict):
    
    def transform(self, string):
        global re1, re2
        s = re1.sub(r':\1',string)
        for k in self.keys():
            if len(k) > 1:
                continue
            s = s.replace(':%s' % k, self[k])
            #s = re.sub(':%s' % k, self[k],s)
        s = re2.sub(r'\1',s)
        return s
    
    def invert(self, string):
        global re1, re2
        s = re1.sub(r':\1',string)
        for k in self.keys():
            if len(k) > 1:
                continue
            #s = re.sub(':%s' % self[k], k, s)
            s = s.replace(':%s' % self[k], k)
        s = re2.sub(r'\1',s)
        return s
