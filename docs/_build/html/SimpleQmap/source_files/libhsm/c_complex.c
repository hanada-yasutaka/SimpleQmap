#include"c_complex.h"


c_complex add_c(c_complex a, c_complex b)
{
  c_complex res;
  
  res.re = a.re + b.re;
  res.im = a.im + b.im;
  
  return res;
}

c_complex sub_c(c_complex a, c_complex b)
{
  c_complex res;

  res.re = a.re - b.re;
  res.im = a.im - b.im;

  return res;


}

c_complex mul_c(c_complex a, c_complex b)
{
  c_complex res;

  res.re = (a.re * b.re) - (a.im * b.im); 
  res.im = (a.re * b.im) + (a.im * b.re);

  return res;  
}


double  abs_c(c_complex a)
{
  double res, tmp;
  double x, y;
  x = fabs(a.re);
  y = fabs(a.im);

  if(x==0){
    res = y;
  }else if(y==0){
    res = x;
  }else if(x>y){
    tmp = y/x;
    res = x*sqrt(1.0 + tmp*tmp);
  } else {
    tmp = x/y;
    res = y*sqrt(1.0 + tmp*tmp);
  }
  return res;
}
  
c_complex conj_c(c_complex z)
{
  c_complex res;
  res.re = z.re;
  res.im = -z.im;
  return res;
}


c_complex cmplx(double r, double i)
{
  c_complex res;

  res.re = r;
  res.im = i;

  return res;
}


c_complex exp_c(c_complex z)
{
  c_complex res;
  double amp;
  double phs;

  amp = exp(z.re);
  phs = z.im;

  res.re = cos(phs);
  res.im = sin(phs);

  res.re *= amp; 
  res.im *= amp;

  return res;
}
