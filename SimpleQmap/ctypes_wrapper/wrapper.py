import os
import ctypes
import numpy
class call_hsm_rep(object): 
	def __init__(self, path):
		self.c_lib = ctypes.cdll.LoadLibrary(path)  
		
	def husimi_rep(self, vec, dim, domain, hsm_range, hsm_grid):
		terget = numpy.array(vec,dtype=numpy.complex128)
		qmin, qmax = domain[0][0], domain[0][1]
		pmin, pmax = domain[1][0], domain[1][1]
		#dim= dim
		h = (qmax - qmin)*(pmax - pmin)/dim
		vqmin, vqmax = hsm_range[0][0], hsm_range[0][1]
		vpmin, vpmax = hsm_range[1][0], hsm_range[1][1]
		row, col = hsm_grid[0], hsm_grid[1]
		hsm_data = numpy.zeros([row, col], dtype=numpy.float64)
		
		rvec = numpy.copy(vec.real)
		ivec = numpy.copy(vec.imag)
		
		f4ptr = ctypes.POINTER(ctypes.c_double)
		data = (f4ptr*row)(*[ROW.ctypes.data_as(f4ptr) for ROW in hsm_data])
		
		hsm = self.c_lib.wrapper_husimi_rep
		hsm.restype = None
		hsm.argtypes = [ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double),\
                        ctypes.POINTER(ctypes.POINTER(ctypes.c_double)), ctypes.c_int, 
                        ctypes.c_int, ctypes.c_int,\
                        ctypes.c_double, ctypes.c_double,\
                        ctypes.c_double, ctypes.c_double,\
                        ctypes.c_double,\
                        ctypes.c_double, ctypes.c_double,\
                        ctypes.c_double, ctypes.c_double]
		hsm(rvec.ctypes.data_as(ctypes.POINTER(ctypes.c_double)),  \
             ivec.ctypes.data_as(ctypes.POINTER(ctypes.c_double)),  \
             data,\
             len(terget),\
             row, col,\
             qmax, qmin,\
             pmax, pmin,\
             h,\
             vqmax, vqmin,\
             vpmax, vpmin
            )
		hsm_data=numpy.array([data[i][j] for i in range(row) for j in range(col)])
		hsm_imag = hsm_data.reshape(row,col)
#		x = numpy.linspace(vqmin, vqmax, row)
#		y = numpy.linspace(vpmin, vpmax, col)
#		X,Y = numpy.meshgrid(x,y)

		return hsm_imag
