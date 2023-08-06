
#include <math.h>
#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>
#include "array.h"
#include "complex.h"
#include "mie.h"




static void
mie_error (char *s)


{
  printf ("Mie -- %s\n", s);
  exit (1);
}




 complex
      Lentz_Dn ( complex z, long n)


  {
     complex alpha_j1, alpha_j2, zinv, aj;
     complex alpha, result, ratio, runratio;



    zinv = csdiv (2.0, z);
    alpha = csmul (n + 0.5, zinv);
    aj = csmul (-n - 1.5, zinv);
    alpha_j1 = cadd (aj, cinv (alpha));
    alpha_j2 = aj;
    ratio = cdiv (alpha_j1, alpha_j2);
    runratio = cmul (alpha, ratio);




    do

      {
        aj.re = zinv.re - aj.re;
        aj.im = zinv.im - aj.im;
        alpha_j1 = cadd (cinv (alpha_j1), aj);
        alpha_j2 = cadd (cinv (alpha_j2), aj);
        ratio = cdiv (alpha_j1, alpha_j2);
        zinv.re *= -1;
        zinv.im *= -1;
        runratio = cmul (ratio, runratio);
      }



    while (fabs (cabs (ratio) - 1.0) > 1e-12);

    result = cadd (csdiv (-n, z), runratio);
    return result;
  }





void
Dn_down ( complex z, long nstop,  complex *D)


{
  long k;
   complex zinv, k_over_z;

  D[nstop - 1] = Lentz_Dn (z, nstop);
  zinv = cinv (z);

  for (k = nstop - 1; k >= 1; k--)
    {
      k_over_z = csmul (k, zinv);
      D[k - 1] = csub (k_over_z, cinv (cadd (D[k], k_over_z)));
    }
}



void
Dn_up ( complex z, long nstop,  complex *D)


{
   complex zinv, k_over_z;
  long k;

  D[0] = cinv (ctan (z));
  zinv = cinv (z);

  for (k = 1; k < nstop; k++)
    {
      k_over_z = csmul (k, zinv);
      D[k] = csub (cinv (csub (k_over_z, D[k - 1])), k_over_z);
    }
}




void
small_Mie (double x,  complex m, double *mu,
           long nangles,  complex *s1,
            complex *s2, double *qext, double *qsca,
           double *qback, double *g)



