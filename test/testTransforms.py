import unittest
from megaminx.megaminx import Megaminx, solved
from megaminx.transform import Transform
from megaminx.solver import Solver

class TestTransforms(unittest.TestCase):

    def test_Transform(self):
      t = Transform({'r':'g','g':'b','b':'r'})
      self.assertEqual(t['r'],'g')
      self.assertEqual(t.transform('rrgggbx'),'ggbbbrx')
      self.assertEqual(t.invert('ggbbbrx'),'rrgggbx')

    def test_get_rotation_transforms(self):
      m = Megaminx()
      xforms = m.get_rotation_transforms('w')
      self.assertEqual(len(xforms),4)
      xform = xforms[0]
      self.assertEqual(xform['w'],'w')
      self.assertEqual(xform['x'],'x')
      tf = ('r','G','p','Y','B','r')
      for i in range(5):
        self.assertEqual(xform[tf[i]],tf[i+1])
      bf = ('b','o','g','k','y','b')
      for i in range(5):
        self.assertEqual(xform[bf[i]],bf[i+1])

    def test_get_transforms(self):
      m = Megaminx()
      xforms = m.get_transforms()
      self.assertEqual(len(xforms),24)
      for i in range(4):
        self.assertEqual(xforms[i]['w'],'w')
        self.assertEqual(xforms[i]['x'],'x')
      for i in range(4,24):
        self.assertNotEqual(xforms[i]['w'],'w')
        self.assertNotEqual(xforms[i]['x'],'x')

    def test_tranformed_cache_lookup(self):
      global solved
      m = Megaminx()
      s = Solver()
      m.faces['w'].rotate_clockwise()
      m.faces['r'].rotate_anticlockwise()
      state = str(m)
      #print(state)
      solution = s.cache.get(state).strip()
      self.assertEqual(solution,'r> w<')
      m2 = Megaminx()
      m2.parse(state)
      m2.apply(solution)
      self.assertEqual(str(m2), solved)
      for t in m.get_transforms():
        tstate = m.transformed_state(t)
        #print(tstate)
        tsolution = t.transform(solution)
        #print(tsolution)
        m2.parse(solved)
        m2.unapply(tsolution)
        self.assertEqual(tstate,str(m2))
      for t in m.get_transforms():
        tstate = m.transformed_state(t)
        tsolution = t.transform(solution)
        m2.parse(tstate)
        m2.apply(tsolution)
        self.assertEqual(str(m2), solved)
      for t in m.get_transforms():
        tstate = m.transformed_state(t)
        tsolution = s.cache.get(tstate).strip()
        solution = t.invert(tsolution)
        self.assertEqual(solution,'r> w<')

    def test_tranformed_cache_lookup_colours(self):
      global solved
      m = Megaminx()
      s = Solver()
      m.faces['w'].rotate_clockwise()
      m.faces['r'].rotate_anticlockwise()
      state = str(m)
      #print(state)
      solution = s.cache.get(state).strip()
      self.assertEqual(solution,'r> w<')
      m2 = Megaminx()
      m2.parse(state)
      m2.apply(solution)
      self.assertEqual(str(m2), solved)
      for t in m.get_colour_transforms():
        tstate = m.transformed_state(t)
        #print(tstate)
        tsolution = t.transform(solution)
        #print(tsolution)
        m2.parse(solved)
        m2.unapply(tsolution)
        self.assertEqual(tstate,str(m2))
      for t in m.get_colour_transforms():
        tstate = m.transformed_state(t)
        tsolution = t.transform(solution)
        m2.parse(tstate)
        m2.apply(tsolution)
        self.assertEqual(str(m2), solved)
      for t in m.get_colour_transforms():
        tstate = m.transformed_state(t)
        tsolution = s.cache.get(tstate).strip()
        solution = t.invert(tsolution)
        self.assertEqual(solution,'r> w<')

    def test_tranformed_cache_lookup_combined(self):
      global solved
      m = Megaminx()
      s = Solver()
      m.faces['w'].rotate_clockwise()
      m.faces['r'].rotate_anticlockwise()
      state = str(m)
      solution = s.cache.get(state).strip()
      self.assertEqual(solution,'r> w<')
      m2 = Megaminx()
      for t1 in m.get_transforms():
        t1state = m.transformed_state(t1)
        t1solution = s.cache.get(t1state).strip()
        solution = t1.invert(t1solution)
        self.assertEqual(solution,'r> w<')
        for t2 in m.get_colour_transforms():
          m2.parse(t1state)
          t2state = m2.transformed_state(t2)
          t2solution = s.cache.get(t2state).strip()
          solution = t1.invert(t2.invert(t2solution))
          self.assertEqual(solution,'r> w<')


if __name__ == '__main__':
    unittest.main()
