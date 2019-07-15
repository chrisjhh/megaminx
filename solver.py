"""Solver for megaminx"""

from . import megaminx
from .filequeue import FileQueue
from .resultscache import ResultsCache
import tempfile
import os
import shutil
import cProfile
import signal
from diskcache import Deque
from TransformIndex import Index

class DelayedKeyboardInterrupt(object):
    def __enter__(self):
        self.signal_received = False
        self.old_handler = signal.signal(signal.SIGINT, self.handler)

    def handler(self, sig, frame):
        self.signal_received = (sig, frame)
        #logging.debug('SIGINT received. Delaying KeyboardInterrupt.')

    def __exit__(self, type, value, traceback):
        signal.signal(signal.SIGINT, self.old_handler)
        if self.signal_received:
            self.old_handler(*self.signal_received)

class Solver:

    def __init__(self):
        self.megaminx = megaminx.Megaminx()
        temp = tempfile.gettempdir()
        queuefile = os.path.join(temp,'megaminx_queue')
        self.queue = Deque(directory=queuefile)
        cachedir = os.path.join(temp,'megaminx_cache')
        self.cache = Index(cachedir)
        #self.queue.clear()
        #self.cache.clear()


    def _initialise_forwards(self):
        temp = tempfile.gettempdir()
        queuefile = os.path.join(temp,'megaminx_forward_queue')
        cachedir = os.path.join(temp,'megaminx_forward_cache')
                
        self.forward_queue = Deque(directory=queuefile)   
        self.forward_cache = Index(cachedir)
        # Check it to see if it begins with the same state
        if 'ostate' in self.forward_cache and self.forward_cache['ostate'] != self.ostate:
            self.forward_queue.clear()
            self.forward_cache.clear()
        if not 'ostate' in self.forward_cache:
            with DelayedKeyboardInterrupt():
                self.forward_queue.append(self.ostate)
                self.forward_cache['ostate'] = self.ostate


    def _clear_forwards(self):
        self.forward_queue.clear()
        self.forward_cache.clear()

    def solve(self,ostate):
        m = self.megaminx
        m.parse(ostate)
        self.ostate = ostate

        if str(m) == megaminx.solved:
            print("Already solved!")
            return

        cache = self.cache

        result = cache.get(ostate)
        if result:
            report(result)
            return

        q = self.queue
        if not len(q):
            q.append(megaminx.solved)

        most_steps = 0

        while len(q):
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
        state = q[0]
        #print(state)
        m.parse(state)
        #print(len(cache))
        moves = "" if state == megaminx.solved else cache[state]
        #print(moves)
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
                #print('b %s' % reverse_action)
                new_moves = reverse_action + ' ' + moves
                new_state = str(m)
                if new_state == self.ostate:
                    # Solved!
                    with DelayedKeyboardInterrupt():
                        cache[new_state] = new_moves
                    return new_moves
                elif not new_state in cache:
                    # New state. Explore more from here
                    with DelayedKeyboardInterrupt():
                        cache[new_state] = new_moves
                        q.append(new_state)
                        #print(len(cache))
        # Done with item in queue now
        with DelayedKeyboardInterrupt():
            q.popleft()

    def process_forward(self):
        m = self.megaminx
        cache = self.forward_cache
        q = self.forward_queue
        state = q[0]
        m.parse(state)
        moves = "" if state == self.ostate else cache[state]
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
                #print('f %s' % action)
                new_moves = moves + ' ' + action if moves else action
                new_state = str(m)
                join_up_moves = self.cache.get(new_state)
                if join_up_moves:
                    # Solved!
                    solution = new_moves + ' ' + join_up_moves
                    # Dispose of forwards cache
                    q.clear()
                    cache.clear()
                    return solution
                elif not new_state in cache:
                    # New state. Explore more from here
                    with DelayedKeyboardInterrupt():
                        cache[new_state] = new_moves
                        q.append(new_state)
        # Done with item in queue now
        with DelayedKeyboardInterrupt():
            q.popleft()


    def double_ended_solve(self,ostate):
        m = self.megaminx
        m.parse(ostate)
        self.ostate = ostate

        if str(m) == megaminx.solved:
            print("Already solved!")
            return

        cache = self.cache

        result = cache.get(ostate)
        if result:
            report(result)
            return

        q = self.queue
        if not len(q):
            with DelayedKeyboardInterrupt():
                q.append(megaminx.solved)

        self._initialise_forwards()

        most_steps = 0

        while len(q):
            
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
                print("%d steps (%d,%d)" % (steps,self.backward_steps,self.forward_steps))
                most_steps = steps              
            

def report(result):
    print("Solved!")
    print(result)

if __name__ == "__main__":
    m = megaminx.Megaminx()
    #solve(str(m))
    m.faces['w'].facets[6] = 'Y'
    m.faces['p'].facets[0] = 'w'
    m.faces['Y'].facets[2] = 'p'
    # m.faces['w'].rotate_clockwise()
    # m.faces['x'].rotate_clockwise()
    # m.faces['Y'].rotate_clockwise()
    # m.faces['w'].rotate_clockwise()
    # m.faces['r'].rotate_clockwise()
    # m.faces['G'].rotate_clockwise()
    # m.faces['r'].rotate_anticlockwise()
    #m.faces['g'].rotate_anticlockwise()
    s = Solver()
    s.double_ended_solve(str(m))
    #s.solve(str(m))

