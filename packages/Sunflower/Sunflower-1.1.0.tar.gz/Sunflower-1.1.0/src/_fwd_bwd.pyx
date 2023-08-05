__version__ = "$Revision: 36 $"

# Copyright 2006-2007 Michael M. Hoffman <hoffman+software@ebi.ac.uk>

from c_numpy cimport PyArray_DATA, PyArray_GETCONTIGUOUS, import_array, ndarray, npy_intp
from fwd_bwd cimport bwd_inner, fwd_inner, inner_funcptr

import_array()

# I use f to represent f or b
cdef double call_inner(inner_funcptr func, ndarray f, ndarray x, ndarray a, ndarray e, ndarray c, npy_intp f_row_start):
    # declarations
    cdef ndarray f_contiguous "f_contiguous", a_contiguous "a_contiguous",
    cdef ndarray e_contiguous "e_contiguous", x_contiguous "x_contiguous"
    cdef ndarray c_contiguous "c_contiguous"

    cdef double *f_data "f_data", *a_data "a_data", *e_data "e_data"
    cdef npy_intp *x_data "x_data", *c_data "c_data"
    cdef npy_intp f_rows "f_rows"
    cdef npy_intp a_cols "a_cols", e_cols "e_cols"
    cdef npy_intp f_cols "f_cols", c_cols "c_cols"

    # array data access: f
    f_contiguous = PyArray_GETCONTIGUOUS(f)
    f_rows = f_contiguous.dimensions[0]
    f_cols = f_contiguous.dimensions[1]
    f_data = <double *>PyArray_DATA(f_contiguous)

    # array data access: x
    x_contiguous = PyArray_GETCONTIGUOUS(x)
    x_data = <npy_intp *>PyArray_DATA(x_contiguous)

    # array data access: a
    a_contiguous = PyArray_GETCONTIGUOUS(a)
    a_cols = a_contiguous.dimensions[1]
    a_data = <double *>PyArray_DATA(a_contiguous)

    # array data access: e
    e_contiguous = PyArray_GETCONTIGUOUS(e)
    e_cols = e_contiguous.dimensions[1]
    e_data = <double *>PyArray_DATA(e_contiguous)

    # array data access: c
    c_contiguous = PyArray_GETCONTIGUOUS(c)
    c_cols = c_contiguous.dimensions[1]
    c_data = <npy_intp *>PyArray_DATA(c_contiguous)

    return func(f_data, x_data, a_data, e_data, c_data, f_rows, f_cols, a_cols, e_cols, c_cols, f_row_start)

def fwd(ndarray f, ndarray x, ndarray a, ndarray e, ndarray c, npy_intp f_row_start):
    return call_inner(fwd_inner, f, x, a, e, c, f_row_start)

def bwd(ndarray b, ndarray x, ndarray a, ndarray e, ndarray c, npy_intp b_row_start):
    return call_inner(bwd_inner, b, x, a, e, c, b_row_start)
