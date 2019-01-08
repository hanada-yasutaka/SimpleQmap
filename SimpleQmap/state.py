# -*- coding:utf-8 -*-
"""
state.py

author: Yasutaka Hanada (2013/05/17)

Domain Setting and Quantum states.


"""

import numpy
twopi = 2.0*numpy.pi


def loadtxt(fname,verbose=True):
    """
    Load data from a text file.
    
    The file must be saved by savetxt method of State instance. 
    
    Parameter
    ----------
    
    fname : str
        File name
    verbose : bool (optional)
        If true, print the parameters of the loaded file
        
    Returns
    -------
    out : State
        Data read from the text file.
    """
    import re
    from SimpleQmap import State,ScaleInfo
    with open(fname, "r") as file:
        for i, line in enumerate(file):
            if re.search('DIM', line):
                dim = int(line.split(" ")[2])        
            if re.search('QMIN', line):
                qmin = float(line.split(" ")[2])
            if re.search('QMAX', line):
                qmax = float(line.split(" ")[2])
            if re.search('PMIN', line):
                pmin = float(line.split(" ")[2])                
            if re.search('PMAX', line):
                pmax = float(line.split(" ")[2])
            if re.search('REP', line):
                rep = line.split(" ")[2].replace("\n","")

    if rep not in ["q","p"]:
        raise TypeError("must be q-rep or p-rep text file")
    
    data = numpy.loadtxt(title).transpose()
    vec = data[2] + 1.j*data[3]
    scl = ScaleInfo(dim, [[qmin,qmax], [pmin, pmax]])
    state = State(scl, vec)
    if rep == "p":
        state = state.p2q()
    if verbose:
        t = "load:%s\n" % title
        t += "dim:%d\n" % dim
        t += "domain:[%f,%f]x[%f,%f]\n" % (qmin,qmax, pmin, pmax)
        t += "representation:q" if rep =="q" else "!!Warning!!\nconvert original data (p-rep.) to q-rep.\n"
        print(t)
    return state

class HilbertSpace(object):
    def __init__(self, dim, domain):
        """
        Base class for state class 
        
        Parameters
        ----------
        dim : positive int
            Hilbert dimension
        domain : 2x2 list such as [[qmin, qmax], [pmin,pmax]]
            qmin, qmax: domain of q-direction
            pmin, pmax: domain of p-direction
        
        >>> H = HilbertSpace(10, [[0,1],[0,1]] )
        >>> H.dim
        10
        >>> H.h
        0.1
        >>> H.hbar
        0.015915494309189534
        >>> H.x
        [array([ 0. ,  0.1,  0.2,  0.3,  0.4,  0.5,  0.6,  0.7,  0.8,  0.9]), array([ 0. ,  0.1,  0.2,  0.3,  0.4,  0.5,  0.6,  0.7,  0.8,  0.9])]
        
        """
        
        self.dim = self._setDim(dim)
        self.domain = self._setDomain(domain)
        self.h = self._setPlanck()
        self.hbar = self.h/twopi
        self.x = [numpy.linspace(self.domain[0][0], self.domain[0][1], self.dim, endpoint=False),
                  numpy.linspace(self.domain[1][0], self.domain[1][1], self.dim, endpoint=False)]

    def _setDim(self, dim):
        if (dim <= 0) or not isinstance(dim, int):
            raise AttributeError("Hilbert dimension must be positive integer")
        return dim
        
    def _setDomain(self, domain):
        qr, pr  = domain[0], domain[1]

        if (qr[0] >= qr[1]):
            raise AttributeError("qmin > qmax (%f,%f)" % (qr[0],qr[1]))
        if (pr[0] >= pr[1]):
            raise AttributeError("pmin > pmax (%f,%f)" % (pr[0],pr[1]))
        return domain
        
    def _setPlanck(self):
        qr, pr = self.domain
        return (pr[1] - pr[0])*(qr[1] - qr[0])/self.dim


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
        return self.xs 

