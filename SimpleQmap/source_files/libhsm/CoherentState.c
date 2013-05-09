#include"CoherentState.h"
#include<stdio.h>

c_complex
coherent_state(double x_in, double h, double x_c, double p_c)
{
  c_complex res;

  double x;
  c_complex z, zz;
  c_complex tmp;

  x = x_in/sqrt(h/(2*M_PI));
  z.re = x_c/sqrt(h/M_PI);
  z.im = p_c/sqrt(h/M_PI);
  zz = mul_c(z,z);

  tmp.re = -abs_c(z)*abs_c(z)/2.0 - (x*x + zz.re)/2.0 + sqrt(2.0)*x*z.re;
  tmp.im =                               - zz.im /2.0 + sqrt(2.0)*x*z.im;

  res = exp_c(tmp);
  res.re *= sqrt(sqrt(2.0/h));
  res.im *= sqrt(sqrt(2.0/h));
  return res;
}

