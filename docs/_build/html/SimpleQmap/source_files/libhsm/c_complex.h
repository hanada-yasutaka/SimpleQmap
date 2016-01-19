#ifndef c_complex_H
#define c_complex_H

#ifdef __cplusplus
extern "C" {
#endif

#include<math.h>

  /// FFTW(ver2) $B$N(B fftw_complex $B$H8_49$9$k$h$&$K(B//
  typedef struct {
    double re;
    double im;
  } c_complex;
  
  c_complex add_c(c_complex a, c_complex b);
  c_complex sub_c(c_complex a, c_complex b);
  c_complex mul_c(c_complex a, c_complex b);
  
  double abs_c(c_complex a);
  c_complex conj_c(c_complex z);
  c_complex cmplx(double r, double i);
  
  c_complex exp_c(c_complex z);
#ifdef __cplusplus
}
#endif

#endif