class state(numpy.ndarray, HilbertSpace):
    """
    State is a vector defined on Hilbert Space
    """
    def __init__(self, input, domain, rep="q"):
        if hasattr(input, "__iter__"): 
            HilbertSpace.__init__(self, len(input), domain)
        elif isinstance(input,int):
            HilbertSpace.__init__(self, input, domain)
        else:
            raise TypeError("cannot create state from %s" % input)
        self.rep = rep
        self._shift = self._Shift()
    """
    Create new state
    
    Parameters
    -----------
    input : array like or int
        shape of numpy array, e.g, [1,2,3] or 10

    domain: 2x2 list such as [[qmin, qmax], [pmin,pmax]]
        qmin, qmax: domain of q-direction
        pmin, pmax: domain of p-direction
    
    rep : 'q' or 'p', (optional)
        representation of state, defalt 'p'
    
    Retern:
    ----------
    out : state
        a state object inherited numpy ndarray
        
    >>> state(10,[[0,1],[0,1]])
    state([ 0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,
            0.+0.j,  0.+0.j,  0.+0.j])
    >>> state([1,2,3,4,5],[[0,1],[0,1]])
    state([ 1.+0.j,  2.+0.j,  3.+0.j,  4.+0.j,  5.+0.j])
    >>> state.rep
    q
    
    Graphic illustration:
    
    """
        
    def __new__(cls, input=[], domain=None,rep="q"):
        if hasattr(input, "__iter__"): 
            return numpy.asarray(input,dtype=complex).view(cls)
        elif isinstance(input,int):
            return numpy.asarray(numpy.zeros(input, dtype=complex)).view(cls)

    def __array_finalize__(self, obj):
        if obj is None: return
        
    def _Shift(self):
        ps = self.domain[1][0]*self.domain[1][1]<0
        qs = self.domain[0][0]*self.domain[0][1]<0
        if self.rep == "q" and not ps and not qs:
            shift = [False, False]
        elif self.rep == "p" and not ps and not qs:
            shift = [False, False]
            
        elif self.rep == "q" and ps and not qs:
            shift = [False, True]
        elif self.rep == "p" and ps and not qs:
            shift = [True, False]
            
        elif self.rep == "q" and not ps and qs:
            shift = [True, False]
        elif self.rep == "p" and not ps and qs:
            shift = [False, True]

        elif self.rep == "q" and ps and qs:
            shift = [True,True]
        elif self.rep == "p" and ps and qs:
            shift = [True, True]

        return shift
    
    def __annotate(self,rep):
        import datetime
        ann ="DATE: %s\n" % datetime.datetime.now()
        ann += "DIM %d\n" % self.scaleinfo.dim
        ann += "QMIN %s\n" % self.scaleinfo.domain[0][0]
        ann += "QMAX %s\n" % self.scaleinfo.domain[0][1]
        ann += "PMIN %s\n" % self.scaleinfo.domain[1][0]
        ann += "PMAX %s\n" % self.scaleinfo.domain[1][1]
        ann += "PMAX %s\n" % self.scaleinfo.domain[1][1]
        ann += "REP %s" % rep
        return ann
    
    def savetxt(self, filename, rep='q',**kwargs):
        """ 
        Save an state data to a text file 
        
        Parameters
        ----------
        filename: str
            file name
        rep: str 
            'q', 'p' or 'hsm'
        
        See Also
        ----------
        numpy.savetxt <http://docs.scipy.org/doc/numpy/reference/generated/numpy.savetxt.html>
        """
        ann = self.__annotate(rep)            
