#!/usr/bin/env python
from __future__ import division, with_statement

__version__ = "$Revision: 413 $"

# Copyright 2007 Michael M. Hoffman <hoffman+software@ebi.ac.uk>

import cPickle as pickle
from os import extsep
import re
import sys

from numpy import NINF, allclose, array, empty, exp as aexp, intp
from pkg_resources import resource_stream

SPECIES_RESOURCENAME = "species.pck"

# these attributes are inherently part of every HMM we produce
ALPHABET = "ACGT"
ALPHABET_INT = range(len(ALPHABET))
LEN_ALPHABET = len(ALPHABET)

SPECIAL_STATE_NAMES = ["silent", "unbound"]
OFFSET_SILENT = 0
OFFSET_UNBOUND = 1

# suffixes that mark the beginning of a TF
TF_START_SUFFIXES = set(["0", "f0", "r0"])

# version of pickle being used
PICKLE_PROTOCOL = 2

EXT = "sfl"

# XXX: this stuff should be OO after conversion to HDF5

def get_params(model):
    a = model["logprobs_transition"]
    e = model["logprobs_emission"]
    cf = intp(model["connections_f"])
    cb = intp(model["connections_b"])

    return (a, e, cf, cb)

def check(model):
    """verify that appropriate probabilities sum to 0 or 1"""
    a = aexp(model["logprobs_transition"])
    e = aexp(model["logprobs_emission"])

    assert e[OFFSET_SILENT].sum() == 0.0

    # XXX: need to think carefully about how much tolerance to allow
    # here
    assert allclose(e[OFFSET_UNBOUND:].sum(-1), 1.0)

    assert allclose(a.sum(-1), 1.0)

def adjust(model, logprobs_emission):
    model["logprobs_emission"][OFFSET_UNBOUND] = logprobs_emission

def _load_from_resource(resourcename):
    full_resourcename = extsep.join([resourcename, EXT])

    return pickle.load(resource_stream("sunflower.data", full_resourcename))

def load(filename, resource=False):
    if resource:
        # first check the index
        species_info_resource = \
            resource_stream("sunflower.data", SPECIES_RESOURCENAME)
        species_infos = pickle.load(species_info_resource)

        try:
            resourcename, logprobs_emission = species_infos[filename]

            res = _load_from_resource(resourcename)
            adjust(res, logprobs_emission)
            return res
        except KeyError:
            # if that doesn't work, use the raw resource name
            return _load_from_resource(filename)
    else:
        return pickle.load(open(filename, "rb"))

def save(filename, model):
    if __debug__:
        check(model)

    with open(filename, "wb") as outfile:
        pickle.dump(model, outfile, PICKLE_PROTOCOL)

def fill_array(scalar, shape, dtype=None, *args, **kwargs):
    if dtype is None:
        dtype = array(scalar).dtype

    res = empty(shape, dtype, *args, **kwargs)
    res.fill(scalar)

    return res

def _arrayize_connection_list(connection_list, num_states):
    max_len = max(len(ks) for ks in connection_list) + 1

    res = fill_array(-1, (num_states, max_len), dtype=intp)

    for l, ks in enumerate(connection_list):
        res[l, 0] = len(ks)
        res[l, 1:len(ks)+1] = ks

    return res

def _make_connections(a, num_states, all_states):
    connection_list_f = [[] for _ in all_states]
    connection_list_b = [[] for _ in all_states]

    for k in all_states:
        for l in all_states:
            if a[k, l] != NINF:
                connection_list_f[l].append(k)
                connection_list_b[k].append(l)

    return [_arrayize_connection_list(connection_list, num_states)
            for connection_list in [connection_list_f, connection_list_b]]

def optimize(model):
    """
    add denormalized data

    The normalized data is really only (alphabet, desc, state_names,
    logprobs_transition, logprobs_emission)

    emitting_states is denormal unless the code in simulator has been
    updated to support more than one silent state.
    """

    num_states = len(model["state_names"])
    logprobs_a = model["logprobs_transition"]

    # not xrange because will be pickled
    all_states = range(num_states)
    emitting_states = range(OFFSET_UNBOUND, num_states)

    connections = _make_connections(logprobs_a, num_states, all_states)

    model.update(all_states=all_states,
                 emitting_states=emitting_states,
                 num_states=num_states,
                 connections_f=connections[0],
                 connections_b=connections[1])

def dump(model):
    print model["state_names"]
    print

    print "a = "
    print aexp(model["logprobs_transition"])
    print

    print "e = "
    print aexp(model["logprobs_emission"])
    print

    print "cf = %s" % model["connections_f"]
    print

    print "cb = %s" % model["connections_b"]

def main(args):
    for arg in args:
        dump(load(arg))

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
