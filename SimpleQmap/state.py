# -*- coding:utf-8 -*-
"""
state.py

Basic Setting and Quantum states
"""

import numpy
twopi = 2.0*numpy.pi

        
class ScaleInfo(object):
    """
    
    ScaleInfoは位相空間の定義域を設定するためのclassです．
    
    Parameters
    ----------
    dim : int
        Hilbert Space dimension
    domain: list
        domain of phase space. expected 2 by 2 list, e.g., [[qmin,qmax], [pmin, pmax]]
    
    Examples
    ----------
    >>> from qmap import ScaleInfo
    >>> scl = ScaleInfo(10, [[0,1],[-0.5,0.5]])
    >>> print(scl.x[0])
    [ 0.   0.1  0.2  0.3  0.4  0.5  0.6  0.7  0.8  0.9]
    >>> print(scl.x[1])
    [-0.5 -0.4 -0.3 -0.2 -0.1  0.   0.1  0.2  0.3  0.4]
    >>> print(scl.h) # scl.getPlanck()
    0.1
    """
    def __init__(self, dim, domain):
        self.dim = dim
        self.__setDomain(domain)
    
    def __setDomain(self, domain):
        if domain[0][0] > domain[0][1]:
            raise ValueError("qmin > qmax")
        if domain[1][0] > domain[1][1]:
            raise ValueError("pmin < qmax")
        
        self.domain = domain
        self.x = [numpy.linspace(self.domain[i][0], self.domain[i][1], self.dim, endpoint=False) for i in range(2)]
        self.h = self.getPlanck()

    def getPlanck(self):
        """ return effective planck constant """
        W = (self.domain[0][1] -self.domain[0][0])*(self.domain[1][1] - self.domain[1][0])
        return W/self.dim

    def getX(self):
        """ return [q, p] """
        return self.x

