#!/usr/bin/env python
from __future__ import division

"""
composition: take composition into account

requires output from fastacomposition, from the exonerate package
"""

__version__ = "$Revision: 425 $"

# Copyright 2007 Michael M. Hoffman <hoffman+software@ebi.ac.uk>

from collections import defaultdict
import sys

from numpy import array, float64, log as alog

from ._utils import DESC
from .hmm import ALPHABET, adjust, load, save

PSEUDOCOUNT = 1

def add_pseudocount(n=0):
    return n + PSEUDOCOUNT

def cols2counts(cols):
    # cols = ['A', '578', 'C', '476', 'G', '485']
    # why only ACG? I'm demonstrating a corner case--it will still
    # work and will create a pseudocount for T

    labels = cols[::2]

    count_generator = (add_pseudocount(int(col)) for col in cols[1::2])

    # counts["X"] where X was previously undefined returns the pseudocount
    counts = defaultdict(add_pseudocount, zip(labels, count_generator))

    return array([counts[letter] for letter in ALPHABET])

def load_fastacomposition(filename):
    # examples:
    # line = "test.fna A 578 C 476 G 485"
    line = iter(open(filename)).next()

    # cols = ['test.fna', 'A', '578', 'C', '476', 'G', '485']
    return line.rstrip().split()[1:]

def calc_logprobs_emission(counts):
    counts_float = array(counts, dtype=float64)

    return alog(counts_float / counts.sum())

def cols2logprobs_emission(cols):
    return calc_logprobs_emission(cols2counts(cols))

def recompose(composition_filename, infilename, outfilename, resource=False):
    cols = load_fastacomposition(composition_filename)
    logprobs_emission = cols2logprobs_emission(cols)

    model = load(infilename, resource)
    adjust(model, logprobs_emission)
    model["desc"] = "; ".join([model["desc"], DESC])

    save(outfilename, model)

def parse_options(args):
    from optparse import OptionParser

    usage = "%prog [OPTION]... FASTACOMPOSITION IN-SFL OUT-SFL"
    version = "%%prog %s" % __version__
    parser = OptionParser(usage=usage, version=version)
    parser.add_option("-R", "--resource", action="store_true",
                      help="get IN-SFL from a resource that comes with the "
                      "Sunflower distribution instead of a file")

    options, args = parser.parse_args(args)

    if not len(args) == 3:
        parser.print_usage()
        sys.exit(1)

    return options, args

def main(args=sys.argv[1:]):
    # XXX: allow more than two in/out pairs
    options, args = parse_options(args)

    return recompose(resource=options.resource, *args)

if __name__ == "__main__":
    sys.exit(main())
