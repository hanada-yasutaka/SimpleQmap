# -*- coding:utf-8 -*-
"""
state.py

author: Yasutaka Hanada (2013/05/17)

Domain Setting and Quantum states.


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
    
    State はScaleInfoで定義された上で波動関数 :math:`| \psi\\rangle` を提供します．
    表示は :math:`q-` 表示，すなわち :math:`\\langle q | \\psi\\rangle` を採用し，
    各種変換を定義しています．
    numpy.ndarrayを継承しています．
        
    
    Parameters
    ----------
    scaleinfo : ScaleInfo instance
                input scaleinfo instance
    data     : State, optional
                 if data is None, return a new array of given scaleinfo, filled with zeros.
                 if data is not None, return a new array of given data, 
                 Note that length data must be same scaleinfo dimnsion.
    
    See Also
    --------
    numpy.ndarray : subclassing ndarray <http://docs.scipy.org/doc/numpy/user/basics.subclassing.html>
    
    
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

    def savetxt(self, filename):
        """ 
        Save an state data to text file 
        
        Parameters
        ----------
        filename: file name
        
        See Also
        ----------
        numpy.savetxt <http://docs.scipy.org/doc/numpy/reference/generated/numpy.savetxt.html>

        """
        ann = self.__annotate()
        abs2 = numpy.abs(self*numpy.conj(self))
        data = numpy.array([self.scaleinfo.x[0], abs2, self.real, self.imag])
        numpy.savetxt(filename, data.transpose(), header=ann)
    
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

    
    def coherent(self, q_c, p_c, x=None):
        """ 
        
        minimum-uncertainty Gaussian wave packet centered at (q_c,p_c)
        
        .. math:: 
        
            \langle q | \psi \\rangle = \exp[-(q-q_c)^2/2\hbar + p_c(q-q_c)/\hbar]
            
        .. warning::
        
        	周期的境界条件を課してないので特別な理由がない限り使わないで下さい．
        
        Parameters
        ----------
        
        q_c, p_c : float
            Centroid (q_c,p_c) of the wave packet
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
                
        .. seealso:: 
        
            Module :state:`coherent`
        
        """         
        
        qrange = self.scaleinfo.domain[0]
        d = qrange[1] - qrange[0]
        lqmin, lqmax = qrange[0] - 2*d, qrange[1] + 2*d
        long_q = numpy.linspace(lqmin, lqmax, 5*self.scaleinfo.dim, endpoint=False)
        
        coh_state = self.coherent(q_c, p_c, long_q)

        vec = numpy.zeros(self.scaleinfo.dim, dtype=numpy.complex128) 
        m = int(len(coh_state)/self.scaleinfo.dim)
        coh_state = coh_state.reshape(m,self.scaleinfo.dim)
        
        for i in range(m):
            vec += coh_state[i][::1]
        norm2 = numpy.dot(vec, numpy.conj(vec))
        
        return State(self.scaleinfo, vec/numpy.sqrt(norm2))
        
    def qrep(self):
    	"""
    	return :math:`\\langle q | \\psi\\rangle`
    	"""
    	return State(self.scaleinfo, self)
    	
    def prep(self):
    	"""
    	return :math:`\\langle p | \\psi\\rangle`
    	"""    
        return State(self.scaleinfo, self.q2p())
        

    def p2q(self):
    	"""
    	Fourier (inverse) transformation from
    	the momentum :math:`(p)` representation to the position :math:`(q)` representation.

    	.. math::
    	
    		\\langle q | \\psi\\rangle = \\sum_p \\langle q | p\\rangle \\!\\langle p | \\psi \\rangle

    	"""    
    
        data = State(self.scaleinfo, self)
        if self.scaleinfo.domain[1][0]*self.scaleinfo.domain[1][1] < 0:
            data = numpy.fft.fftshift(data)        
        data = numpy.fft.ifft(data)*numpy.sqrt(self.scaleinfo.dim)#/numpy.sqrt(self.scaleinfo.dim)        
        return State(self.scaleinfo, data)
    
    def q2p(self):
    	"""
    	Fourier (forward) transformation from
    	the position :math:`(q)` representation to the momentum :math:`(p)` representation. 
    	
    	.. math::
    	
            \\langle p | \\psi\\rangle = \\sum_q \\langle p | q\\rangle \\!\\langle q | \\psi \\rangle
    	
    	"""
        data = numpy.fft.fft(self)/numpy.sqrt(self.scaleinfo.dim)
        if self.scaleinfo.domain[1][0]*self.scaleinfo.domain[1][1] < 0:
            data = numpy.fft.fftshift(data)
        return State(self.scaleinfo, data) #*numpy.sqrt(self.scaleinfo.dim)
    	
    def hsmrep(self, col, row, region=None):
    	"""
    	Husimi (phase space) representation.

        Parameter
        ----------
        col, row: int
            mesh grid 
        region: 2 by 2 list
            Husimi plot range. expected 2 by 2 list, e.g., [[qmin,qmax], [pmin, pmax]]
    	    
    	.. todo::
    		
            未デバッグ
		
    	"""

        if region==None:
            region = self.scaleinfo.domain
        else:
            region = hsm_region
        from ctypes_wrapper import wrapper
        import os
        path = os.environ['PYTHONPATH'].split(":")
        index = [p.endswith('SimpleQmap') for p in path].index(True)
        file_path = path[index] + '/SimpleQmap/shared/libhsm.so'

        cw = wrapper.call_hsm_rep(file_path)
        hsm_imag = cw.husimi_rep(self, self.scaleinfo.dim, self.scaleinfo.domain, region, [row,col])

        x = numpy.linspace(region[0][0], region[0][1], row)
        y = numpy.linspace(region[1][0], region[1][1], col)

        X,Y = numpy.meshgrid(x,y)
        return X,Y,hsm_imag    	
    	
    	
    def abs2(self):
    	"""
    	return :math:`|\\langle x | \\psi \\rangle|^2` where :math:`x` is :math:`q` or :math:`p` 
    	"""
    	data = self*numpy.conj(self)
    	return numpy.abs(data)
    def norm(self):
    	norm = numpy.abs(numpy.sum(self*numpy.conj(self)))
    	return norm
    
def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _test()
