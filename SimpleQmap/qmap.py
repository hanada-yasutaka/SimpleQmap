#-*- coding:utf-8 -*-
"""
qmap.py

author: Yasutaka Hanada (2013/05/17)

量子系の計算を行います．
具体的には，
    1. 与えられた初期条件の時間発展を行います
    2. 系の時間発展演算子の固有値及び固有ベクトルを求めます．
    
"""

import numpy
from state import *
twopi = 2.0*numpy.pi

class Qmap(object):
    def __init__(self, map, dim, domain):
        """
        システムの決定を行います
        
        Parameter
        ----------
        map : map instance
        
        dim : integer
            Hilbert Space dimension.
            
        domain:
            region of the calculation domain.
            
        """
        self.map = map
        self.scaleinfo = ScaleInfo(dim, domain)
        self.dim =self.scaleinfo.dim
        self.setOperate()

        self.stateIn = State(self.scaleinfo)
        self.stateOut = State(self.scaleinfo)


    def setOperate(self):
        """
        時間発展演算子をsetします
        fftの使用するため，演算順序を適当に変更しています．
        """ 
        self.operator = [State(self.scaleinfo) for i in range(2)]
        self.op0(self.scaleinfo.x[0])
        if (self.scaleinfo.domain[1][0] == 0.0):
            self.op1(self.scaleinfo.x[1])
        elif (numpy.abs(self.scaleinfo.domain[1][0]) == numpy.abs(self.scaleinfo.domain[1][1])):
            self.op1(numpy.fft.fftshift(self.scaleinfo.x[1]))
        else:
            raise ValueError("unexpected domain.")

    def op0(self,x):
        """
        set operator exp(-iV(q)/hbar)
        """
        self.operator[0] = numpy.exp(-1.j*twopi*self.map.ifunc0(x)/self.scaleinfo.h)
    
    def op1(self,x):
        """
        set operator exp(-iT(p)/hbar)
        """
        self.operator[1] = numpy.exp(-1.j*twopi*self.map.ifunc1(x)/self.scaleinfo.h)
        
    def operate(self):
        """ <q'|exp(-iT(p)/hbar)exp(-iV(q)/hbar)|q> <q| initial > """
        pvec = numpy.fft.fft(self.operator[0]*self.stateIn)
        qvec = numpy.fft.ifft(self.operator[1]*pvec)
        self.stateOut = State(self.scaleinfo, qvec)
        
    def setInit(self, state):
        """ 
        初期条件尾セット
        """
        if not isinstance(state, State):
            raise TypeError("expected State:",type(state))
        self.stateIn = state.copy()

    def getState(self):
        return State(self.scaleinfo)

    def getIn(self):
        return self.stateIn

    def getOut(self):
        return self.stateOut

    def pull(self):
        self.stateIn = self.stateOut
    
    def evol(self):
        """ 
        1step 時間発展します．
        """
        self.operate()
        self.pull()

    def setMatrix(self):
        """ 
        make matrix :<q'|exp(-iT(p)/hbar)exp(-iV(q)/hbar)|q>
        """ 
        self.matrix = numpy.zeros([self.dim, self.dim],dtype=numpy.complex128)
        
        for i in range(self.dim):
            vec = State(self.scaleinfo)
            vec.insert(i,1.0+0j)
            self.setInit(vec)
            self.operate()
            self.matrix[i,:] = self.stateOut
        self.matrix = numpy.transpose(self.matrix)

    def eigen(self):
        """
        Return eigenvalues and eigenvectors of matrix 
        <q'|exp(-iT(p)/hbar)exp(-iV(q)/hbar)|q>
        """ 
        try:
            evals, evecs = numpy.linalg.eig(self.matrix)
            vecs = [State(self.scaleinfo, evec) for evec in evecs.transpose()]
            return evals, vecs 
        except AttributeError:
            self.setMatrix()
            evals, evecs = numpy.linalg.eig(self.matrix)
            vecs = [State(self.scaleinfo, evec) for evec in evecs.transpose()]                        
            return evals, vecs
        
    def getMatrix(self):
        try:
            return self.matrix
        except AttributeError:
            self.setMatrix()
            return self.matrix

def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _test() 