{
   complex ahat1, ahat2, bhat1;
   complex z0, m2, m4;
  double x2, x3, x4;

  if ((s1 == NULL) || (s2 == NULL))
    nangles = 0;

  m2 = csqr (m);
  m4 = csqr (m2);
  x2 = x * x;
  x3 = x2 * x;
  x4 = x2 * x2;
  z0.re = -m2.im;
  z0.im = m2.re - 1;


  {
     complex z1, z2, z3, z4, D;

    if (m.re == 0)
      {
        z3 = cset (0.0, 2.0 / 3.0 * (1.0 - 0.2 * x2));
        D = cset (1.0 - 0.5 * x2, 2.0 / 3.0 * x3);
      }
    else
      {
        z1 = csmul (2.0 / 3.0, z0);
        z2.re = 1.0 - 0.1 * x2 + (4.0 * m2.re + 5.0) * x4 / 1400.0;
        z2.im = 4.0 * x4 * m2.im / 1400.0;
        z3 = cmul (z1, z2);

        z4 = csmul (x3 * (1.0 - 0.1 * x2), z1);
        D.re = 2.0 + m2.re + (1 - 0.7 * m2.re) * x2 + (8 * m4.re - 385 * m2.re + 350.0) / 1400 * x4 + z4.re;
        D.im = (-0.7 * m2.im) * x2 + (8 * m4.im - 385 * m2.im) / 1400 * x4 + z4.im;
      }
    ahat1 = cdiv (z3, D);

  }



  {
     complex z2, z6, z7;
    if (m.re == 0)
      {
        bhat1 = cdiv (cset (0.0, -(1.0 - 0.1 * x2) / 3.0), cset (1 + 0.5 * x2, -x3 / 3));
      }
    else
      {
        z2 = csmul (x2 / 45, z0);
        z6.re = 1.0 + (2.0 * m2.re - 5.0) * x2 / 70.0;
        z6.im = m2.im * x2 / 35;
        z7.re = 1.0 - (2.0 * m2.re - 5.0) * x2 / 30.0;
        z7.im = -m2.im * x2 / 15;
        bhat1 = cmul (z2, cdiv (z6, z7));
      }
  }



  {
     complex z3, z8;

    if (m.re == 0)
      {
        ahat2 = cset (0, x2 / 30.);
      }
    else
      {
        z3 = csmul ((1.0 - x2 / 14) * x2 / 15.0, z0);
        z8.re = 2.0 * m2.re + 3.0 - (m2.re / 7.0 - 0.5) * x2;
        z8.im = 2.0 * m2.im - m2.im / 7.0 * x2;
        ahat2 = cdiv (z3, z8);
      }
  }



  {
     complex ss1;
    double T;

    T = cnorm (ahat1) + cnorm (bhat1) + (5 / 3) * cnorm (ahat2);
    *qsca = 6 * x4 * T;
    *qext = 6 * x * (ahat1.re + bhat1.re + (5 / 3) * ahat2.re);
    *g = (ahat1.re * (ahat2.re + bhat1.re) + ahat1.im * (ahat2.im + bhat1.im)) / T;
    ss1.re = 1.5 * x2 * (ahat1.re - bhat1.re - (5 / 3) * ahat2.re);
    ss1.re = 1.5 * x2 * (ahat1.im - bhat1.im - (5 / 3) * ahat2.im);
    *qback = cnorm (ss1);
  }



  {
    double muj, angle;
    long j;
    x3 *= 1.5;
    ahat1.re *= x3;
    ahat1.im *= x3;
    bhat1.re *= x3;
    bhat1.im *= x3;
    ahat2.re *= x3 * 5 / 3;
    ahat2.im *= x3 * 5 / 3;
    for (j = 0; j < nangles; j++)
      {
        muj = mu[j];
        angle = 2 * muj * muj - 1;
        s1[j].re = ahat1.re + (bhat1.re + ahat2.re) * muj;
        s1[j].im = ahat1.im + (bhat1.im + ahat2.im) * muj;
        s2[j].re = bhat1.re + ahat1.re * muj + ahat2.re * angle;
        s2[j].im = bhat1.im + ahat1.im * muj + ahat2.im * angle;
      }
  }



}




void
Mie (double x,  complex m, double *mu, long nangles,  complex *s1,
      complex *s2, double *qext, double *qsca, double *qback, double *g)



