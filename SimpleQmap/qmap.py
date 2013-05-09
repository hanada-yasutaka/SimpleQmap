import numpy
twopi= 2.0*numpy.pi


        
class Qmap(object):
    def __init__(self, map, dim,domain):
        self.map = map
        self.dim = dim

        self.stateIn = numpy.zeros(self.dim, dtype=numpy.complex128)
        self.stateOut = numpy.zeros(self.dim, dtype=numpy.complex128)        
        self.operator = [numpy.zeros(self.dim, dtype=numpy.complex128) for i in range(2)]
        self.setDomain(domain)
        
    def setDomain(self, domain):
            
        self.domain = domain
        self.x = [numpy.linspace(self.domain[i][0], self.domain[i][1], self.dim, endpoint=False) for i in range(2)]
        self.h = self.getPlanck()
        self.op0(self.x[0])
        if (domain[1][0] == 0.0):
            self.op1(self.x[1])
        elif (numpy.abs(domain[1][0]) == numpy.abs(domain[1][1])):
            self.op1(numpy.fft.fftshift(self.x[1]))
        else:
            raise ValueError("unexpected domain.")
    
    def getPlanck(self):
        W = (self.domain[0][1] -self.domain[0][0])*(self.domain[1][1] - self.domain[1][0])
        return W/self.dim
        
    def op0(self,x):
        self.operator[0] = numpy.exp(-1.j*twopi*self.map.ifunc0(x)/self.h)
    
    def op1(self,x):
        self.operator[1] = numpy.exp(-1.j*twopi*self.map.ifunc1(x)/self.h)
        
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
            orth_basis = numpy.zeros(self.dim,dtype=numpy.complex128)
            orth_basis[i] = 1.0+0.j
            self.setInit(orth_basis)
            self.operate()
            self.matrix[i,:] = self.stateOut
        self.matrix = numpy.transpose(self.matrix)


    def eigen(self):
        try:
            evals, evecs = numpy.linalg.eig(self.matrix)
            return evals, evecs.transpose()
        except AttributeError:
            self.setMatrix()
            evals, evecs = numpy.linalg.eig(self.matrix)
            return evals, evecs.transpose()
    def getX(self):
        return self.x
        
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
    
