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
        量子論の計算手続きをまとめたclassです．
        
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
		make operators
		
		.. seealso::
		
			Module :qmap:Qmap:`op0` and Module :qmap:Qmap:`op1`
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
        make operator :math:`\exp[-\\frac{i}{\hbar}V(\hat{q})]`
        """
        self.operator[0] = numpy.exp(-1.j*twopi*self.map.ifunc0(x)/self.scaleinfo.h)
    
    def op1(self,x):
        """
        make operator :math:`\exp[-\\frac{i}{\hbar}T(\hat{p})]`        
        """
        self.operator[1] = numpy.exp(-1.j*twopi*self.map.ifunc1(x)/self.scaleinfo.h)
        
    def operate(self):
        """
        time evolution of a given state :math:`|\psi_0\\rangle` 

    	.. math::
    	
    		\langle q | \psi_1 \\rangle = \langle q |\hat{U} | \psi_0 \\rangle
    		
    	.. note::
    	
    		特に理由がなければ時間発展にはevolve() を使ってください．
        
        
        """
        pvec = numpy.fft.fft(self.operator[0]*self.stateIn)
        qvec = numpy.fft.ifft(self.operator[1]*pvec)
        self.stateOut = State(self.scaleinfo, qvec)
        
    def setInit(self, state):
        """ 
		set initial state

		Parameters
        ----------
        
        state: State class instance
        		
        """
        if not isinstance(state, State):
            raise TypeError("expected State:",type(state))
        self.stateIn = state.copy()

    def getState(self):
    	""" return null state"""
        return State(self.scaleinfo)

    def getIn(self):
    	""" return previous state of time evolution"""
        return self.stateIn

    def getOut(self):
        """ return time evolved state"""
        return self.stateOut

    def pull(self):
    	"""
    	substitution time evolved state into previous state
    	
    	.. math::
    		
    		|\psi_0 \\rangle = |\psi_1 \\rangle 
    	
    	"""
        self.stateIn = self.stateOut
    
    def evolve(self):
        """ 
		iteative operation of :math:`\hat{U}` for a given initial state
        """
        self.operate()
        self.pull()

    def setMatrix(self):
        """ 
        make time evolution operator matrix in position representation
        
        .. math::
        
        	\langle q_1 | \hat{U} | q_0\\rangle
        
        where 
        
        .. math::
        	
        	\hat{U} = \exp[-\\frac{i}{\hbar}T(\hat{p})]\exp[-\\frac{i}{\hbar}V(\hat{q})]
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
        return eigenvalues and eigenvectors of time evolution operator matrix 
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
    	"""
    	return time evolution operator matrix
    	"""
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