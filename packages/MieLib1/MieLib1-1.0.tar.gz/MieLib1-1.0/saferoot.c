
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include "saferoot.h"



double
saferoot (void (*funcd) (double, double *, double *), double x1, double x2, double xacc)



{
  double df, dx, dxold, f, fh, fl;
  double temp, xh, xl, rts;
  double temp1, temp2;
  long j, MAXIT = 100;

  (*funcd) (x1, &fl, &df);
  if (fl == 0.0)
    return x1;

  (*funcd) (x2, &fh, &df);
  if (fh == 0.0)
    return x2;

  if ((fl > 0.0 && fh > 0.0) || (fl < 0.0 && fh < 0.0))
    {
      printf ("saferoot -- Root must be bracketed.\n");
      printf ("saferoot -- x1  = %10.5f; f(x1) = %10.5f \n", x1, fl);
      printf ("saferoot -- x2  = %10.5f; f(x2) = %10.5f \n", x2, fh);
      exit (1);
    }


  if (fl < 0.0)
    {
      xl = x1;
      xh = x2;
    }
  else
    {
      xh = x1;
      xl = x2;
    }

  rts = 0.5 * (x1 + x2);
  dxold = fabs (x2 - x1);
  dx = dxold;
  (*funcd) (rts, &f, &df);

  for (j = 1; j <= MAXIT; j++)
    {

      temp1 = (rts - xh) * df - f;
      temp2 = (rts - xl) * df - f;

      if ((temp1 * temp2 >= 0.0) || (fabs (2.0 * f) > fabs (dxold * df)))
        {
          dxold = dx;
          dx = 0.5 * (xh - xl);
          rts = xl + dx;
          if (xl == rts)
            return rts;
        }
      else
        {
          dxold = dx;
          dx = f / df;
          temp = rts;
          rts -= dx;
          if (temp == rts)
            return rts;
        }

      if (fabs (dx) < xacc)
        return rts;

      (*funcd) (rts, &f, &df);

      if (f < 0.0)
        xl = rts;
      else
        xh = rts;
    }

  printf ("saferoot -- Root cannot be found.\n");
  printf ("saferoot -- Executed %ld iterations. \n", x1, fl);
  exit (1);
  return 0.0;
}
