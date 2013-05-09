#ifndef WRAPPER_HUSIMI_REP_H
#define WRAPPER_HUSIMI_REP_H

extern void wrapper_husimi_rep(const double *rvec, const double *ivec,
	double **hsm_imag,
	int hdim,
	int row, int col,
	double qmax, double qmin,
	double pmax, double pmin,
	double h,
	double vqmax, double vqmin,
	double vpmax, double vpmin);

#endif
