#!/usr/bin/env python
from __future__ import division, with_statement

"""
h5cat: h5cat two HDF5 files together without
overwriting nodes or throwing errors
"""

__version__ = "$Revision: 413 $"

# Copyright 2007 Michael M. Hoffman <hoffman+software@ebi.ac.uk>

from errno import EISDIR
from os import strerror
import sys

from path import path
from tables import NodeError

from ._utils import DESC, progress
from .hdf5 import h5open

def concatenate_file(src_file, dst_file):
    for src_node in src_file.root._f_walkNodes():
        group_pathname = src_node._v_parent._v_pathname
        dst_group = dst_file.getNode(group_pathname)

        try:
            src_node._f_copy(dst_group)
        except NodeError:
            pass

def h5cat(src_filenames, dst_filename, recursive=False, ignore_errors=False):
    with h5open(dst_filename, "w", DESC) as dst_file:
        for src_filename in src_filenames:
            progress(src_filename)

            src_filepath = path(src_filename)
            if src_filepath.isdir():
                if recursive:
                    src_filenames.extend(src_filepath.listdir())
                    continue
                else:
                    raise IOError(EISDIR, strerror(EISDIR))

            try:
                with h5open(src_filename) as src_file:
                    concatenate_file(src_file, dst_file)
            except IOError, err:
                if ignore_errors:
                    err_msg = "ignored %s: %s" % (err.__class__.__name__, err)
                    print >>sys.stderr, err_msg
                else:
                    raise

def parse_options(args):
    from optparse import OptionParser

    usage = "%prog [OPTION]... SRC... DST"
    version = "%%prog %s" % __version__
    parser = OptionParser(usage=usage, version=version)
    parser.add_option("-r", "--recursive", action="store_true",
                      help="act recursively on directories")
    parser.add_option("--ignore-errors", action="store_true",
                      help="continue to the next file on error instead of "
                      "terminating")

    options, args = parser.parse_args(args)

    if not len(args) >= 2:
        parser.print_usage()
        sys.exit(1)

    return options, args

def main(args=sys.argv[1:]):
    options, args = parse_options(args)

    h5cat(args[:-1], args[-1], recursive=options.recursive,
          ignore_errors=options.ignore_errors)

if __name__ == "__main__":
    sys.exit(main())
