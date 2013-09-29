import unittest
import numpy as np
import SimpleQmap as S


class TestState(unittest.TestCase):
    def setUp(self):
        self.dim = int(np.random.randint(1,100)*2)
        xmax = np.random.random()+1.0
        xmin = -xmax
        ymax = np.random.random()+1.0
        ymin = -ymax
        self.domain = [[xmin, xmax], [ymin, ymax]]
        k=np.random.random()
        self.scl = S.ScaleInfo(dim=self.dim, domain=self.domain)
        self.map = S.StandardMap(k=k)
        self.qmap = S.Qmap(map = self.map, dim=self.dim, domain=self.domain)
    def print_setting(self):
        print("")
        print("matrix size: (%d, %d)" % (self.dim, self.dim) )
        print("domain:[%.3f, %.3f]x[%.3f, %.3f]" % (self.domain[0][0],self.domain[0][1], self.domain[1][0],self.domain[1][1]))
        print("")
        
    def test_unitarilty(self):
        self.print_setting()
        mat = self.qmap.getMatrix()
        iden =  mat.dot(np.conj(mat.transpose()))
        eye = np.eye(self.dim) + 0.j
        [self.assertAlmostEqual(iden[i][j], eye[i][j]) for i in range(self.dim) for j in range(self.dim) ]
        
    def test_eigenvalues(self):
        self.print_setting()
        evals, evecs = self.qmap.eigen()
        norm = np.abs(evals*np.conj(evals))
        
        [self.assertAlmostEqual(x, 1.0) for x in norm]
        
    def test_orthogonality(self):
        eval, evecs = self.qmap.eigen()
        for i in range(self.dim):
            ovl = [evecs[i].inner(evecs[j]) for j in range(self.dim)]
            ovl2 = [np.abs(x*np.conj(x)) for x in ovl]
            [self.assertAlmostEqual(ovl2[j],0.0) for j in range(self.dim) if i!=j]
            self.assertAlmostEqual(ovl2[i], 1.0)
        
if __name__ == '__main__':
    unittest.main()
