/* $Revision: 304 $ */
/* Copyright 2006-2007 Michael M. Hoffman <hoffman+software@ebi.ac.uk> */

#include "Python.h" /* must be the very first include */

#include <math.h>

#define NO_IMPORT
#include "numpy/arrayobject.h"

#include "fwd_bwd.h"
#include "logmath.h"

/* at some point in the future I wil be changing the data structure
** here to one where a and c are combined into a single struct, and
** referred to with a double pointer (the first level of which is a
** struct containing e) rather than fixed (row, col)
** arrays
*/

/* like this:
double fwd_inner2(double * const f,
                  const npy_intp * const x,
                  const hmm_half * const model,
                  const npy_intp f_rows, // should also be buried in a struct
                  const npy_intp f_cols, // ditto XXX: lookup how numpy does it
                  const npy_intp f_row_start)
{
    ...
}
*/

/* x is 1-based. f[0, *] is for initialization. b[0, *] is unused */

/* c: connected_states */

double
fwd_inner(double * const f,
          const npy_intp * const x,
          const double * const a,
          const double * const e,
          const npy_intp * const c,
          const npy_intp f_rows,
          const npy_intp f_cols,
          const npy_intp a_cols,
          const npy_intp e_cols,
          const npy_intp c_cols,
          const npy_intp f_row_start)
{
  npy_intp i, k, l;
  npy_intp x_i;
  double f_ik, f_il, f_iminus1k, a_kl, e_lx, res;
  double *fp;
  npy_intp c_offset_start, c_offset;

  /* array initialization */
  for (fp = f + (f_row_start * f_cols); fp < f + (f_rows * f_cols); fp++) {
    *fp = -INFINITY;
  }

  /* initialization */
  f[0] = 0;

  /* recursion */
  for (i = (f_row_start ? f_row_start : 1); i < f_rows; i++) {
      x_i = x[i];

      /* emitting states */
      for (l = 1; l < f_cols; l++) {
          f_il = -INFINITY;

          c_offset_start = l * c_cols;

          /* XXXopt: use pointers instead? */
          for (c_offset = c_offset_start + 1;
               c_offset <= c_offset_start + c[c_offset_start];
               c_offset++) {
              k = c[c_offset];

              /* XXXopt: calculate f[(i-1) * f_cols] once in outer
                 loop (repeat in backward) */
              f_iminus1k = f[(i - 1) * f_cols + k];

              if (f_iminus1k != -INFINITY) {
                /* XXXopt: calculate a[l] once (repeat in backwards) */
                /* a_kl should never be -INFINITY or it wouldn't be in c */
                a_kl = a[k * a_cols + l];

                /* XXXopt: loop after first assignment, so we don't
                   have to check this equality every time */
                if (f_il == -INFINITY) {
                  f_il = f_iminus1k + a_kl;
                } else {
                  f_il = logadd(f_il, f_iminus1k + a_kl);
                }
              }
          }

          if (f_il != -INFINITY) {
              e_lx = e[l * e_cols + x_i];
              f[i * f_cols + l] = f_il + e_lx;
          }
      }

      /* silent state */
      f_il = -INFINITY;

      for (c_offset = 1; c_offset <= c[0]; c_offset++) {
          k = c[c_offset];
          f_ik = f[i * f_cols + k];

          if (f_ik != -INFINITY) {
            a_kl = a[k * a_cols];

            if (f_il == -INFINITY) {
              f_il = f_ik + a_kl;
            } else {
              f_il = logadd(f_il, f_ik + a_kl);
            }
          }
      }

      f[i * f_cols] = f_il;
  }

  /* termination */
  res = -INFINITY;
  for (k = 1; k < f_cols; k++) {
    f_ik = f[(f_rows - 1) * f_cols + k];
    if (f_ik != -INFINITY) {
      res = f_ik;
      break;
    }
  }

  for (k = k+1; k < f_cols; k++) {
    f_ik = f[(f_rows - 1) * f_cols + k];
    if (f_ik != -INFINITY) {
      if (res == -INFINITY) {
        res = f_ik;
      } else {
        res = logadd(res, f_ik);
      }
    }
  }

  return res;
}

