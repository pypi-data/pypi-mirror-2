#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <float.h>

#include "complex.h"



static void
complex_error (char *s)


{
  printf ("%s\n", s);
  exit (1);
}





complex
      cset (double a, double b)


  {
    complex c;
    c.re = a;
    c.im = b;
    return c;
  }




complex
      cpolarset (double r, double theta)


  {
    return cset (r * cos (theta), r * sin (theta));
  }




double
cabs (complex z)


{
  double x, y, temp;

  x = fabs (z.re);
  y = fabs (z.im);
  if (x == 0.0)
    return y;
  if (y == 0.0)
    return x;

  if (x > y)
    {
      temp = y / x;
      return (x * sqrt (1.0 + temp * temp));
    }

  temp = x / y;
  return (y * sqrt (1.0 + temp * temp));
}




double
carg (complex z)


{
  return atan2 (z.im, z.re);
}




double
cnorm (complex z)


{
  return (z.re * z.re + z.im * z.im);
}




complex
      csqrt (complex z)


  {
    double a, b;

    if ((z.re == 0.0) && (z.im == 0.0))
      return cset (0, 0);

    a = sqrt ((fabs (z.re) + cabs (z)) * 0.5);
    if (z.re >= 0)
      b = z.im / (a + a);
    else
      {
        b = z.im < 0 ? -a : a;
        a = z.im / (b + b);
      }

    return cset (a, b);
  }




complex
      csqr (complex z)


  {
    return cmul (z, z);
  }




complex
      cinv (complex w)


  {
    double r, d;

    if ((w.re == 0) && (w.im == 0))
      complex_error ("Attempt to invert 0+0i");

    if (fabs (w.re) >= fabs (w.im))
      {
        r = w.im / w.re;
        d = 1 / (w.re + r * w.im);
        return cset (d, -r * d);
      }

    r = w.re / w.im;
    d = 1 / (w.im + r * w.re);
    return cset (r * d, -d);
  }




complex
      conj (complex z)


  {
    return cset (z.re, -z.im);
  }




complex
      cadd (complex z, complex w)


  {
    complex c;

    c.im = z.im + w.im;
    c.re = z.re + w.re;
    return c;
  }





complex
      csub (complex z, complex w)


  {
    complex c;
    c.im = z.im - w.im;
    c.re = z.re - w.re;
    return c;
  }




complex
      cmul (complex z, complex w)


  {
    complex c;
    c.re = z.re * w.re - z.im * w.im;
    c.im = z.im * w.re + z.re * w.im;
    return c;
  }




complex
      cdiv (complex z, complex w)


  {
    complex c;
    double r, denom;

    if ((w.re == 0) && (w.im == 0))
      complex_error ("Attempt to divide by 0+0i");

    if (fabs (w.re) >= fabs (w.im))
      {
        r = w.im / w.re;
        denom = w.re + r * w.im;
        c.re = (z.re + r * z.im) / denom;
        c.im = (z.im - r * z.re) / denom;
      }
    else
      {
        r = w.re / w.im;
        denom = w.im + r * w.re;
        c.re = (z.re * r + z.im) / denom;
        c.im = (z.im * r - z.re) / denom;
      }
    return c;
  }




double
crdiv (complex z, complex w)


{
  double r, c, denom;

  if ((w.re == 0) && (w.im == 0))
    complex_error ("Attempt to find real part with divisor 0+0i");

  if (fabs (w.re) >= fabs (w.im))
    {
      r = w.im / w.re;
      denom = w.re + r * w.im;
      c = (z.re + r * z.im) / denom;
    }
  else
    {
      r = w.re / w.im;
      denom = w.im + r * w.re;
      c = (z.re * r + z.im) / denom;
    }
  return c;
}




double
crmul (complex z, complex w)


{
  return z.re * w.re - z.im * w.im;
}





complex
      csadd (double x, complex z)


  {
    complex c;
    c.re = x + z.re;
    c.im = z.im;
    return c;
  }




