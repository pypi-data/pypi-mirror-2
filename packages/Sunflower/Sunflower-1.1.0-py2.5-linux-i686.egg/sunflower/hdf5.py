#!/usr/bin/env python
from __future__ import division

"""
hdf5: HDF5/PyTables utility functions
"""

__version__ = "$Revision: 428 $"

from collections import defaultdict
from contextlib import closing
from hashlib import md5
import sys
from warnings import simplefilter

import tables

from ._utils import progress

SEP = "/" # XXX: this should be in PyTables
PREFIX = "_"
NYBBLES = 2

simplefilter("ignore", tables.NaturalNameWarning)

def balanced_path(name, nybbles=NYBBLES):
    hexdigest = md5(name).hexdigest()

    return SEP + PREFIX + hexdigest[:nybbles]

def balanced_path_full(name, *args, **kwargs):
    return SEP.join([balanced_path(name, *args, **kwargs), name])

# XXXopt: caching these here may be a memory leak
class H5GroupDefaultdict(defaultdict):
    def __init__(self, h5file, *args, **kwargs):
        self.h5file = h5file
        defaultdict.__init__(self, object, *args, **kwargs)

    def __missing__(self, key):
        res = self.h5file.createGroup("/", key.lstrip("/"))
        self[key] = res

        return res

class H5BalancedGroupCache(object):
    def __init__(self, h5file):
        self.h5file = h5file
        self.groups = H5GroupDefaultdict(h5file)

    def __getitem__(self, name):
        return self.groups[balanced_path(name)]

    def create_dataset(self, class_name, name, *args, **kwargs):
        where = self[name]._v_pathname

        method = getattr(self.h5file, "create" + class_name)
        return method(where, name, *args, **kwargs)

# XXX: upgrade PyTables, remove this
def h5open(filename, *args, **kwargs):
    return closing(tables.openFile(filename, *args, **kwargs))

def get_node(h5file, name):
    return h5file.getNode(balanced_path(name), name)

# slightly depth first for performance reasons
# assumes the layout is all groups on the first layer
def walk_nodes(h5file, classname="Array"):
    for group in h5file.root._v_groups.itervalues():
        for node in group._f_walkNodes(classname):
            yield node

def walk_nodes_progress(*args, **kwargs):
    inarrays = walk_nodes(*args, **kwargs)

    for inarray_index, inarray in enumerate(inarrays):
        progress("%6d: %s", inarray_index, inarray.name)

        yield inarray

def walk_included_nodes(h5file, names):
    if names:
        return (get_node(h5file, name) for name in names)
    else:
        return walk_nodes(h5file)

if __debug__:
    __pychecker__ = "no-special"
