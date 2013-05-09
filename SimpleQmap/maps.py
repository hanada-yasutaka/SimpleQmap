import numpy
twopi=2.0*numpy.pi

class StandardMap(object):
    def __init__(self, k):
        self.k = k
    def func0(self, x):
        return self.k*numpy.sin(twopi*x)/twopi
        
    def func1(self, x):
        return x
        
    def ifunc0(self, x):
        return -self.k*numpy.cos(twopi*x)/(twopi*twopi)
        
    def ifunc1(self, x):
        return 0.5*x*x
        