import unittest
import SimpleQmap as S
import numpy as np
import os

class TestEigen(unittest.TestCase):
    def setUp(self):
        self.dim = int(np.random.randint(1,50)*2)
        xmax = np.random.random()+1.0
        xmin = -xmax
        ymax = np.random.random()+1.0
        ymin = -ymax
        self.domain = [[xmin, xmax], [ymin, ymax]]
        k=np.random.random()
        self.map = S.StandardMap(k=k)
        self.qmap = S.Qmap(map = self.map, dim=self.dim, domain=self.domain)
        self.evals, self.evecs = self.qmap.eigen()
        
    def test_unitality(self):
        z0 = np.array([x*np.conj(x) for x in self.evals])
        z1 = np.ones(z0.shape) + 0.j
        np.testing.assert_array_almost_equal(z0, z1,12)
    
    def test_saveload(self):
        fname="data.dat"
        for vec0 in self.evecs:
            vec0.savetxt(fname,rep="q")
            vec1 = S.loadtxt(fname,False)
            np.testing.assert_array_almost_equal(vec0,vec1,12)

            vec0.savetxt(fname,rep="p")
            vec1 = S.loadtxt(fname,False)
            np.testing.assert_array_almost_equal(vec0,vec1,12)
        os.remove(fname)

    def test_orthogonality(self):
        for i,vec in enumerate(self.evecs):
            x = np.array([vec.inner(x) for x in self.evecs])
            y = np.array([1e-16+1.j*1e-16]*len(self.evecs))
            y[i] = 1.0 + 0.j
            np.testing.assert_array_almost_equal(x,y,10)


if __name__ == '__main__':
    unittest.main()


