#ifndef MIE_H
#define MIE_H

 complex Lentz_Dn ( complex z, long n)

 ;

void Dn_down ( complex z, long nstop,  complex *D)

 ;

void Dn_up ( complex z, long nstop,  complex *D)

 ;

void small_Mie (double x,  complex m, double *mu,
		long nangles,  complex *s1,
		 complex *s2, double *qext, double *qsca,
		double *qback, double *g)

 ;

void Mie (double x,  complex m, double *mu, long nangles,  complex *s1,
    complex *s2, double *qext, double *qsca, double *qback, double *g)

 ;

void ez_Mie (double x, double n, double *qsca, double *g)

 ;
 

void Qbsc_Mie(double x, double n, double im, double *qbsc, double *g)
;

#endif

