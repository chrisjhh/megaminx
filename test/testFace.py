import unittest
from megaminx.megaminx import Megaminx

class TestFace(unittest.TestCase):

    def test_opposite_face(self):
      m = Megaminx()
      self.assertEqual(m.faces['w'].opposite_face().colour,'x')
      self.assertEqual(m.faces['x'].opposite_face().colour,'w')
      self.assertEqual(m.faces['r'].opposite_face().colour,'o')
      self.assertEqual(m.faces['o'].opposite_face().colour,'r')
      self.assertEqual(m.faces['G'].opposite_face().colour,'g')
      self.assertEqual(m.faces['g'].opposite_face().colour,'G')
      self.assertEqual(m.faces['p'].opposite_face().colour,'k')
      self.assertEqual(m.faces['k'].opposite_face().colour,'p')
      self.assertEqual(m.faces['Y'].opposite_face().colour,'y')
      self.assertEqual(m.faces['y'].opposite_face().colour,'Y')
      self.assertEqual(m.faces['B'].opposite_face().colour,'b')
      self.assertEqual(m.faces['b'].opposite_face().colour,'B')

if __name__ == '__main__':
    unittest.main()
