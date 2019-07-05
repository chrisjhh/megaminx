"""Solver for megaminx"""

from . import megaminx
from .filequeue import FileQueue
from .resultscache import ResultsCache
import tempfile
import os
import shutil

class Solver:

    def __init__(self):
        self.megaminx = megaminx.Megaminx()
        temp = tempfile.gettempdir()
        queuefile = os.path.join(temp,'megaminx_queue')
        self.queue = FileQueue(queuefile,True)
        cachedir = os.path.join(temp,'megaminx_cache')
        self.cache = ResultsCache(cachedir)

    def _initialise_forwards(self):
        temp = tempfile.gettempdir()
        queuefile = os.path.join(temp,'megaminx_forward_queue')
        cachedir = os.path.join(temp,'megaminx_forward_cache')
        if os.path.isfile(queuefile):
            # Check it to see if it begins with the same state
            fh = open(queuefile, "rb")
            ostate = fh.readline()
            fh.close()
            if ostate != self.ostate:
                # Belongs to a different case
                # Remove it
                self._clear_forwards()
                
        self.forward_queue = FileQueue(queuefile,True)   
        self.forward_cache = ResultsCache(cachedir)

        if self.forward_queue.empty():
            self.forward_queue.enqueue(self.ostate)

    def _clear_forwards(self):
        temp = tempfile.gettempdir()
        queuefile = os.path.join(temp,'megaminx_forward_queue')
        cachedir = os.path.join(temp,'megaminx_forward_cache')
        os.unlink(queuefile)
        if os.path.isfile(queuefile + '_i'):
            os.unlink(queuefile + '_i')
        if os.path.isdir(cachedir):
            shutil.rmtree(cachedir)

    def solve(self,ostate):
        m = self.megaminx
        m.parse(ostate)
        self.ostate = ostate

        if str(m) == megaminx.solved:
            print("Already solved!")
            return

        cache = self.cache

        result = cache.retrieve(m)
        if result:
            report(result)
            return

        q = self.queue
        if q.empty():
            q.enqueue(megaminx.solved)

        most_steps = 0

        while not q.empty():
            solved = self.process_backward()
            if solved:
                report(solved)
                return
            if self.backward_steps > most_steps:
                print("%d steps" % self.backward_steps)
                most_steps = self.backward_steps

    def process_backward(self):
        m = self.megaminx
        cache = self.cache
        q = self.queue
        state = q.dequeue()
        m.parse(state)
        moves = "" if state == megaminx.solved else cache.retrieve(m)
        self.backward_steps = len(moves.split(" "))
      
        for col in m.colours:
            for act in range(2):
                # Reset
                m.parse(state)
                if act == 0:
                    m.faces[col].rotate_clockwise()
                else:
                    m.faces[col].rotate_anticlockwise()
                reverse_action = col + ('<', '>')[act]
                new_moves = reverse_action + ' ' + moves
                new_state = str(m)
                if new_state == self.ostate:
                    # Solved!
                    cache.store(m,new_moves)
                    return new_moves
                elif not cache.retrieve(m):
                    # New state. Explore more from here
                    cache.store(m,new_moves)
                    q.enqueue(new_state)

    def process_forward(self):
        m = self.megaminx
        cache = self.forward_cache
        q = self.forward_queue
        state = q.dequeue()
        m.parse(state)
        moves = "" if state == self.ostate else cache.retrieve(m)
        self.forward_steps = len(moves.split(" "))
      
        for col in m.colours:
            for act in range(2):
                # Reset
                m.parse(state)
                if act == 0:
                    m.faces[col].rotate_clockwise()
                else:
                    m.faces[col].rotate_anticlockwise()
                action = col + ('>', '<')[act]
                new_moves = moves + ' ' + action if moves else action
                new_state = str(m)
                join_up_moves = self.cache.retrieve(m)
                if join_up_moves:
                    # Solved!
                    solution = new_moves + ' ' + join_up_moves
                    # Dispose of forwards cache
                    q.close()
                    self._clear_forwards()
                    return solution
                elif not cache.retrieve(m):
                    # New state. Explore more from here
                    cache.store(m,new_moves)
                    q.enqueue(new_state)


    def double_ended_solve(self,ostate):
        m = self.megaminx
        m.parse(ostate)
        self.ostate = ostate

        if str(m) == megaminx.solved:
            print("Already solved!")
            return

        cache = self.cache

        result = cache.retrieve(m)
        if result:
            report(result)
            return

        q = self.queue
        if q.empty():
            q.enqueue(megaminx.solved)

        self._initialise_forwards()

        most_steps = 0

        while not q.empty():
            
            solved = self.process_backward()
            if solved:
                report(solved)
                return
            solved = self.process_forward()
            if solved:
                report(solved)
                return
            steps = self.backward_steps + self.forward_steps
            if  steps > most_steps:
                print("%d steps" % steps)
                most_steps = steps              

def report(result):
    print("Solved!")
    print(result)

if __name__ == "__main__":
    m = megaminx.Megaminx()
    #solve(str(m))
    #m.faces['w'].facets[6] = 'Y'
    #m.faces['p'].facets[0] = 'w'
    #m.faces['Y'].facets[2] = 'p'
    m.faces['w'].rotate_clockwise()
    m.faces['x'].rotate_clockwise()
    m.faces['Y'].rotate_clockwise()
    m.faces['w'].rotate_clockwise()
    m.faces['r'].rotate_clockwise()
    m.faces['G'].rotate_clockwise()
    m.faces['r'].rotate_anticlockwise()
    m.faces['g'].rotate_anticlockwise()
    s = Solver()
    s.double_ended_solve(str(m))
    #s.solve(str(m))

