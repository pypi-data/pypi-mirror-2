#!/usr/bin/env python
from __future__ import division, with_statement

"""
coop: adds and parameterizes cooperativity states between 
transcription factor "petals"
"""

__version__ = "$Revision: 428 $"

# Copyright 2007 Michael M. Hoffman <hoffman+software@ebi.ac.uk>

from collections import defaultdict
import sys

from numpy import NINF, array, float64, log as alog, exp as aexp
from math import log, exp

from ._utils import DESC
from .hmm import (SPECIAL_STATE_NAMES, OFFSET_UNBOUND, OFFSET_SILENT,
                  LEN_ALPHABET, TF_START_FINAL_SUFFIXES,
                  get_state_names, get_tf_info, get_transitions, 
                  adjust_transitions, get_emissions, adjust_emissions,
                  fill_array, optimize, load, save, dump)

def load_priors(filename):

    strength_priors = {}
    distance_priors = {}
    state_offsets = {}
    coop_state_names = list()

    ## read the file - must be in the form TF1 TF2 P(TF1->TF2) P(COOP->COOP)
    ## assumes symmetric cooperativity
    state_offset = 0
    with open(filename) as infile:
        for line in infile:
            tokens = line.split()
            if len(tokens) == 4:

                tf1 = tokens[0]
                tf2 = tokens[1]
                strength = float(tokens[2])
                distance = float(tokens[3])

                assert strength < 1
                assert distance < 1

                ## there are generally not going to be huge numbers of
                ## TFs involved so it's ok (for now) to duplicate the work 
                ## for self-coop (tf1 == tf2) states
                if tf1 not in strength_priors:
                    strength_priors[tf1] = {}
                    distance_priors[tf1] = {}
                    state_offsets[tf1] = {}

                if tf2 not in strength_priors:
                    strength_priors[tf2] = {}
                    distance_priors[tf2] = {}
                    state_offsets[tf2] = {}

                strength_priors[tf1][tf2] = strength
                strength_priors[tf2][tf1] = strength

                distance_priors[tf1][tf2] = distance
                distance_priors[tf2][tf1] = distance

                ## XXX: very important that there is no duplication in the
                ## input state pairs - not sure how best to check this
                if tf1 == tf2:
                    coop_state_names.append("COOP.%s.%s" % (tf1, tf1))
                    state_offsets[tf1][tf1] = state_offset
                    state_offset += 1

                else:
                    coop_state_names.append("COOP.%s.%s" % (tf1, tf2))
                    state_offsets[tf1][tf2] = state_offset
                    state_offset += 1

                    coop_state_names.append("COOP.%s.%s" % (tf2, tf1))
                    state_offsets[tf2][tf1] = state_offset
                    state_offset += 1
 
    return (strength_priors, distance_priors, coop_state_names, state_offsets)