double
bwd_inner(double * const b,
          const npy_intp * const x,
          const double * const a,
          const double * const e,
          const npy_intp * const c,
          const npy_intp b_rows,
          const npy_intp b_cols,
          const npy_intp a_cols,
          const npy_intp e_cols,
          const npy_intp c_cols,
          const npy_intp b_row_start)
{
  npy_intp i, k, l;
  npy_intp x_iplus1;
  double b_ik, b_il, b_iplus1l, a_kl, e_lx, res;
  double *bp;
  npy_intp c_offset_start, c_offset;

  /* array initialization: if b_row_start == 0, then initialize everything */
  for (bp = b + ((b_row_start ? b_row_start : b_rows)* b_cols) - 1; bp >= b; bp--) {
    *bp = -INFINITY;
  }

  /* initialization */
  /* iterate through the emitting states */
  for (k = 1; k < b_cols; k++) {
      b[(b_rows - 1) * b_cols + k] = 0;
  }

  /* recursion */
  for (i = (b_row_start ? (b_row_start - 1) : (b_rows - 2)); i > 0; i--) {
      /* silent state for x[i+1] */
      x_iplus1 = x[i + 1];
      b_ik = -INFINITY;

      /* XXXopt: use pointers instead? */
      for (c_offset = 1; c_offset <= c[0]; c_offset++) {
        l = c[c_offset];
        b_il = b[(i + 1) * b_cols + l];

        a_kl = a[l];
        if (a_kl != -INFINITY) {
          e_lx = e[l * e_cols + x_iplus1];

          if (e_lx != -INFINITY) {
            if (b_ik == -INFINITY) {
              b_ik = b_il + a_kl + e_lx;
            } else {
              b_ik = logadd(b_ik, b_il + a_kl + e_lx);
            }
          }
        }
      }
      b[(i + 1) * b_cols] = b_ik;

      /* emitting states */
      for (k = 1; k < b_cols; k++) {
          b_ik = -INFINITY;
          c_offset_start = k * c_cols;

          for (c_offset = c_offset_start + 1;
               c_offset <= c_offset_start + c[c_offset_start];
               c_offset++) {
              l = c[c_offset];
              b_iplus1l = b[(i + 1) * b_cols + l];

              if (b_iplus1l != -INFINITY) {
                  a_kl = a[k * a_cols + l];

                  if (a_kl != -INFINITY) {
                      e_lx = e[l * e_cols + x_iplus1];
                      if (e_lx == -INFINITY) {
                          e_lx = 0;
                      }

                      if (b_ik == -INFINITY) {
                        b_ik = b_iplus1l + a_kl + e_lx;
                      } else {
                        b_ik = logadd(b_ik, b_iplus1l + a_kl + e_lx);
                      }
                  }
              }
          }

          if (b_ik != -INFINITY) {
              b[i * b_cols + k] = b_ik;
          }
      }
  }
  /* termination */
  res = -INFINITY;
  x_iplus1 = x[1];

  /* emitting states */
  for (l = 1; l < b_cols; l++) {
    a_kl = a[l]; /* k = 0 */
    e_lx = e[l * e_cols + x_iplus1];
    b_il = b[b_cols + l]; /* i = 1 */

    if (b_il != -INFINITY) {
      res = a_kl + e_lx +b_il;
      break;
    }
  }

  for (l = l+1; l < b_cols; l++) {
    b_il = b[b_cols + l]; /* i = 1 */
    if (b_il != -INFINITY) {
      a_kl = a[l]; /* k = 0 */

      if (a_kl != -INFINITY) {
        e_lx = e[l * e_cols + x_iplus1];

        if (e_lx != -INFINITY) {
          if (res == -INFINITY) {
            res = a_kl + e_lx + b_il;
          } else {
            res = logadd(res, a_kl + e_lx + b_il);
          }
        }
      }
    }
  }

  return res;
}
