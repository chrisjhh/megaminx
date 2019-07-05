"""Class for large queues of items that should be stored in file instead of memory"""

import tempfile
import json
import os.path

class FileQueue:
    
    def __init__(self,filename=None,persistent=False):
        if filename:
            mode = 'a+b' if persistent else 'w+b'
            self.fh = open(filename, mode)
        else:
            self.fh = tempfile.TemporaryFile()
        self.readpos = 0
        if filename and persistent:
            self._loadpos(filename)
    
    def enqueue(self,obj):
        self.fh.seek(0,2)
        self.fh.write(json.dumps(obj))
        self.fh.write('\n')

    def dequeue(self):
        # Assume we have finished with last value when we
        # move on to next
        self._savepos()
        self.fh.seek(self.readpos)
        data = self.fh.readline()
        self.readpos = self.fh.tell()
        if not data:
            return None
        return json.loads(data)

    def empty(self):
        self.fh.seek(0,2)
        return self.fh.tell() == self.readpos

    def close(self):
        self.fh.close()
        self.fh = None

    def _loadpos(self, filename):
        (dirname,basename) = os.path.split(filename)
        self._indexfile = os.path.join(dirname,basename + '_i')
        if os.path.isfile(self._indexfile):
            fh = open(self._indexfile, "rb")
            self.readpos = int(fh.read())
            fh.close()
            self.fh.seek(0,2)
            #print(self.readpos,self.fh.tell())
            if self.readpos > self.fh.tell():
                self.readpos = self.fh.tell()
            #print('Readpos restored to ',self.readpos)
            

    def _savepos(self):
        if hasattr(self, '_indexfile'):
            fh = open(self._indexfile, "wb")
            fh.write(str(self.readpos))
            fh.close()


if __name__ == "__main__":
    q = FileQueue()
    print(q.empty())
    q.enqueue({'t': 'test'})
    print(q.empty())
    q.enqueue([1,2,3])
    print(q.empty())
    x = q.dequeue()
    print(x)
    print(x['t'])
    print(q.empty())
    x = q.dequeue()
    print(x)
    print(x[0])
    print(q.empty())
    x = q.dequeue()
    print(x)

    # Persistent queue
    pq = FileQueue('testing',True)
    if pq.empty():
        print('Initialising persistent queue')
        for i in range(6):
            pq.enqueue(i)
    else:
        print('Reading from existing queue')
    for i in range(3):
        x = pq.dequeue()
        print('Item %d: %s' % (i,str(x)))

    