complex
      csdiv (double x, complex w)


  {
    complex c;
    double r, factor;

    if ((w.re == 0) && (w.im == 0))
      complex_error ("Attempt to divide scalar by 0+0i");

    if (fabs (w.re) >= fabs (w.im))
      {
        r = w.im / w.re;
        factor = x / (w.re + r * w.im);
        c.re = factor;
        c.im = -r * factor;
      }
    else
      {
        r = w.re / w.im;
        factor = x / (w.im + r * w.re);
        c.im = -factor;
        c.re = r * factor;
      }
    return c;
  }




complex
      csmul (double x, complex z)


  {
    complex c;
    c.re = z.re * x;
    c.im = z.im * x;
    return c;
  }





complex
      csin (complex z)


  {
    return cset (sin (z.re) * cosh (z.im), cos (z.re) * sinh (z.im));
  }




complex
      ccos (complex z)


  {
    return cset (cos (z.re) * cosh (z.im), -(sin (z.re) * sinh (z.im)));
  }




complex
      ctan (complex z)


  {
    double t, x, y;

    if (z.im == 0)
      return cset (tan (z.re), 0.0);
    if (z.im > DBL_MAX_10_EXP)
      return cset (0.0, 1.0);
    if (z.im < -DBL_MAX_10_EXP)
      return cset (0.0, -1.0);

    x = 2 * z.re;
    y = 2 * z.im;
    t = cos (x) + cosh (y);
    if (t == 0)
      complex_error ("Complex tangent is infinite");

    return cset (sin (x) / t, sinh (y) / t);
  }




complex
      casin (complex z)


  {
    complex x;
    x = clog (cadd (cset (-z.im, z.re), csqrt (csub (cset (1, 0), cmul (z, z)))));
    return cset (x.im, -x.re);
  }




complex
      cacos (complex z)


  {
    complex x;
    x = clog (cadd (z, cmul (cset (0, 1), csqrt (csub (cset (1, 0), csqr (z))))));
    return cset (x.im, -x.re);
  }




complex
      catan (complex z)


  {
    complex x;
    x = clog (cdiv (cset (z.re, 1 + z.im), cset (-z.re, 1 - z.im)));
    return cset (-x.im / 2, x.re / 2);
  }





complex
      csinh (complex z)


  {
    return cset (sinh (z.re) * cos (z.im), cosh (z.re) * sin (z.im));
  }




complex
      ccosh (complex z)


  {
    return cset (cosh (z.re) * cos (z.im), sinh (z.re) * sin (z.im));
  }




complex
      ctanh (complex z)


  {
    double x = 2 * z.re;
    double y = 2 * z.im;
    double t = 1.0 / (cosh (x) + cos (y));

    return cset (t * sinh (x), t * sin (y));
  }




complex
      catanh (complex z)


  {
    return catan (cset (-z.im, z.re));
  }




complex
      casinh (complex z)


  {
    return casin (cset (-z.im, z.re));
  }





complex
      cexp (complex z)


  {
    double x = exp (z.re);
    return cset (x * cos (z.im), x * sin (z.im));
  }




complex
      clog (complex z)


  {
    return cset (log (cabs (z)), carg (z));
  }




complex
      clog10 (complex z)


  {
    return cset (0.2171472409516259 * log (cnorm (z)), carg (z));
  }





complex *
      new_carray (long size)


  {
    complex *a;

    if (size <= 0)
      complex_error ("Non-positive complex array size chosen");

    a = (complex *) malloc (size * sizeof (complex));

    if (a == NULL)
      complex_error ("Can't allocate complex array");
    return a;
  }




void
free_carray (complex *a)


{
  if (a != NULL)
    free (a);
}




complex *
      copy_carray (complex *a, long size)


  {
    complex *b = NULL;

    if (a == NULL)
      complex_error ("Can't duplicate a NULL complex array");

    b = new_carray (size);
    if (b != NULL)
      memcpy (b, a, size * sizeof (complex));
    return b;
  }




void
set_carray (complex *a, long size, complex z)


{
  long j;

  if (a == NULL)
    complex_error ("Can't operate on a NULL complex array");

  for (j = 0; j < size; j++)
    a[j] = z;
}
