#!/usr/bin/env python
from __future__ import division, with_statement

"""
factorizers: break arrays up into factors
"""

__version__ = "$Revision: 457 $"

# Copyright 2007 Michael M. Hoffman <hoffman+software@ebi.ac.uk>

import csv
import sys

from numpy import (arange, array, empty, identity, isfinite, isnan, isneginf,
                   newaxis, ones, zeros)
import tabdelim # register unix-tab

from ._utils import FastaIterator, enum, progress
from .hmm import ALPHABET, ALPHABET_INT, LEN_ALPHABET

FACTOR_NAME_DEFAULT = "all"

LABELS_ALN = ["observed", "unobserved",
              "ambiguous", "insertion", "unaligned", "error"]
LABELS_CONS = ["conserved", "substitution"] + LABELS_ALN[2:]
LABELS_SUBS_ONLY = ["substitution/observed", "substitution/unobserved"]
LABELS_ALIGNED_ONLY = ["observed", "aligned"]

LEN_LABELS_ALN = len(LABELS_ALN)
LEN_LABELS_SUBS_ONLY = len(LABELS_SUBS_ONLY)
LEN_LABELS_ALIGNED_ONLY = len(LABELS_ALIGNED_ONLY)

LABELS_ALN_ENUM = enum(LABELS_ALN)
LABEL_ALN_OBS = LABELS_ALN_ENUM["observed"]
LABEL_ALN_UNOBS = LABELS_ALN_ENUM["unobserved"]
LABEL_ALN_UNALIGNED = LABELS_ALN_ENUM["unaligned"]

LABELS_SUBS_ONLY_ENUM = enum(LABELS_SUBS_ONLY)
LABEL_SUB_OBS = LABELS_SUBS_ONLY_ENUM["substitution/observed"]
LABEL_SUB_UNOBS = LABELS_SUBS_ONLY_ENUM["substitution/unobserved"]

LABELS_ALIGNED_ONLY_ENUM = enum(LABELS_ALIGNED_ONLY)
LABEL_ALIGNED_ONLY_OBS = LABELS_ALIGNED_ONLY_ENUM["observed"]
LABEL_ALIGNED_ONLY_ALIGNED = LABELS_ALIGNED_ONLY_ENUM["aligned"]

GAPPED_ALPHABET = ALPHABET + "N-.!"
LEN_GAPPED_ALPHABET = len(GAPPED_ALPHABET)
GAPPED_ALPHABET_ENUM = enum(GAPPED_ALPHABET)

GAPPED_ALPHABET2LABELS_ALN = [("N", "ambiguous"), ("-", "insertion"),
                              (".", "unaligned"), ("!", "error")]

IDENTITY_ALPHABET = identity(LEN_ALPHABET, bool)
SLICE_ALPHABET = slice(0, LEN_ALPHABET)

def gapped_seq2int(seq):
    res = [GAPPED_ALPHABET_ENUM[char] for char in seq.upper()]
    return array(res)

def load_seqs(filename):
    progress("loading sequences from %s..." % filename)
    with open(filename) as seqfile:
        iterator = FastaIterator(seqfile)
        res = dict((defline.partition(" ")[0], seq)
                   for defline, seq in iterator)

        progress("  done")
        return res

class Factorizer(object):
    """
    abstract base class: add an outer dimension to transcript_array
    for a factor
    """

    labels = NotImplemented

    def __getitem__(self, index):
        return self.labels[index]

    def __iter__(self):
        return iter(self.labels)

    def __call__(self, inarray):
        raise NotImplementedError

    def _init_res(self, inarray):
        inarray_shape = inarray.shape
        shape = (len(self.labels),) + inarray_shape
        dtype = inarray.atom.dtype

        return zeros(shape, dtype)

    def factor_arrays(self, inarrays):
        for inarray_index, inarray in enumerate(inarrays):
            name = inarray.name

            if not inarray_index % 10:
                progress(" %5d: %s", inarray_index, name)

            yield name, self(inarray), inarray.attrs