class State(numpy.ndarray):
    """
    
    State はScaleInfoで定義された上で複素ベクトルを提供します．
    numpy.ndarrayを継承しています．
    
    Parameters
    ----------
    scaleinfo : ScaleInfo instance

    data: (optional) State
        if data is None, return a new array of given scaleinfo, filled with zeros.
        if data is not None, return a new array of given data, 
        Note that length data must be same scaleinfo dimnsion.

    Examples
    ----------
    >>> from qmap import State, ScaleInfo
    >>> scl = ScaleInfo(10, [[0,1],[-0.5,0.5]])
    >>> State(scl, range(10))
    State([ 0.+0.j,  1.+0.j,  2.+0.j,  3.+0.j,  4.+0.j,  5.+0.j,  6.+0.j,
            7.+0.j,  8.+0.j,  9.+0.j])
    >>> vec = State(scl)
    >>> print(vec)
    [ 0.+0.j  0.+0.j  0.+0.j  0.+0.j  0.+0.j  0.+0.j  0.+0.j  0.+0.j  0.+0.j
      0.+0.j]
    >>> print(vec.scaleinfo.x[0])
    [ 0.   0.1  0.2  0.3  0.4  0.5  0.6  0.7  0.8  0.9]
    >>> newvec = vec.copy()
    >>> print(newvec)
    [ 0.+0.j  0.+0.j  0.+0.j  0.+0.j  0.+0.j  0.+0.j  0.+0.j  0.+0.j  0.+0.j
      0.+0.j]
    >>> print(newvec.scaleinfo.h)
    0.1
    >>> newvec[0] = 1.0+0.j
    >>> vec
    State([ 0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,
            0.+0.j,  0.+0.j,  0.+0.j])
    >>> newvec
    State([ 1.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,
            0.+0.j,  0.+0.j,  0.+0.j])
    
    See Also
    ----------
    Numpy Document <http://docs.scipy.org/doc/numpy/user/basics.subclassing.html>
    """
    
    def __new__(cls, scaleinfo, data=None):
        if not isinstance(scaleinfo , ScaleInfo): raise TypeError("expected type ScaleInfo", type(scaleinfo))
        if data == None:
            data = numpy.zeros(scaleinfo.dim)
        obj = numpy.asarray(data, dtype=numpy.complex128).view(cls)
        obj.scaleinfo = scaleinfo
        return obj

    def __array_finalize__(self, obj):
        if obj is None: return
        self.scaleinfo = getattr(obj, 'scaleinfo',None)

    def savetxt(self, title):
        """ 
        Save an state data to text file 
        
        Parameters
        ----------
        title: filename
        
        See Also
        ----------
        numpy.savetxt
        """
        ann = self.__annotate()
        abs2 = numpy.abs(self*numpy.conj(self))
        data = numpy.array([self.scaleinfo.x[0], abs2, self.real, self.imag])
        numpy.savetxt(title, data.transpose(), header=ann)
    
    def __annotate(self):
        import datetime
        ann ="DATE: %s\n" % datetime.datetime.now()
        ann += "DIM %d\n" % self.scaleinfo.dim
        ann += "QMIN %s\n" % self.scaleinfo.domain[0][0]
        ann += "QMAX %s\n" % self.scaleinfo.domain[0][1]
        ann += "PMIN %s\n" % self.scaleinfo.domain[1][0]
        ann += "PMAX %s\n" % self.scaleinfo.domain[1][1]
        return ann
    
    def insert(self, i, x=1.0+0.j):
        """
        >>> from state import State, ScaleInfo
        >>> scl = ScaleInfo(10, [[0,1],[-0.5,0.5]])
        >>> state = State(scl)
        >>> state.insert(2,2.0+1.j)
        >>> print(state)
        [ 0.+0.j  0.+0.j  2.+1.j  0.+0.j  0.+0.j  0.+0.j  0.+0.j  0.+0.j  0.+0.j
          0.+0.j]
        """
        if not isinstance(i, int): raise ValueError("excepted: integer")
        self[i] = x

    
    def _cs(self, q_c, p_c, x=None):
        """ 
        minimum-uncertainty Gaussian wave packet centered at (q0,p0)
        周期的境界条件を課してないので特別な理由がない限り使うな．
        Parameters
        ----------
        q_c, p_c : float
            Centroid (q_c,p_c) of wave packet
        x : (optional) array
            if x is None, x is replaced scaleinfo q-direction (self.scaleinfo.x[0])
        """ 
        if x == None:
            x = self.scaleinfo.x[0]
        re = -(x - q_c)*(x - q_c)*numpy.pi/(self.scaleinfo.h)
        im = (x - q_c)*p_c*twopi/self.scaleinfo.h
        res = numpy.exp(re+ 1.j*im)
        norm2 = numpy.abs(numpy.dot(res, numpy.conj(res)))
        return res/numpy.sqrt(norm2)
    
    # todo: like classmethod 

    def cs(self, q_c, p_c):
        """ 
        create new state which 
        minimum-uncertainty Gaussian wave packet centered at (q_c,p_c) on periodic boundary condition.
        
        Parameters
        ----------
        q_c, p_c : float
            Centroid (q_c,p_c) of wave packet
        
        Examples
        ----------
        >>> from state import State, ScaleInfo
        >>> scl = ScaleInfo(10, [[0,1],[-0.5,0.5]])
        >>> state = State(scl)
        >>> state.cs(0.5,0.1)
        State([ -5.19214101e-04 +4.91950621e-47j,
                -3.55650243e-03 -2.58395027e-03j,
                -1.22265106e-02 -3.76293303e-02j,
                 5.88151479e-02 -1.81014412e-01j,
                 3.95164004e-01 -2.87103454e-01j,
                 6.68740103e-01 -8.71513377e-71j,
                 3.95164004e-01 +2.87103454e-01j,
                 5.88151479e-02 +1.81014412e-01j,
                -1.22265106e-02 +3.76293303e-02j,  -3.55650243e-03 +2.58395027e-03j])
        """         
        
        qrange = self.scaleinfo.domain[0]
        d = qrange[1] - qrange[0]
        lqmin, lqmax = qrange[0] - 2*d, qrange[1] + 2*d
        long_q = numpy.linspace(lqmin, lqmax, 5*self.scaleinfo.dim, endpoint=False)
        
        coh_state = self._cs(q_c, p_c, long_q)

        vec = numpy.zeros(self.scaleinfo.dim, dtype=numpy.complex128) 
        m = int(len(coh_state)/self.scaleinfo.dim)
        coh_state = coh_state.reshape(m,self.scaleinfo.dim)
        
        for i in range(m):
            vec += coh_state[i][::1]
        norm2 = numpy.dot(vec, numpy.conj(vec))
        
        return State(self.scaleinfo, vec/numpy.sqrt(norm2))
    
def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _test()