def add_coop(model, filename):

    ## read the coop priors
    (strength_priors, distance_priors, coop_state_names, \
         coop_state_offsets) = load_priors(filename)

    ## get the tf information and matrices
    state_names = get_state_names(model)
    (tf_start_offsets, tf_end_offsets, revcom) = get_tf_info(model)
    logprobs_a_old = get_transitions(model)
    logprobs_e_old = get_emissions(model)

    ## map tf names to start offsets and end offsets
    ## (works for both fwdonly and revcom)
    tf_to_start_offsets = {}
    tf_to_end_offsets = {}
    for tf_start_offset,tf_end_offset in zip(tf_start_offsets,tf_end_offsets):
        
        last_dot = state_names[tf_start_offset].rindex(".")
        tf_name = state_names[tf_start_offset][:last_dot]

        if tf_name not in tf_to_start_offsets:
            tf_to_start_offsets[tf_name] = list()
            tf_to_end_offsets[tf_name] = list()

        tf_to_start_offsets[tf_name].append(tf_start_offset)
        tf_to_end_offsets[tf_name].append(tf_end_offset)

    ## append the coop state names
    num_states_orig = len(state_names)
    state_names.extend(coop_state_names)
    num_states = len(state_names)

    ## reshape the transition and emissions matrices
    ## XXX: RAM usage doubles here. logprobs_a needs to be a more efficient
    ## data structure since it is sparse
    ## XXX: use resize() here?
    logprobs_a = fill_array(NINF, (num_states, num_states))
    logprobs_e = fill_array(NINF, (num_states, LEN_ALPHABET))

    logprobs_a_old_shape = logprobs_a_old.shape
    logprobs_e_old_shape = logprobs_e_old.shape

    logprobs_a[:logprobs_a_old_shape[0], :logprobs_a_old_shape[1]] = \
        logprobs_a_old
    logprobs_e[:logprobs_e_old_shape[0], :logprobs_e_old_shape[1]] = \
        logprobs_e_old

    ## update transitions
    for tf1 in coop_state_offsets:

        ## transitions for tf1 -> coop.tf1.tf2, coop.tf1.tf2 -> self,
        ## coop.tf1.tf2 -> tf2
        total_tf1_out = 0
        for tf2 in coop_state_offsets[tf1]:

            coop_state_offset = coop_state_offsets[tf1][tf2] + num_states_orig
            strength = strength_priors[tf1][tf2]
            distance = distance_priors[tf1][tf2]

            ## tf1 -> coop.tf1.tf2
            for tf1_end_offset in tf_to_end_offsets[tf1]:
                logprobs_a[tf1_end_offset, coop_state_offset] = log(strength)

            total_tf1_out += strength

            ## coop.tf1.tf2 -> coop.tf1.tf2
            logprobs_a[coop_state_offset, coop_state_offset] = log(distance)

            ## coop.tf1.tf2 -> tf2
            for tf2_start_offset in tf_to_start_offsets[tf2]:
                
                if revcom:
                    logprobs_a[coop_state_offset, tf2_start_offset] = log((1 - distance) / 2)
                else:
                    logprobs_a[coop_state_offset, tf2_start_offset] = log(1 - distance)

        assert total_tf1_out < 1

        ## tf1 -> silent
        for tf1_end_offset in tf_to_end_offsets[tf1]:
            logprobs_a[tf1_end_offset, OFFSET_SILENT] = log(1 - total_tf1_out)

    ## update emissions - for coop it is the same as unbound
    for tf1 in coop_state_offsets:
        for tf2 in coop_state_offsets[tf1]:
            coop_state_offset = coop_state_offsets[tf1][tf2] + num_states_orig
            logprobs_e[coop_state_offset] = logprobs_e[OFFSET_UNBOUND]

    return (logprobs_a, logprobs_e)

def transition_debug(logprobs_a, tf_start_offsets, tf_end_offsets, \
                         coop_state_offsets, num_states_orig):

    ## DEBUG: print only interesting transitions
    logprobs_ae = aexp(logprobs_a)
    all_offsets = list()
    all_offsets.append(OFFSET_SILENT)
    all_offsets.append(OFFSET_UNBOUND)
    for start,end in zip(tf_start_offsets, tf_end_offsets):
        all_offsets.append(start)
        all_offsets.append(end)
    for tf1 in coop_state_offsets:
        for tf2 in coop_state_offsets:
            all_offsets.append(coop_state_offsets[tf1][tf2] + num_states_orig)

    print all_offsets

    for i in all_offsets:
        for j in all_offsets:
            print "%0.4f" % logprobs_ae[i,j],
        print

def coop(priors_filename, infilename, outfilename, resource=False):

    model = load(infilename, resource)
    (logprobs_a, logprobs_e) = add_coop(model, priors_filename)

    adjust_transitions(model, logprobs_a)
    adjust_emissions(model, logprobs_e)
    model["desc"] = "; ".join([model["desc"], DESC])

    optimize(model)
    save(outfilename, model)

def parse_options(args):
    from optparse import OptionParser

    usage = "%prog [OPTION]... COOP-PRIORS IN-SFL OUT-SFL"
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

    return coop(resource=options.resource, *args)

if __name__ == "__main__":
    sys.exit(main())