class TabdelimFactorizer(Factorizer):
    def __init__(self, filename):
        with open(filename) as tabfile:
            reader = csv.reader(tabfile, dialect="unix-tab")
            name2label = dict(reader)

        labels = list(sorted(set(name2label.itervalues())))
        # labels += "error"
        factor_enum = enum(labels)

        self.labels = labels
        self.name2factor = dict((name, factor_enum[label])
                                for name, label in name2label.iteritems())

    def __call__(self, inarray):
        res = self._init_res(inarray)

        factor = self.name2factor[inarray.name]
        res[factor] = inarray.read()

        return res


class AlignmentFactorizer(Factorizer):
    def __init__(self, filename):
        self.seqs = load_seqs(filename)

    def _init_res(self, inarray):
        res = Factorizer._init_res(self, inarray)

        try:
            seq = self.seqs[inarray.name]
        except KeyError:
            return res, None

        if res.shape[1] != len(seq):
            raise ValueError("length of alignment does not match that of sequence")

        seq_array = gapped_seq2int(seq)

        return res, seq_array


class ByNucleotideAlignmentFactorizer(AlignmentFactorizer):
    labels = LABELS_ALN

    def __init__(self, *args, **kwargs):
        AlignmentFactorizer.__init__(self, *args, **kwargs)

        mask = zeros((LEN_GAPPED_ALPHABET, LEN_LABELS_ALN, LEN_ALPHABET), bool)

        for gapped_letter, label_aln in GAPPED_ALPHABET2LABELS_ALN:
            gapped_alphabet_id = GAPPED_ALPHABET_ENUM[gapped_letter]
            label_aln_id = LABELS_ALN_ENUM[label_aln]

            mask[gapped_alphabet_id, label_aln_id] = True

        mask[SLICE_ALPHABET, LABEL_ALN_OBS] = IDENTITY_ALPHABET
        mask[SLICE_ALPHABET, LABEL_ALN_UNOBS] = ~IDENTITY_ALPHABET

        self.mask = mask

    def __call__(self, inarray):
        res, seq_array = self._init_res(inarray)

        if seq_array is None:
            res[LABEL_ALN_UNALIGNED] = inarray.read()
            return res

        where = self.mask[seq_array].transpose(1, 0, 2)
        res[where] = array([inarray.read()] * LEN_LABELS_ALN)[where]

        return res


class AlignedOnlyAlignmentFactorizer(AlignmentFactorizer):
    labels = LABELS_ALIGNED_ONLY

    def __init__(self, *args, **kwargs):
        AlignmentFactorizer.__init__(self, *args, **kwargs)

        shape = (LEN_GAPPED_ALPHABET, LEN_LABELS_ALIGNED_ONLY, LEN_ALPHABET)
        mask = zeros(shape, bool)

        mask[SLICE_ALPHABET, LABEL_ALIGNED_ONLY_OBS] = IDENTITY_ALPHABET
        mask[SLICE_ALPHABET, LABEL_ALIGNED_ONLY_ALIGNED] = True

        self.mask = mask

    def __call__(self, inarray):
        res, seq_array = self._init_res(inarray)

        if seq_array is None:
            return res

        where = self.mask[seq_array].transpose(1, 0, 2)
        res[where] = array([inarray.read()] * LEN_LABELS_ALIGNED_ONLY)[where]

        return res

def make_mask_bypos_alignment():
    # this is a different kind of mask
    # transforms a pair into something from LABELS_CONS

    # default: substitution
    res = ones((LEN_GAPPED_ALPHABET, LEN_GAPPED_ALPHABET), int)

    for nucleotide in ALPHABET_INT:
        res[nucleotide, nucleotide] = LABEL_ALN_OBS

    for gapped_letter, label_aln in GAPPED_ALPHABET2LABELS_ALN:
        gapped_alphabet_id = GAPPED_ALPHABET_ENUM[gapped_letter]
        label_cons_id = LABELS_ALN_ENUM[label_aln]

        res[gapped_alphabet_id, :] = label_cons_id
        res[:, gapped_alphabet_id] = label_cons_id

    return res

