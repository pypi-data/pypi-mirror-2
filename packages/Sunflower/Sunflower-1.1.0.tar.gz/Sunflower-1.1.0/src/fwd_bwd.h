/* $Revision: 32 $ */
/* Copyright 2006-2007 Michael M. Hoffman <hoffman+software@ebi.ac.uk> */

/* you must #include "numpy/arrayobject.h" before including this file */

#define INNER_FUNC_SIGNATURE double *, const npy_intp *, const double *, \
                             const double *, const npy_intp *, npy_intp, \
                             npy_intp, npy_intp, npy_intp, npy_intp, npy_intp

typedef double (*inner_funcptr)(INNER_FUNC_SIGNATURE);

double fwd_inner(INNER_FUNC_SIGNATURE);
double bwd_inner(INNER_FUNC_SIGNATURE);
