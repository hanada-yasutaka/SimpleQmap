#-*- coding:utf-8 -*-
import numpy
from state import *
twopi = 2.0*numpy.pi

class Qmap(object):
    def __init__(self, map, dim, domain):
        #ScaleInfo.__init__(self, dim , domain)
        self.map = map
        self.scaleinfo = ScaleInfo(dim, domain)
        self.dim =self.scaleinfo.dim
        self.setOperate()

        self.stateIn = State(self.scaleinfo)
        self.stateOut = State(self.scaleinfo)


    def setOperate(self):
        self.operator = [State(self.scaleinfo) for i in range(2)]
        self.op0(self.scaleinfo.x[0])
        if (self.scaleinfo.domain[1][0] == 0.0):
            self.op1(self.scaleinfo.x[1])
        elif (numpy.abs(self.scaleinfo.domain[1][0]) == numpy.abs(self.scaleinfo.domain[1][1])):
            self.op1(numpy.fft.fftshift(self.scaleinfo.x[1]))
        else:
            raise ValueError("unexpected domain.")

    def op0(self,x):
        self.operator[0] = numpy.exp(-1.j*twopi*self.map.ifunc0(x)/self.scaleinfo.h)
    
    def op1(self,x):
        self.operator[1] = numpy.exp(-1.j*twopi*self.map.ifunc1(x)/self.scaleinfo.h)
        
    def operate(self):
        pvec = numpy.fft.fft(self.operator[0]*self.stateIn)
        qvec = numpy.fft.ifft(self.operator[1]*pvec)
        self.stateOut = State(self.scaleinfo, qvec)
        
    def setInit(self, state):
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
        self.operate()
        self.pull()

    def setMatrix(self):
        self.matrix = numpy.zeros([self.dim, self.dim],dtype=numpy.complex128)
        
        for i in range(self.dim):
            vec = State(self.scaleinfo)
            vec.insert(i,1.0+0j)
            self.setInit(vec)
            self.operate()
            self.matrix[i,:] = self.stateOut
        self.matrix = numpy.transpose(self.matrix)

    def eigen(self):
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