"""Directory structure cache for storing solver results"""

import os
import os.path

class ResultsCache:
    
    def __init__(self,directory):
        if not os.path.exists(directory):
            os.mkdir(directory)
        self.dir = directory

    def store(self,m,value):
        location = self._location(m)
        filename = os.path.join(self.dir,location)
        directory = os.path.dirname(filename)
        if not os.path.isdir(directory):
            os.makedirs(directory)
        fh = open(filename,'w+b')
        fh.write(value)
        fh.close()


    def retrieve(self,m):
        location = self._location(m)
        filename = os.path.join(self.dir,location)
        if not os.path.isfile(filename):
            return None
        fh = open(filename,'rb')
        value = fh.read()
        fh.close()
        return value

    def _location(self,m):
        dir1 = str(m.faces['w'])
        dir2 = str(m.faces['x'])
        dir1 = dir1.replace('[','')
        dir1 = dir1.replace(']','')
        dir2 = dir2.replace('[','')
        dir2 = dir2.replace(']','')
        full = str(m)
        full = full.replace('[','_')
        full = full.replace(']','_')
        return os.path.join(dir1,dir2,full)

if __name__ == "__main__":
    from .megaminx import Megaminx
    m = Megaminx()
    c = ResultsCache('tempdir')
    c.store(m,'solved')
    m.faces['w'].rotate_anticlockwise()
    c.store(m, 'w>')
    m.faces['p'].rotate_clockwise()
    c.store(m, 'p< w>')
    print(c._location(m))
    print(c.retrieve(m))
    m.faces['p'].rotate_anticlockwise()
    print(c._location(m))
    print(c.retrieve(m))
    m.faces['w'].rotate_clockwise()
    print(c._location(m))
    print(c.retrieve(m))
    m.faces['G'].rotate_clockwise()
    print(c._location(m))
    print(c.retrieve(m))
