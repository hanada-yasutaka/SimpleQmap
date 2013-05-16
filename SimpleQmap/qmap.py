#-*- coding:utf-8 -*-
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

class Vector(numpy.ndarray):
    """
    
    Vector はScaleInfoで定義された上でのベクトルを提供します．
    numpy.ndarrayを継承しています．
    
    Parameters
    ----------
    scaleinfo : ScaleInfo instance

    data: (optional) Vector
        if data is None, return a new array of given scaleinfo, filled with zeros.
        if data is not None, return a new array of given data, 
        Note that length data must be same scaleinfo dimnsion.

    Examples
    ----------
    from qmap import Vector, ScaleInfo
    >>> scl = ScaleInfo(10, [[0,1],[-0.5,0.5]])
    >>> vec = Vector(scl)
    >>> print(vec)
    [ 0.+0.j  0.+0.j  0.+0.j  0.+0.j  0.+0.j  0.+0.j  0.+0.j  0.+0.j  0.+0.j
      0.+0.j]
    >>> print(vec.scaleinfo.x[0])
    [ 0.   0.1  0.2  0.3  0.4  0.5  0.6  0.7  0.8  0.9]
    >>> newvec = vec.copy()
    >>> print newvec
    [ 0.+0.j  0.+0.j  0.+0.j  0.+0.j  0.+0.j  0.+0.j  0.+0.j  0.+0.j  0.+0.j
      0.+0.j]
    >>> print(newvec.scaleinfo.h)
    0.1
    >>> newvec[0] = 1.0+0.j
    >>> vec
    Vector([ 0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,
            0.+0.j,  0.+0.j,  0.+0.j])
    >>> newvec
    Vector([ 1.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,
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
    def savetxt(self, title):
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
    
    def one(self, index):
        self[index] = 1.0 + 0.j
        return self 
        
        
class Qmap(object):
    def __init__(self, map, dim, domain):
        #ScaleInfo.__init__(self, dim , domain)
        self.map = map
        self.scaleinfo = ScaleInfo(dim, domain)
        self.dim =self.scaleinfo.dim
        self.setOperate()

        self.stateIn = Vector(self.scaleinfo)
        self.stateOut = Vector(self.scaleinfo)


    def setOperate(self):
        self.operator = [Vector(self.scaleinfo) for i in range(2)]
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
        outvec = numpy.fft.fft(self.operator[0]*self.stateIn)
        self.stateOut = numpy.fft.ifft(self.operator[1]*outvec)
        
    def setInit(self, x):
        if len(x) != self.dim:
            raise ValueError("input velue lentht must be %d" % self.dim)
        self.stateIn = numpy.copy(x)

    def getIn(self):
        return self.stateIn

    def getOut(self):
        return self.stateOut

    def pull(self):
        self.stateIn = numpy.copy(self.stateOut)
    
    def evol(self):
        self.operate()
        self.pull()

    def setMatrix(self):
        self.matrix = numpy.zeros([self.dim, self.dim],dtype=numpy.complex128)

        for i in range(self.dim):
            vec = Vector(self.scaleinfo)
            self.setInit(vec.one(i))
            self.operate()
            self.matrix[i,:] = self.stateOut
        self.matrix = numpy.transpose(self.matrix)

    def eigen(self):
        try:
            evals, evecs = numpy.linalg.eig(self.matrix)
            vecs = [Vector(self.scaleinfo, evec) for evec in evecs.transpose()]
            return evals, vecs 
        except AttributeError:
            self.setMatrix()
            evals, evecs = numpy.linalg.eig(self.matrix)
            vecs = [Vector(self.scaleinfo, evec) for evec in evecs.transpose()]                        
            return evals, vecs
        
    def getMatrix(self):
        try:
            return self.matrix
        except AttributeError:
            self.setMatrix()
            return self.matrix
    def saveMatrix(self,rfname='matrix_real.dat',ifname='matrix_imag.dat'):
        f1 = open(rfname, "w")
        f2 = open(ifname, "w")
        for i in range(self.dim):
            [ f1.write("%.40e " % self.matrix[i,j].real ) for j in range(self.dim) ]
            [ f2.write("%.40e " % self.matrix[i,j].imag ) for j in range(self.dim) ]            
            f1.write("\n")
            f2.write("\n")            
        f1.close()
        f2.close()
        
    
    def saveVector(self,title,vec,eval=None):
        import datetime
        abs2 = numpy.abs(vec*numpy.conj(vec))
        with open(title, "w") as f:
            f.write("# DATE: %s \n" % datetime.datetime.now() )
            f.write("# DIM %d\n" % self.dim)
            f.write("# QMIN %f\n" % self.domain[0][0])
            f.write("# QMAX %f\n" % self.domain[0][1])
            f.write("# PMIN %f\n" % self.domain[1][0])
            f.write("# PMAX %f\n" % self.domain[1][1])
            if eval != None:
                f.write("# EIGEN VALUE REAL %.15e\n" % eval.real)
                f.write("# EIGEN VALUE IMAG %.15e\n" % eval.imag)        
            f.write("# q, abs(evec*conj(evec)), evec.real, evec.imag\n")        
            numpy.savetxt(f,numpy.array([self.x[0], abs2, vec.real, vec.imag]).transpose() )
    
