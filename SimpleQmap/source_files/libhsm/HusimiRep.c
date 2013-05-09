#include<stdio.h>
#include<stdlib.h>
#include<assert.h>
#include"HusimiRep.h"
#include"CoherentState.h"


typedef c_complex Complex;

static void fill_cvec(int vsize, Complex *in_vec, Complex c);
static void  set_result(double **res_data,  double w, int i, int j);
static void  get_cs_vec(int vsize, Complex *cs,
		double cs_x, double cs_p,
		double dx, double xmin, double h);
//static void  normalize(double **res_data, int row, int col);
static double get_weight(int vsize,
			 const Complex *trgt_vec,
			 const Complex *cs_vec);
//static void  out_cs_vec(int size, Complex *cs); // debug用 //
//static void  dump_args(int N, const Complex *target); // debug 用 //


void test(void)
{
  printf("welcom to husimiRep.c\n");
}

void husimi_rep(const Complex *trgt_vec,
		double **res_data,
		int hdim,
		int row,  int col,
		double xmax,  double xmin,
		double pmax,  double pmin,
		double h,
		double xe,  double xs,
		double pe,  double ps)
     
{
  double weight;
  const double cs_dx = (xe - xs)/col;
  const double cs_dp = (pe - ps)/row;

  const double dx = (xmax - xmin)/hdim;

  double cs_x;
  double cs_p;
  Complex *cs_vec = (Complex *) malloc(hdim * sizeof(Complex));
  assert(cs_vec);

  int i, j;
  for( i=0; i!=row; i++){
    for( j=0; j!=col; j++){
      cs_x = xs + j*cs_dx;
      cs_p = ps + i*cs_dp;
      get_cs_vec(hdim, cs_vec, cs_x, cs_p, dx, xmin, h);
      weight = get_weight(hdim, trgt_vec, cs_vec); // | < trgt | cs > |^2
      set_result(res_data, weight, i, j);
    }
  }

  //  normalize(res_data, row, col);
  free(cs_vec);
}


void out_husimi_data(FILE *of, double **data,
		 int row, int col,
		 double xmax, double xmin,
		 double pmax, double pmin)
{
  int res;
  int ix, ip;
  double x, p;
  double dx = (xmax-xmin)/col;
  double dp = (pmax-pmin)/row;
  for(ip=0; ip!=row; ip++){
    p = pmin + ip * dp;
    for(ix=0; ix!=col; ix++){
      x = xmin + ix *dx;
      res = fprintf(of,"%lf %lf %lf\n",x, p, data[ip][ix]);
      assert(res>=0);
    }
    fprintf(of,"\ne\n");
  }
//  fprintf(stderr, "%d, %d\n", ix, ip);
    
}





//------------------ static --------------------------------------------//


static void 
fill_cvec(int vsize, Complex *in_vec, Complex c)

{
  int i;
  for( i=0; i!=vsize; i++){
    in_vec[i] = c;
  }

}


static void 
get_cs_vec(int vsize, Complex *cs_vec,
	   double cs_x, double cs_p,
	   double dx, double xmin, double h)
{
  int i;
  const int tail_len = vsize;
  //  const int tail_len = 800;
  int rdim;
  int ldim;
  double rx;
  double lx;
  
  int center_dim = (int) ((cs_x - xmin)/dx);
  

  fill_cvec(vsize, cs_vec, cmplx(0.0, 0.0));
  
  for(i=0; i!=tail_len; i++){
    rdim = center_dim+i+1;
    ldim = center_dim-i-1;  
    rx = rdim*dx + xmin;
    lx = ldim*dx + xmin;
    while(rdim >= vsize){
      rdim -= vsize;
    }
    while(ldim <= -1){
      ldim += vsize;
    }
    cs_vec[rdim] = add_c(cs_vec[rdim], coherent_state(rx, h, cs_x, cs_p));
    cs_vec[ldim] = add_c(cs_vec[ldim], coherent_state(lx, h, cs_x, cs_p));
    //    if(abs_c(cs_vec[rdim]) <= 1e-20 )
    //      break;
  }
  if(center_dim >= vsize){
    cs_vec[center_dim-vsize] = add_c(cs_vec[center_dim-vsize],
				     coherent_state(center_dim*dx+xmin,
						    h, cs_x, cs_p));
  }else{
    cs_vec[center_dim      ] = add_c(cs_vec[center_dim      ],
				     coherent_state(center_dim*dx+xmin,
						    h, cs_x, cs_p));
  }
  //    out_cs_vec(vsize, cs_vec);
  //    exit(0);
}


static void 
set_result(double **res_data,
	   double w, int i, int j)
{
  res_data[i][j] = w;

}

static double
get_weight(int vsize, const Complex *bra, const Complex *ket)
{
  int i;
  Complex sum = cmplx(0.0, 0.0);
  
  for(i=0; i!=vsize; i++){
    sum = add_c(sum, mul_c(bra[i], conj_c(ket[i])) );
  }

  return abs_c(sum) * abs_c(sum);
}

/*
static void 
normalize(double **res_data, int row, int col)
{
  int i, j;
  double sum = 0.0;
  
  for(i=0; i!=row; i++){
    for(j=0; j!=col; j++){
      sum += res_data[i][j];
    }
  }
  assert(sum != 0.0);
  for(i=0; i!=row; i++){
    for(j=0; j!=col; j++){
      res_data[i][j] /= sum;
    }
  }
  
}
*/

//// debug用 ////
/*
static void  out_cs_vec(int size, Complex *cs)
{
  int i;
  FILE *fp;
  if ((fp = fopen("cs.log", "w")) == NULL) {
    printf("file(cs.log) open error!!\n");
    exit(-1);
  }
  
  for(i=0; i!=size; i++){
    fprintf(fp, "%d\t%lg\t%lg\t%lg\n", i, abs_c(cs[i]),cs[i].re, cs[i].im);
  }

}


static void  dump_args(int N, const Complex *c_vec)
{
  int i;
  for(i=0; i!=N;i++){
    printf("[%f, %f]\n", c_vec[i].re, c_vec[i].im);  
  }
}
*/
