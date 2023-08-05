#!/usr/bin/env python
from __future__ import division, with_statement

"""
priors: alters the prior probabilities of transitions from the
silent state to various transcription factor "petals"
"""

__version__ = "$Revision: 428 $"

# Copyright 2007 Michael M. Hoffman <hoffman+software@ebi.ac.uk>

from collections import defaultdict
import sys

from numpy import array, float64, log as alog
from math import log, exp

from ._utils import DESC
from .hmm import (SPECIAL_STATE_NAMES, OFFSET_UNBOUND, OFFSET_SILENT,
                  TF_START_FINAL_SUFFIXES,
                  get_state_names, get_tf_info, get_transitions, 
                  adjust_transitions, load, save, dump)

def load_priors(filename):

    priors = {}

    ## read the file - must be in the form TF prior
    with open(filename) as infile:
        for line in infile:
            tokens = line.split()
            if len(tokens) == 2:
                priors[tokens[0]] = float(tokens[1])

    ## check that the unbound prior was set
    assert SPECIAL_STATE_NAMES[OFFSET_UNBOUND] in priors

    ## check that priors sum to 1 - if not, scale them
    total = sum(priors.values())
    if total != 1.0:
        # XXX: vectorize
        for key in priors.keys():
            priors[key] = priors[key] / total

    return priors

def update_priors(model, priors):

    state_names = get_state_names(model)
    (tf_start_offsets, tf_end_offsets, revcom) = get_tf_info(model)
    logprobs_a = get_transitions(model)

    ## map tf names to start offsets (works for both fwdonly and revcom)
    tf_to_start_offsets = {}
    for tf_start_offset in tf_start_offsets:
        
        last_dot = state_names[tf_start_offset].rindex(".")
        tf_name = state_names[tf_start_offset][:last_dot]

        if tf_name not in tf_to_start_offsets:
            tf_to_start_offsets[tf_name] = list()

        tf_to_start_offsets[tf_name].append(tf_start_offset)

    for tf_name in priors:

        ## unbound is a special case
        if tf_name == SPECIAL_STATE_NAMES[OFFSET_UNBOUND]:
            logprobs_a[OFFSET_SILENT, OFFSET_UNBOUND] = log(priors[tf_name])

        else:
            for tf_start_offset in tf_to_start_offsets[tf_name]:

                cell = (OFFSET_SILENT, tf_start_offset)

                if revcom:
                    logprobs_a[cell] = log(priors[tf_name] / 2)
                else:
                    logprobs_a[cell] = log(priors[tf_name])

    return logprobs_a

def priors(priors_filename, infilename, outfilename, resource=False):

    model = load(infilename, resource)
    priors = load_priors(priors_filename)

    logprobs_transition = update_priors(model, priors)

    adjust_transitions(model, logprobs_transition)
    model["desc"] = "; ".join([model["desc"], DESC])

    save(outfilename, model)

def parse_options(args):
    from optparse import OptionParser

    usage = "%prog [OPTION]... PRIORS IN-SFL OUT-SFL"
    version = "%%prog %s" % __version__
    parser = OptionParser(usage=usage, version=version)
    parser.add_option("-R", "--resource", action="store_true",
                      help="get SFLFILE from a resource that comes with the "
                      "sunflower distribution instead of a file")

    options, args = parser.parse_args(args)

    if not len(args) == 3:
        parser.print_usage()
        sys.exit(1)

    return options, args

def main(args=sys.argv[1:]):

    options, args = parse_options(args)

    return priors(resource=options.resource, *args)

if __name__ == "__main__":
    sys.exit(main())