#        abs2 = numpy.abs(self*numpy.conj(self))
        if rep in ["q", "p"]:
            x = self.scaleinfo.x[0] if rep == "q" else self.scaleinfo.x[1]
            state = self if rep == "q" else self.q2p()
            abs2 = state.abs2()
            data = numpy.array([x, abs2, state.real, state.imag])
            numpy.savetxt(filename, data.transpose(), header=ann)
        elif rep == "hsm":
            x,y,z = self.hsmrep(**kwargs)
            data = numpy.array([x,y,z])
            with open(filename, "bw") as of:
                for slice_data in data.T:
                    numpy.savetxt(of, slice_data)
                    of.write(b"\n")
        else:
            raise TypeError('rep is "p", "q" or "hsm"')

    def coherent(self, q_c, p_c, x):
        """ 
        
        minimum-uncertainty Gaussian wave packet centered at (q_c,p_c, x)
        
        .. math:: 
        
            \langle x | \psi \\rangle = \exp[-(x-q_c)^2/2\hbar + p_c(x-q_c)/\hbar]
            
        .. warning::
        
            周期的境界条件を課してないので特別な理由がない限り使わないで下さい．
        
        Parameters
        ----------
        
        q_c, p_c : float
            Centroid (q_c,p_c,x) of the wave packet
        x : array
        """ 
        
        re = -(x - q_c)*(x - q_c)*numpy.pi/(self.h)
        im = (x - q_c)*p_c*twopi/self.h
        res = state(numpy.exp(re+ 1.j*im), self.domain)
        norm2 = numpy.abs(res.inner(res)) 
        return res/numpy.sqrt(norm2)

    def cs(self, q_c, p_c, rep = None):
        """ 
        create new State object which 
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
        if rep is None:
            rep = self.rep
        qrange = self.domain[0]
        d = qrange[1] - qrange[0]
        lqmin, lqmax = qrange[0] - 2*d, qrange[1] + 2*d
        long_q = numpy.linspace(lqmin, lqmax, 5*self.dim, endpoint=False)
        
        coh_state = self.coherent(q_c, p_c, long_q)

        vec = numpy.zeros(self.dim, dtype=numpy.complex128) 
        m = int(len(coh_state)/self.dim)
        coh_state = coh_state.reshape(m,self.dim)
        
        for i in range(m):
            vec += coh_state[i][::1]
        norm2 = numpy.dot(vec, numpy.conj(vec))
        
        vec = state(vec/numpy.sqrt(norm2), self.domain, rep)
        if rep == "p":
            vec = state(vec.q2p(), self.domain, rep)
        return vec 
        
    def qrep(self):
        """
        return :math:`\\langle q | \\psi\\rangle` as a State object
        """
        return self.copy() if self.rep == "q" else self.p2q()
        
    def prep(self):
        """
        return :math:`\\langle p | \\psi\\rangle` as a State object
        """
        return self.copy() if self.rep == "p" else self.q2p()
        
    def p2q(self):
        """
        Fourier (inverse) transformation from
        the momentum :math:`(p)` representation to the position :math:`(q)` representation.
        
        .. math::
        
            \\langle q | \\psi\\rangle = \\sum_p \\langle q | p\\rangle \\!\\langle p | \\psi \\rangle
            
        """
        
        data = state(self,self.domain)
        if self._shift[0]:
            data = numpy.fft.fftshift(data)        
        data = numpy.fft.ifft(data)*numpy.sqrt(self.dim)
        return state(data, self.domain)
    
        
    def q2p(self):
        """
        Fourier (forward) transformation from
        the position :math:`(q)` representation to the momentum :math:`(p)` representation. 
        
        .. math::
        
            \\langle p | \\psi\\rangle = \\sum_q \\langle p | q\\rangle \\!\\langle q | \\psi \\rangle
            
        """
        data = numpy.fft.fft(self)/numpy.sqrt(self.dim)
        if self._shift[1]:
           data = numpy.fft.fftshift(data)
        return state(data, self.domain)
        
    def hsmrep(self, grid=[50,50], vrange=None):
        """
        
        Husimi (phase space) representation.
        
        Parameter
        ----------
        col, row: int
            mesh grid of husimi rep.
        region: 2 by 2 list
            Husimi plot range. expected 2 by 2 list, e.g., [[qmin,qmax], [pmin, pmax]]
        """
        if vrange==None:
            vrange = self.domain
        import SimpleQmap
        from SimpleQmap.ctypes_wrapper import wrapper
        import os, glob
        
        for path in glob.glob(SimpleQmap.__path__[0] + "/shared/libhsm*.so"):
            if os.path.exists(path):
                break
        try:
            cw = wrapper.call_hsm_rep(path)
        except NameError:
            raise RuntimeError("libhsm.so not found.")
        data = self.qrep() if self.rep == "q" else self.p2q()

        hsm_imag = cw.husimi_rep(data, self.dim, self.domain, vrange, grid)

        x = numpy.linspace(vrange[0][0], vrange[0][1], grid[0])
        y = numpy.linspace(vrange[1][0], vrange[1][1], grid[1])

        X,Y = numpy.meshgrid(x,y)
        return X,Y,hsm_imag        
        
    def abs2(self):
        """
        return :math:`|\\langle x | \\psi \\rangle|^2` where :math:`x` is :math:`q` or :math:`p` as numpy.array object
        """
        data = self*numpy.conj(self)
        return numpy.array(numpy.abs(data))

    def norm(self):
        """
        return :math:`\\sum_x |\\langle x | \\psi \\rangle|^2` where 
        :math:`x` is :math:`q` or :math:`p` as real value constant (numpy.float64)
        """
        norm = numpy.abs(numpy.sum(self*numpy.conj(self)))
        return numpy.float64(norm)

    def inner(self, phi):
        """
        return :math:`\\langle \\phi | \\psi\\rangle` as complex value constant (numpy.complex128)
        """
        res = numpy.sum(self*numpy.conj(phi))
        return numpy.complex128(res)
    
    def copy(self):
        return state(self.toarray(), self.domain)
    
    def toarray(self):
        return numpy.array(self.tolist())


class State(numpy.ndarray):
    """
    State is a vector defined on Hilbert space.
        
    
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
        if data is None:
            data = numpy.zeros(scaleinfo.dim)
        obj = numpy.asarray(data, dtype=numpy.complex128).view(cls)
        obj.scaleinfo = scaleinfo
        obj.x = scaleinfo.x
        return obj

    def __array_finalize__(self, obj):
        if obj is None: return
        self.scaleinfo = getattr(obj, 'scaleinfo',None)

    def savetxt(self, filename, rep='q',**kwargs):
        """ 
        Save an state data to a text file 
        
        Parameters
        ----------
        filename: str
            file name
        rep: str 
            'q', 'p' or 'hsm'
        
        See Also
        ----------
        numpy.savetxt <http://docs.scipy.org/doc/numpy/reference/generated/numpy.savetxt.html>
        """
        ann = self.__annotate(rep)            
