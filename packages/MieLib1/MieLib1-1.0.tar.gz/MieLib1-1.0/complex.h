#ifndef _COMPLEX_
#define _COMPLEX_

typedef struct 
  {
    double re, im;
  }complex;


complex cset (double a, double b)

 ;

complex cpolarset (double r, double theta)

 ;


double cabs (complex z)

 ;

double carg (complex z)

 ;

complex csqr (complex z)

 ;

complex conj (complex z)

 ;

double cnorm (complex z)

 ;

complex csqrt (complex z)

 ;

complex cinv (complex w)

 ;


complex cadd (complex z, complex w)

 ;

complex csub (complex z, complex w)

 ;

complex cmul (complex z, complex w)

 ;

complex cdiv (complex z, complex w)

 ;


double crdiv (complex z, complex w)

 ;

double crmul (complex z, complex w)

 ;

complex csadd (double x, complex z)

 ;

complex csdiv (double x, complex w)

 ;

complex csmul (double x, complex z)

 ;


complex csin (complex z)

 ;

complex ccos (complex z)

 ;

complex ctan (complex z)

 ;

complex casin (complex z)

 ;

complex cacos (complex z)

 ;

complex catan (complex z)

 ;


complex csinh (complex z)

 ;

complex ccosh (complex z)

 ;

complex ctanh (complex z)

 ;

complex catanh (complex z)

 ;

complex casinh (complex z)

 ;


complex cexp (complex z)

 ;

complex clog (complex z)

 ;

complex clog10 (complex z)

 ;


complex *new_carray (long size)

 ;

void free_carray (complex *a)

 ;

complex *copy_carray (complex *a, long size)

 ;

void set_carray (complex *a, long size, complex z)

 ;
#endif