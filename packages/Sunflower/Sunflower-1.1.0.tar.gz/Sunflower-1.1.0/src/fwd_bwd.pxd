# $Revision: 32 $
# Copyright 2006-2007 Michael M. Hoffman <hoffman+software@ebi.ac.uk>

from c_numpy cimport npy_intp

cdef extern from "fwd_bwd.h":
  ctypedef double (*inner_funcptr)(double *, npy_intp *, double *, double *,
                                   npy_intp *, npy_intp, npy_intp, npy_intp,
                                   npy_intp, npy_intp, npy_intp)

  cdef double fwd_inner(double *, npy_intp *, double *, double *, npy_intp *,
                        npy_intp, npy_intp, npy_intp, npy_intp, npy_intp,
                        npy_intp)
  cdef double bwd_inner(double *, npy_intp *, double *, double *, npy_intp *,
                        npy_intp, npy_intp, npy_intp, npy_intp, npy_intp,
                        npy_intp)