#        abs2 = numpy.abs(self*numpy.conj(self))
        if rep in ["q", "p"]:
            x = self.scaleinfo.x[0] if rep == "q" else self.scaleinfo.x[1]
            state = self if rep == "q" else self.q2p()
            abs2 = state.abs2()
            data = numpy.array([x, abs2, state.real, state.imag])
            numpy.savetxt(filename, data.transpose(), header=ann)
        elif rep == "hsm":
            x,y,z = self.hsmrep(**kwargs)
            data = numpy.array([x,y,z])
            with open(filename, "bw") as of:
                for slice_data in data.T:
                    numpy.savetxt(of, slice_data)
                    of.write(b"\n")
        else:
            raise TypeError('rep is "p", "q" or "hsm"')

    
    def __annotate(self,rep):
        import datetime
        ann ="DATE: %s\n" % datetime.datetime.now()
        ann += "DIM %d\n" % self.scaleinfo.dim
        ann += "QMIN %s\n" % self.scaleinfo.domain[0][0]
        ann += "QMAX %s\n" % self.scaleinfo.domain[0][1]
        ann += "PMIN %s\n" % self.scaleinfo.domain[1][0]
        ann += "PMAX %s\n" % self.scaleinfo.domain[1][1]
        ann += "PMAX %s\n" % self.scaleinfo.domain[1][1]
        ann += "REP %s" % rep
        return ann
    
    def insert(self, i, x):
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
    
    def coherent(self, q_c, p_c, x):
        """ 
        
        minimum-uncertainty Gaussian wave packet centered at (q_c,p_c, x)
        
        .. math:: 
        
            \langle x | \psi \\rangle = \exp[-(x-q_c)^2/2\hbar + p_c(x-q_c)/\hbar]
            
        .. warning::
        
            周期的境界条件を課してないので特別な理由がない限り使わないで下さい．
        
        Parameters
        ----------
        
        q_c, p_c : float
            Centroid (q_c,p_c,x) of the wave packet
        x : array
        """ 
        
        re = -(x - q_c)*(x - q_c)*numpy.pi/(self.scaleinfo.h)
        im = (x - q_c)*p_c*twopi/self.scaleinfo.h
        res = State(self.scaleinfo, data = numpy.exp(re+ 1.j*im))
        norm2 = numpy.abs(res.inner(res)) 
        return res/numpy.sqrt(norm2)

    def cs(self, q_c, p_c):
        """ 
        create new State object which 
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
        return :math:`\\langle q | \\psi\\rangle` as a State object
        """
        return State(self.scaleinfo, self)
        
    def prep(self):
        """
        return :math:`\\langle p | \\psi\\rangle` as a State object
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
        
    def hsmrep(self, col=50, row=50, region=None):
        """
        
        Husimi (phase space) representation.
        
        Parameter
        ----------
        col, row: int
            mesh grid of husimi rep.
        region: 2 by 2 list
            Husimi plot range. expected 2 by 2 list, e.g., [[qmin,qmax], [pmin, pmax]]
        """
        if region==None:
            region = self.scaleinfo.domain
        #else:
        #    region = hsm_region
        import SimpleQmap
        from SimpleQmap.ctypes_wrapper import wrapper
        import os, glob
        #path = os.environ['PYTHONPATH'].split(":")
        
        for path in glob.glob(SimpleQmap.__path__[0] + "/shared/libhsm*.so"):
            if os.path.exists(path):
                break
        try:
            cw = wrapper.call_hsm_rep(path)
        except NameError:
            raise RuntimeError("libhsm.so not found.")
            
        hsm_imag = cw.husimi_rep(self, self.scaleinfo.dim, self.scaleinfo.domain, region, [row,col])

        x = numpy.linspace(region[0][0], region[0][1], row)
        y = numpy.linspace(region[1][0], region[1][1], col)

        X,Y = numpy.meshgrid(x,y)
        return X,Y,hsm_imag    	
        
        
    def abs2(self):
        """
        return :math:`|\\langle x | \\psi \\rangle|^2` where :math:`x` is :math:`q` or :math:`p` as numpy.array object
        """
        data = self*numpy.conj(self)
        return numpy.array(numpy.abs(data))

    def norm(self):
        """
        return :math:`\\sum_x |\\langle x | \\psi \\rangle|^2` where 
        :math:`x` is :math:`q` or :math:`p` as real value constant (numpy.float64)
        """
        norm = numpy.abs(numpy.sum(self*numpy.conj(self)))
        return numpy.float64(norm)

    def inner(self, phi):
        """
        return :math:`\\langle \\phi | \\psi\\rangle` as complex value constant (numpy.complex128)
        """
        res = numpy.sum(self*numpy.conj(phi))
        return numpy.complex128(res)
    
    def copy(self):
        return State(self.scaleinfo, self.toarray())
    
    def toarray(self):
        return numpy.array(self.tolist())
    
if __name__ == "__main__":
    import doctest
    doctest.testmod()
