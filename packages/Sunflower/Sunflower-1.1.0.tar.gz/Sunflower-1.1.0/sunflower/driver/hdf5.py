#!/usr/bin/env python
from __future__ import division

__version__ = "$Revision: 428 $"

# Copyright 2007, 2009 Michael M. Hoffman <hoffman+software@ebi.ac.uk>

import sys

from tables import openFile

from . import FileDriver, defline_identifier
from .._utils import DESC
from ..hdf5 import H5BalancedGroupCache

class HDF5Driver(FileDriver):
    def __enter__(self):
        outfile = openFile(self.filename, "w", DESC)
        self.file = outfile
        self.groups = H5BalancedGroupCache(outfile)

        return self

    def __exit__(self, *exc_info):
        self.file.close()

    def __call__(self, arr, (defline, seq)):
        name = defline_identifier(defline)
        leaf = self.groups.create_dataset("Array", name, arr, defline)

        attrs = leaf.attrs
        attrs.measurement = self.measurement
        attrs.colnames = self.colnames
        attrs.run_info = DESC

        if self.write_seq:
            attrs.seq = seq

        attrs.start = self.defline_start(defline)

def main(args=sys.argv[1:]):
    pass

if __name__ == "__main__":
    sys.exit(main())
