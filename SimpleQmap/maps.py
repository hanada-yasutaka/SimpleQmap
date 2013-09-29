# -*- coding:utf-8 -*-
"""
maps.py

author: Yasutaka Hanada (2013/05/17)


系はkicked rotator
    
.. math::
        
    H(q,p) = T(p) + V(q)\sum_{n\in\mathbb{Z}}\delta(t-n)
        
で定義します．

"""

import numpy
twopi=2.0*numpy.pi

class Symplectic(object):
    pass
        
class StandardMap(Symplectic):
    """ 
    標準写像
    
    Hamiltonian
    
    .. math::
            
        T(p) = \\frac{p^2}{2},\qquad \\frac{k}{4\pi^2}\cos(2\pi q) 
            

    
    .. figure:: ./imag/std.png
       :scale: 50%

    Phase space portrait of Standard Map with :math:`k = 1`
    
    Parameters
    ----------
    k : float
        paramter
    
    
    """
    def __init__(self, k):
        self.k = k

    def func0(self, x):
        """
        return :math:`dV(q)/dq = k\sin(2\pi q)/2\pi`
        
        Parameters
        ---------
            x: array like
        
        Returns
        ---------
            out: array like
        """
        return -self.k*numpy.sin(twopi*x)/twopi
        
    def func1(self, x):
        """
        return :math:`dT(p)/dp = p`
                
        Parameters
        ---------
            x: array like
        
        Returns
        ---------
            out: array like
        """
        
        return x
        
    def ifunc0(self, x):
        """
        return :math:`V(q)`
                
        Parameters
        ---------
            x: array like
        
        Returns
        ---------
            out: array like
        """
        
        
        return self.k*numpy.cos(twopi*x)/(twopi*twopi)
        
    def ifunc1(self, x):
        """
        return :math:`T(p)`
                
        Parameters
        ---------
            x: array like
        
        Returns
        ---------
            out: array like
        """
        
        return 0.5*x*x
        