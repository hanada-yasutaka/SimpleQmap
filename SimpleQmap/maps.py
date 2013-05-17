# -*- coding:utf-8 -*-
"""
maps.py

author: Yasutaka Hanada (2013/05/17)

Difinition of systems

系はハミルトニアン
    .. math::
        
        H(q,p) = T(p) + V(q)
        
で定義可能とします．

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
            
            H(q,p) = ¥frac{p^2}{2} + ¥frac{k}{2¥pi}*cos(2¥pi q) 
            
    
    Parameters
    ----------
    k : float
        non-linear paramter
    """
    def __init__(self, k):
        self.k = k

    def func0(self, x):
        """
        return - dV(q)/dq
        
        Parameters
        ---------
            x: array like (can be complex)
        
        Returns
        ---------
            out: array like
        """
        return -self.k*numpy.sin(twopi*x)/twopi
        
    def func1(self, x):
        """
        return dT(p)/dp
                
        Parameters
        ---------
            x: array like (can be complex)
        
        Returns
        ---------
            out: array like
        """
        
        return x
        
    def ifunc0(self, x):
        """
        return V(q)
                
        Parameters
        ---------
            x: array like (can be complex)
        
        Returns
        ---------
            out: array like
        """
        
        
        return self.k*numpy.cos(twopi*x)/(twopi*twopi)
        
    def ifunc1(self, x):
        """
        return T(p)
                
        Parameters
        ---------
            x: array like (can be complex)
        
        Returns
        ---------
            out: array like
        """
        
        return 0.5*x*x
        