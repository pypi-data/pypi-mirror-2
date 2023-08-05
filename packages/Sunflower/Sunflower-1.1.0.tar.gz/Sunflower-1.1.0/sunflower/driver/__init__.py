#!/usr/bin/env python
from __future__ import division

__version__ = "$Revision: 413 $"

# Copyright 2007 Michael M. Hoffman <hoffman+software@ebi.ac.uk>

import re
import sys

from optparse import IndentedHelpFormatter
from pkg_resources import load_entry_point

from .._poly import substitute

class DriverHelpFormatter(IndentedHelpFormatter):
    """just replaces 'Options:' with 'Driver options:'"""
    def format_heading(self, heading):
        if heading == "Options":
            heading = "Driver options"

        return IndentedHelpFormatter.format_heading(self, heading)

class Driver(object):
    def __init__(self, command_args, colnames, measurement, write_seq,
                 start_default=None, limit_slice=slice(None)):
        assert not command_args

        self.colnames = colnames
        self.measurement = measurement
        self.write_seq = write_seq
        self.start_default = start_default

        limit_start = limit_slice.start
        if not limit_start:
            limit_start = 0
        self.limit_start = limit_start

    def __exit__(self, *exc_info):
        pass

    @classmethod
    def print_help(cls):
        return cls.get_option_parser().print_help()

    @classmethod
    def print_usage(cls):
        return cls.get_option_parser().print_usage()

    def defline_start(self, defline):
        if self.start_default is None:
            start = get_defline_start(defline)
        else:
            start = self.start_default

        limit_start = self.limit_start
        if limit_start is not None:
            start += limit_start

        return start

class FileDriver(Driver):
    def __init__(self, command_args, *args, **kwargs):
        if len(command_args) != 1:
            self.print_help()
            sys.exit(1)

        # set special characters on Poly distributed systems
        filename = substitute(command_args[0])

        self.filename = filename

        Driver.__init__(self, [], *args, **kwargs)

    @staticmethod
    def get_option_parser():
        from optparse import OptionParser

        usage = ("%prog --driver=DRIVER [OPTION...] MODEL SEQFILE "
                 "[DRIVEROPTION...] OUTFILE")
        return OptionParser(usage=usage, formatter=DriverHelpFormatter())

def load(name):
    return load_entry_point("sunflower", "sunflower.drivers", name)

# genomic format:
# chromosome:NCBI36:21:1:46944323:1 chromosome 21
# or
# chromosome:NCBI36:21:1:46944323:1:subseq(0,30000) chromosome 21

def defline_identifier(defline):
    first_word = defline.lstrip().partition(" ")[0]
    col_split = first_word.split(":")

    if len(col_split) >= 3:
        return ":".join(col_split[:3])
    else:
        return first_word

re_directive = re.compile(r"\[sunflower ([^]]+)\]")
def get_defline_start(defline):
    m_directive = re_directive.search(defline)
    if m_directive:
        texts = m_directive.group(1).split()
        directives = dict(text.split("=") for text in texts)

        return int(directives.get("start", 0))

    res = 0

    first_word = defline.partition(" ")[0]
    col_split = first_word.split(":")

    if len(col_split) >= 5:
        res = int(col_split[3])
    if len(col_split) >= 7 and col_split[-1].startswith("subseq("):
        res += int(col_split[-1][7:].partition(",")[0])

    return res

def main(args=sys.argv[1:]):
    pass

if __name__ == "__main__":
    sys.exit(main())
