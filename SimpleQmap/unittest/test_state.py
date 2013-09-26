import unittest
import numpy as np
import SimpleQmap as S


class TestState(unittest.TestCase):
    def test_ScaleInfo(self):
    	dim = np.random.randint(1,100)
    	xmax = np.random.random()
    	xmin = -xmax
    	ymax = np.random.random()
    	ymin = -ymax
    	domain = [[xmin, xmax], [ymin, ymax]]
    	scl = S.ScaleInfo(dim=dim, domain=domain)
    	self.assertTrue(scl.dim == dim)
    	self.assertTrue(scl.domain == domain)
    	x = np.linspace(xmin, xmax, dim, endpoint=False)
    	y = np.linspace(ymin, ymax, dim, endpoint=False)    	
    	self.assertTrue(np.all(scl.x[0] == x))
    	self.assertTrue(np.all(scl.x[1] == y))
        xmin, xmax = np.random.random(), np.random.random()
        ymin, ymax = np.random.random(), np.random.random()
        domain = [[xmin, xmax],[ymin, ymax]]
        with self.assertRaises(ValueError):
        	S.ScaleInfo(dim, domain)
    	
if __name__ == '__main__':
    unittest.main()
