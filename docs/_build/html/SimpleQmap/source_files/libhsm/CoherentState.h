#ifndef COHERENT_STATE
#define COHERENT_STATE

#ifdef __cplusplus
extern "C" {
#endif


#include<math.h>
#include"c_complex.h"

// typedef c_omplex Complex;

c_complex coherent_state(double x, double h, double x_c, double p_c);

#ifdef __cplusplus
}
#endif


#endif
