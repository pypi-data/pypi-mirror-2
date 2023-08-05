#!/usr/bin/env python
from __future__ import division

__version__ = "$Revision: 457 $"

# Copyright 2007, 2009 Michael M. Hoffman <hoffman+software@ebi.ac.uk>

import sys

from . import FileDriver, defline_identifier

class TabDelimDriver(FileDriver):
    def __enter__(self):
        outfile = open(self.filename, "w")
        self.file = outfile

        return self

    def __exit__(self, *exc_info):
        self.file.close()

    def __call__(self, arr, (defline, seq)):
        name = defline_identifier(defline)

        self.file.write(name)
        self.file.write("\t")
        self.file.write(str(arr))
        self.file.write("\n")

def main(args=sys.argv[1:]):
    pass

if __name__ == "__main__":
    sys.exit(main())