{

   complex *D;
   complex z1, an, bn, bnm1, anm1, qbcalc;
  double *pi0, *pi1, *tau;
   complex xi, xi0, xi1;
  double psi, psi0, psi1;
  double alpha, beta, factor;
  long n, k, nstop, sign;




  if (m.im < 0.0)
    mie_error ("This program requires m.im>=0");
  if (x <= 0.0)
    mie_error ("This program requires positive sphere sizes");
  if (nangles < 0)
    mie_error ("This program requires non-negative angle sizes");
  if (nangles < 0)
    mie_error ("This program requires non-negative angle sizes");
  if ((nangles > 0) && (s1 == NULL))
    mie_error ("Space must be allocated for s1 if nangles!=0");
  if ((nangles > 0) && (s2 == NULL))
    mie_error ("Space must be allocated for s2if nangles!=0");
  if (x > 20000)
    mie_error ("Program not validated for spheres with x>20000");



  if (((m.re == 0) && (x < 0.1)) || ((m.re > 0.0) && (cabs (m) * x < 0.1)))
    {
      small_Mie (x, m, mu, nangles, s1, s2, qext, qsca, qback, g);
      return;
    }




  nstop = floor (x + 4.05 * pow (x, 0.33333) + 2.0);




  if (nangles > 0)
    {
      set_carray (s1, nangles, cset (0.0, 0.0));
      set_carray (s2, nangles, cset (0.0, 0.0));

      pi0 = new_darray (nangles);
      pi1 = new_darray (nangles);
      tau = new_darray (nangles);

      set_darray (pi0, nangles, 0.0);
      set_darray (tau, nangles, 0.0);
      set_darray (pi1, nangles, 1.0);
    }


  if (m.re > 0)

    {
       complex z;

      z = csmul (x, m);

      D = new_carray (nstop + 1);
      if (D == NULL)
        mie_error ("Cannot allocate log array");

      if (fabs (m.im * x) < ((13.78 * m.re - 10.8) * m.re + 3.9))
        Dn_up (z, nstop, D);
      else
        Dn_down (z, nstop, D);
    }




  psi0 = sin (x);
  psi1 = psi0 / x - cos (x);
  xi0 = cset (psi0, cos (x));
  xi1 = cset (psi1, cos (x) / x + sin (x));
  *qsca = 0.0;
  *g = 0.0;
  *qext = 0.0;
  sign = 1;
  qbcalc = cset (0.0, 0.0);
  anm1 = cset (0.0, 0.0);
  bnm1 = cset (0.0, 0.0);



  for (n = 1; n <= nstop; n++)
    {

      if (m.re == 0.0)
        {
          an = csdiv (n * psi1 / x - psi0, csub (csmul (n / x, xi1), xi0));
          bn = csdiv (psi1, xi1);
        }
      else if (m.im == 0.0)
        {
          z1.re = D[n].re / m.re + n / x;
          an = csdiv (z1.re * psi1 - psi0, csub (csmul (z1.re, xi1), xi0));

          z1.re = D[n].re * m.re + n / x;
          bn = csdiv (z1.re * psi1 - psi0, csub (csmul (z1.re, xi1), xi0));
        }
      else
        {
          z1 = cdiv (D[n], m);
          z1.re += n / x;
          an = cdiv (cset (z1.re * psi1 - psi0, z1.im * psi1), csub (cmul (z1, xi1), xi0));

          z1 = cmul (D[n], m);
          z1.re += n / x;
          bn = cdiv (cset (z1.re * psi1 - psi0, z1.im * psi1), csub (cmul (z1, xi1), xi0));
        }



      for (k = 0; k < nangles; k++)
        {
          factor = (2.0 * n + 1.0) / (n + 1.0) / n;
          tau[k] = n * mu[k] * pi1[k] - (n + 1) * pi0[k];
          alpha = factor * pi1[k];
          beta = factor * tau[k];
          s1[k].re += alpha * an.re + beta * bn.re;
          s1[k].im += alpha * an.im + beta * bn.im;
          s2[k].re += alpha * bn.re + beta * an.re;
          s2[k].im += alpha * bn.im + beta * an.im;
        }

      for (k = 0; k < nangles; k++)
        {
          factor = pi1[k];
          pi1[k] = ((2.0 * n + 1.0) * mu[k] * pi1[k] - (n + 1.0) * pi0[k]) / n;
          pi0[k] = factor;
        }



      factor = 2.0 * n + 1.0;
      *g += (n - 1.0 / n) * (anm1.re * an.re + anm1.im * an.im + bnm1.re * bn.re + bnm1.im * bn.im);
      *g += factor / n / (n + 1.0) * (an.re * bn.re + an.im * bn.im);
      *qsca += factor * (cnorm (an) + cnorm (bn));
      *qext += factor * (an.re + bn.re);
      sign *= -1;
      qbcalc.re += sign * factor * (an.re - bn.re);
      qbcalc.im += sign * factor * (an.im - bn.im);



      factor = (2.0 * n + 1.0) / x;
      xi = csub (csmul (factor, xi1), xi0);
      xi0 = xi1;
      xi1 = xi;

      psi = factor * psi1 - psi0;
      psi0 = psi1;
      psi1 = xi1.re;

      anm1 = an;
      bnm1 = bn;


    }


  *qsca *= 2 / (x * x);
  *qext *= 2 / (x * x);
  *g *= 4 / (*qsca) / (x * x);
  *qback = cnorm (qbcalc) / (x * x);



  if (m.re > 0)
    free_carray (D);
  if (nangles > 0)
    {
      free_darray (pi0);
      free_darray (pi1);
      free_darray (tau);
    }


}




void
ez_Mie (double x, double n, double *qsca, double *g)


{
  long nangles = 0;
  double *mu = NULL;
   complex *s1 = NULL;
   complex *s2 = NULL;
   complex m;
  double qext, qback;

  m.re = n;
  m.im = 0.0;

  Mie (x, m, mu, nangles, s1, s2, &qext, qsca, &qback, g);
}

void
Qbsc_Mie (double x, double n, double im, double *qbsc, double *g)


{
  long nangles = 0;
  double *mu = NULL;
   complex *s1 = NULL;
   complex *s2 = NULL;
   complex m;
  double qext, qsca;

  m.re = n;
  m.im = im;

  Mie (x, m, mu, nangles, s1, s2, &qext, &qsca, qbsc, g);
}



