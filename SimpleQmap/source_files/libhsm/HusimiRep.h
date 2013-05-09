#ifndef HUSIMI_REP
#define HUSIMI_REP

#ifdef __cplusplus
extern "C" {
#endif
#include<stdio.h>
#include<math.h>
#include"c_complex.h"


  void husimi_rep(const c_complex *trgt_data,
		  double **res_data,
		  int hdim,
		  int row,  int col,
		  double xmax,  double xmin,
		  double pmax,  double pmin,
		  double h,
		  double view_xmax,  double view_xmin,
		  double view_pmax,  double view_pmin);
  
  void out_husimi_data(FILE *of, double **data,
		       int row, int col,
		       double vxmax, double vxmin,
		       double vpmax, double vpmin);

#ifdef __cplusplus
}
#endif


#endif
