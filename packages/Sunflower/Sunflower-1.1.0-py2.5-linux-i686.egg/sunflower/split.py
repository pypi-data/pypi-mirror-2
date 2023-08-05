#!/usr/bin/env python
from __future__ import division, with_statement

"""
split: DESCRIPTION

OUTTMPL like myfile.%s.h5
"""

__version__ = "$Revision: 413 $"

# Copyright 2007 Michael M. Hoffman <hoffman+software@ebi.ac.uk>

from contextlib import nested
from itertools import repeat
import sys

from tables import Group, NoSuchNodeError

from .hdf5 import h5open, walk_nodes
from .utils import progress

#parameters.NODE_MAX_SLOTS = 0

def split_file(inwalker, outfiles, measurements):
    for src_node in inwalker:
        name = src_node.name
        progress(name)

        assert (src_node.attrs.measurement == measurements).all()

        src_array = src_node.read()
        title = src_node.title
        byteorder = src_node.byteorder
        group_pathname = src_node._v_parent._v_pathname
        src_attrs = src_node.attrs

        for outfile_index, outfile in enumerate(outfiles):
            dst_array = src_array[..., outfile_index]

            dst_node = outfile.createArray(group_pathname, name, dst_array,
                                           title, byteorder,
                                           createparents=True)

            src_attrs._f_copy(dst_node)
            dst_node.attrs.measurement = measurements[outfile_index]

def split(infilename, out_template, inroot_pathname="/"):
    if inroot_pathname is None:
        inroot_pathname = "/"

    with h5open(infilename) as infile:
        inroot_node = infile.getNode(inroot_pathname)

        # using isinstance to avoid running afoul of natural namings
        # that mess this up
        if isinstance(inroot_node, Group):
            inwalker_factory = inroot_node._f_walkNodes
        else:
            inwalker_factory = repeat(inroot_node)

        first_array = inwalker_factory().next()

        measurements = first_array.attrs.measurement

        assert not isinstance(measurements, basestring)

        outfile_managers = (h5open(out_template % measurement, "a")
                            for measurement in measurements)

        with nested(*outfile_managers) as outfiles:
            split_file(inwalker_factory(), outfiles, measurements)

def parse_options(args):
    from optparse import OptionParser

    usage = "%prog [OPTION]... INFILE OUTTMPL"
    version = "%%prog %s" % __version__
    parser = OptionParser(usage=usage, version=version)
    parser.add_option("-n", "--node", metavar="NODE",
                      help="only produce output for children of NODE")

    options, args = parser.parse_args(args)

    if not len(args) == 2:
        parser.print_usage()
        sys.exit(1)

    return options, args

def main(args=sys.argv[1:]):
    options, args = parse_options(args)

    return split(args[0], args[1], inroot_pathname=options.node)

if __name__ == "__main__":
    sys.exit(main())
