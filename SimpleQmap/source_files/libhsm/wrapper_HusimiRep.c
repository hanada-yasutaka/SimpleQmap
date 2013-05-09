#include <stdio.h>
#include <stdlib.h>
#include "HusimiRep.h"
#include "wrapper_husimi_rep.h"
typedef c_complex Complex;

void wrapper_husimi_rep(const double *rvec, const double *ivec,
			double **hsm_imag,
			int hdim,
			int row, int col,
			double qmax, double qmin,
			double pmax, double pmin,
			double h,
			double vqmax, double vqmin,
			double vpmax, double vpmin)
{
  int i;
  Complex *terget_vec = (Complex *)malloc(hdim*sizeof(Complex));
  
  for(i=0;i<hdim;i++){
    terget_vec[i].re = rvec[i];
    terget_vec[i].im = ivec[i];
  }

  husimi_rep(terget_vec, hsm_imag, hdim,
	     row, col,
	     qmax, qmin,
	     pmax, pmin,
	     h,
	     vqmax, vqmin,
	     vpmax, vpmin);

}
