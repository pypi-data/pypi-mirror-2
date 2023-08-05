#!/usr/bin/env python
from __future__ import division, with_statement

"""
make_species_info: DESCRIPTION
"""

__version__ = "$Revision: 256 $"

# Copyright 2007 Michael M. Hoffman <hoffman+software@ebi.ac.uk>

INPUT_FILENAME = "all.fastacomposition"
OUTPUT_FILENAME = "../../sunflower/data/species.pck"

from cPickle import dump
import sys

from sunflower.hmm import PICKLE_PROTOCOL
from sunflower.recompose import cols2logprobs_emission

def make_species_info(filename=INPUT_FILENAME):
    info = {}

    with open(filename) as infile:
        for line in infile:
            cols = line.rstrip().split()

            species = cols[0]
            resourcename = cols[1]
            count_cols = cols[2:]

            logprobs_emission = cols2logprobs_emission(count_cols)

            info[species] = (resourcename, logprobs_emission)

    with open(OUTPUT_FILENAME, "wb") as outfile:
        dump(info, outfile, PICKLE_PROTOCOL)

def parse_options(args):
    from optparse import OptionParser

    usage = "%prog [OPTION]... [FILE]"
    version = "%%prog %s" % __version__
    parser = OptionParser(usage=usage, version=version)

    options, args = parser.parse_args(args)

    if not len(args) <= 1:
        parser.print_usage()
        sys.exit(1)

    return options, args

def main(args=sys.argv[1:]):
    options, args = parse_options(args)

    return make_species_info(*args)

if __name__ == "__main__":
    sys.exit(main())
