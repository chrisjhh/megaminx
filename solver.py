"""Solver for megaminx"""

from . import megaminx
from .filequeue import FileQueue
from .resultscache import ResultsCache
import tempfile
import os

def solve(ostate):
    m = megaminx.Megaminx()
    m.parse(ostate)

    if str(m) == megaminx.solved:
        print("Already solved!")
        return

    temp = tempfile.gettempdir()
    queuefile = os.path.join(temp,'megaminx_queue')
    q = FileQueue(queuefile,True)

    cachedir = os.path.join(temp,'megaminx_cache')
    cache = ResultsCache(cachedir)

    result = cache.retrieve(m)
    if result:
        report(result)
        return

    if q.empty():
        q.enqueue(megaminx.solved)

    most_steps = 0

    while not q.empty():
        state = q.dequeue()
        m.parse(state)
        moves = "" if state == megaminx.solved else cache.retrieve(m)
        steps = len(moves.split(" "))
        if  steps > most_steps:
            print("%d steps" % steps)
            most_steps = steps
      
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
                if new_state == ostate:
                    report(new_moves)
                    cache.store(m,new_moves)
                    q.close()
                    return
                elif not cache.retrieve(m):
                    # New state. Explore more from here
                    cache.store(m,new_moves)
                    q.enqueue(new_state)
                    

def report(result):
    print("Solved!")
    print(result)

if __name__ == "__main__":
    m = megaminx.Megaminx()
    #solve(str(m))
    #m.faces['w'].facets[6] = 'Y'
    #m.faces['p'].facets[0] = 'w'
    #m.faces['Y'].facets[2] = 'p'
    #m.faces['w'].rotate_clockwise()
    m.faces['x'].rotate_anticlockwise()
    m.faces['o'].rotate_clockwise()
    m.faces['B'].rotate_clockwise()
    m.faces['Y'].rotate_clockwise()
    m.faces['r'].rotate_anticlockwise()
    solve(str(m))

