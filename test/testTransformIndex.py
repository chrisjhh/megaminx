import unittest
from megaminx.megaminx import Megaminx
from megaminx.TransformIndex import TransformIndex

class TestTransformIndex(unittest.TestCase):

    def test_TransformIndex(self):
        cache = TransformIndex()
        m = Megaminx()
        m.faces['w'].rotate_clockwise()
        m.faces['r'].rotate_anticlockwise()
        state = str(m)
        solution = 'r> w<'
        cache[state] = solution
        value = cache[state]
        self.assertEqual(value,'r> w<')
        # Check all colour transforms
        for t in m.get_colour_transforms():
            tstate = m.transformed_state(t)
            self.assertIn(tstate,cache)
            tvalue = cache[tstate]
            self.assertEqual(tvalue,t.transform(solution))
        m2 = Megaminx()
        for t1 in m.get_transforms():
            t1state = m.transformed_state(t1)
            self.assertIn(t1state,cache)
            t1value = cache[t1state]
            self.assertEqual(t1value,t1.transform(solution))
            m2.parse(t1state)
            for t2 in m.get_colour_transforms():
                t2state = m2.transformed_state(t2)
                self.assertIn(t2state,cache)
                t2value = cache[t2state]
                self.assertEqual(t2value,t2.transform(t1value))
                self.assertEqual(t2value,t2.transform(t1.transform(solution)))

if __name__ == '__main__':
    unittest.main()
