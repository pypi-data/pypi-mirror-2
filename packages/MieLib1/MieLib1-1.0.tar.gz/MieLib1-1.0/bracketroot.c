
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include "bracketroot.h"



void
bracketroot (double (*fx) (double), double x1, double x2, long n,
             double xb1[], double xb2[], long *nrequested)



{
  long nfound, i;
  double x, fp, fc, dx;

  if ((n <= 0) | (*nrequested <= 0))
    return;

  nfound = 0;
  dx = (x2 - x1) / n;
  x = x1;
  fp = (*fx) (x);
  for (i = 0; i < n; i++)
    {
      x += dx;
      fc = (*fx) (x);
      if (((fc < 0.0) && (fp > 0.0)) || ((fp < 0.0) && (fc > 0.0)))
        {
          nfound++;
          xb1[nfound - 1] = x - dx;
          xb2[nfound - 1] = x;
          if (*nrequested == nfound)
            return;
        }
      fp = fc;
    }
  *nrequested = nfound;
}
