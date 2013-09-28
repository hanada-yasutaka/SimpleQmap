import unittest
import numpy as np
import SimpleQmap as S


class TestState(unittest.TestCase):
    def setUp(self):
        self.dim = int(np.random.randint(1,100)*2)
    	xmax = np.random.random()
    	xmin = -xmax
    	ymax = np.random.random()
    	ymin = -ymax
        self.domain = [[xmin, xmax], [ymin, ymax]]
        k=np.random.random()
        self.scl = S.ScaleInfo(dim=self.dim, domain=self.domain)
        self.map = S.StandardMap(k=k)
        self.qmap = S.Qmap(map = self.map, dim=self.dim, domain=self.domain)


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
        xmin, xmax = np.random.random(), -np.random.random()
        ymin, ymax = np.random.random(), -np.random.random()
        domain = [[xmin, xmax],[ymin, ymax]]

        with self.assertRaises(ValueError):
            S.ScaleInfo(dim, domain)
        	
    def test_transform(self):
		state = S.State(self.scl)
		q_c = np.random.random()
		p_c = np.random.random()
		cs = state.cs(q_c,p_c)

		self.assertAlmostEqual(cs.norm(), 1.0)
		self.assertTrue(isinstance(cs.norm(),np.float64))
		cs_prep = cs.q2p()
		self.assertAlmostEqual(cs_prep.norm(), 1.0)
		self.assertTrue(isinstance(cs_prep,S.State))
		cs_qrep = cs_prep.p2q()
		self.assertAlmostEqual(cs_qrep.norm(), 1.0)
		self.assertTrue(isinstance(cs_prep,S.State))		
		ovl = np.abs(np.sum(cs*np.conj(cs_qrep)))		
		self.assertAlmostEqual(ovl, 1.0)
		inn = cs.qrep().inner(cs.prep())
		self.assertTrue(isinstance(inn, np.complex128))
		self.assertNotAlmostEqual(np.abs(inn*np.conj(inn)), 1.0)

    	
    	
if __name__ == '__main__':
    unittest.main()