class ByPosAlignmentFactorizer(AlignmentFactorizer):
    labels = LABELS_CONS

    def __init__(self, *args, **kwargs):
        AlignmentFactorizer.__init__(self, *args, **kwargs)

        self.mask = make_mask_bypos_alignment()

    def __call__(self, inarray):
        res, seq_array = self._init_res(inarray)

        if seq_array is None:
            res[LABEL_ALN_UNALIGNED] = inarray.read()
            return res

        ref_array = gapped_seq2int(inarray.attrs.seq)

        where = self.mask[ref_array, seq_array]
        res[where, arange(inarray.shape[0])] = inarray.read()

        return res


class SubsOnlyAlignmentFactorizer(AlignmentFactorizer):
    labels = LABELS_SUBS_ONLY

    def __init__(self, *args, **kwargs):
        AlignmentFactorizer.__init__(self, *args, **kwargs)

        # (ref_seq, align_seq, label, mutation)
        shape = (LEN_GAPPED_ALPHABET, LEN_GAPPED_ALPHABET,
                 LEN_LABELS_SUBS_ONLY, LEN_ALPHABET)
        mask = zeros(shape, bool)

        for ref_nucleotide in ALPHABET_INT:
            for align_nucleotide in ALPHABET_INT:
                if ref_nucleotide == align_nucleotide:
                    continue

                submask = mask[ref_nucleotide, align_nucleotide]

                for mutation_nucleotide in ALPHABET_INT:
                    if mutation_nucleotide == align_nucleotide:
                        submask[LABEL_SUB_OBS, mutation_nucleotide] = True
                    else:
                        submask[LABEL_SUB_UNOBS, mutation_nucleotide] = True

        self.mask = mask

    def __call__(self, inarray):
        res, seq_array = self._init_res(inarray)
        ref_array = gapped_seq2int(inarray.attrs.seq)

        where = self.mask[ref_array, seq_array].transpose(1, 0, 2)
        res[where] = array([inarray.read()] * LEN_LABELS_SUBS_ONLY)[where]

        return res


class NullFactorizer(Factorizer):
    def __init__(self, name=FACTOR_NAME_DEFAULT):
        self.labels = [name]

    def __call__(self, inarray):
        res = self._init_res(inarray)
        res[0] = inarray.read()

        return res

# this will deal with zeros correctly as long as you do sums and
# divisors separately
def calc_total_datacol(addend_array, methodname="sum"):
    return getattr(addend_array, methodname)(-1)[..., newaxis]

def add_total(addend_array, methodname="sum"):
    "add an additional row at the end for total"
    orig_shape = addend_array.shape
    shape = list(orig_shape)
    shape[-1] = 1

    res = empty(shape, addend_array.dtype)
    res[..., :orig_shape[-1]] = addend_array
    res[..., -1] = getattr(addend_array, methodname)(-1)

    return res

def fmt_float(number):
    """
    NaN -> "NA"
    inf -> "Inf"
    """
    number = float(number)

    if isfinite(number):
        return str(number)

    if isnan(number):
        return "NA"

    if isneginf(number):
        return "-Inf"

    return "Inf"

def choose_factorizer(options):
    # XXX: allow stacking of factors
    opt_alignment = options.alignment
    if opt_alignment:
        return options.alignment_factorizer(opt_alignment)
    elif options.tab_delim:
        return TabdelimFactorizer(options.tab_delim)
    else:
        return NullFactorizer()

def main(args=sys.argv[1:]):
    pass

if __name__ == "__main__":
    sys.exit(main())

if __debug__:
    __pychecker__ = "no-returnvalues unusednames=tabdelim"
