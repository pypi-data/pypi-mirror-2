#!/usr/bin/env python
from __future__ import division, with_statement

"""
report: aggregate by sequence or position
"""

__version__ = "$Revision: 457 $"

# Copyright 2007 Michael M. Hoffman <hoffman+software@ebi.ac.uk>

import csv
from itertools import izip, repeat
import sys

from numpy import (NINF, PINF, array, errstate, finfo, histogram,
                   linspace, log1p, minimum, maximum, ndindex, newaxis,
                   rollaxis, square, sqrt as asqrt, zeros)
import tabdelim # for side-effect: dialect="unix-tab"

from ._utils import correct_range, enum, progress
from .hdf5 import h5open, walk_included_nodes, walk_nodes
from .factorizers import (AlignedOnlyAlignmentFactorizer,
                          ByNucleotideAlignmentFactorizer,
                          ByPosAlignmentFactorizer,
                          LABEL_ALIGNED_ONLY_ALIGNED, LABEL_ALIGNED_ONLY_OBS,
                          SubsOnlyAlignmentFactorizer, choose_factorizer,
                          fmt_float, calc_total_datacol)

FIELDNAMES = ["seqname", "factor", "datacol", "pos", "measurement",
              "sd", "min", "max", "n", "T", "T_d", "d_T"]

# layout of stats before transposition:
# stat: (mean, sd, min, max, n)
# datacol: state (reference mode) or nucleotide (mutate mode)

AXES_ENUM = enum(["seq", "stat", "factor", "pos", "datacol"])
AXIS_SEQ = AXES_ENUM["seq"]
AXIS_STAT = AXES_ENUM["stat"]
AXIS_FACTOR = AXES_ENUM["factor"]
AXIS_POS = AXES_ENUM["pos"]
AXIS_DATACOL = AXES_ENUM["datacol"]

STAT_OFFSET_ENUM = enum(["mean", "sd", "min", "max", "n"])
STAT_OFFSET_MEAN = STAT_OFFSET_ENUM["mean"]
STAT_OFFSET_N = STAT_OFFSET_ENUM["n"]

NUM_BINS_DEFAULT = 100

def distance_jc69(p):
    """calculate Jukes and Cantor 1969 distances"""
    return -0.75*log1p((-4/3)*p)

def calc_total_ranges(addend_array, ranges, methodname="sum"):
    totals = [getattr(addend_array[:, r], methodname)(1) for r in ranges]

    res = array(totals) # axes = (range, factor, datacol)
    return res.transpose(1, 0, 2) # axes = (factor, range, datacol)

def correct_ranges(ranges, start):
    return [correct_range(r, start) for r in ranges]

def calc_total(addend_array, ranges, total_datacol, methodname="sum"):
    if ranges:
        addend_array = calc_total_ranges(addend_array, ranges, methodname)
    if total_datacol:
        addend_array = calc_total_datacol(addend_array, methodname)

    return addend_array

class ArrayRecordList(list):
    """dummy list subclass to allow setting of attributes"""

class FactorizedArrayChecker(object):
    """
    checks that shape and start are consistent
    """
    def __init__(self, arrays):
        self.arrays = arrays

    def __iter__(self):
        shape = None

        for seqname, transcript_array, attrs in self.arrays:
            if shape is None:
                shape = transcript_array.shape
                self.shape = shape

                start = attrs.start
                self.start = start

                # ensure that there are no extra columns for various
                # measurements--unsupported
                assert len(shape) == 3
            else:
                assert shape == transcript_array.shape
                assert start == attrs.start

            yield seqname, transcript_array

    def wrap(self, arrayrecord):
        res = ArrayRecordList([arrayrecord])
        res.shape = self.shape
        res.start = self.start

        return res

def histogram_arrays(factorized_arrays, ranges, total_datacol, num_bins,
                     bin_range, measurement_min):
    assert measurement_min == 0.0
    """
    overload AXIS_STAT to return different bins
    """
    start = None

    # transcript_array: (factor, pos, datacol)
    for seqname, transcript_array in factorized_arrays:
        if start is None:
            # not determined until first array is read
            start = factorized_arrays.start
            len_factor, _, len_datacol = factorized_arrays.shape
            ranges = correct_ranges(ranges, start)
            len_ranges = len(ranges)

            if total_datacol:
                len_datacol_out = 1
            else:
                len_datacol_out = len_datacol

            # (factor, bin, datacol, range) or (factor, pos, datacol, stat)
            res_shape = (len_factor, len_ranges, len_datacol_out, num_bins)
            res = zeros(res_shape, dtype=int)

        # generates (0, 0, 0) .. (n, n, n)
        for indices in ndindex(len_factor, len_ranges, len_datacol):
            r = ranges[indices[1]]
            range_array = transcript_array[indices[0], r, indices[2]]

            # _ is a common Python convention for an unused variable
            range_histogram, _ = histogram(range_array, num_bins, bin_range)

            if total_datacol:
                indices = indices[:2] + (0,)

            res[indices] += range_histogram

    # (stat, factor, pos, datacol)
    return rollaxis(res, 3, 0), start

def aggregate_arrays(factorized_arrays, ranges, total_datacol, calc_d_T,
                     measurement_min):
    # XXXopt: if you don't want min, max, sd, many calcs can be avoided.
    # But for now this is the fastest part of the program anyway.

    sums = 0.0
    square_sums = 0.0
    divisors = 0
    mins = PINF
    maxs = NINF

    for seqname, transcript_array in factorized_arrays:
        # replace zeros (or other ignored number) with +inf
        transcript_array_is_zero = transcript_array <= measurement_min
        transcript_array_zeros_replaced = transcript_array.copy()
        transcript_array_zeros_replaced[transcript_array_is_zero] = PINF

        transcript_array[transcript_array_is_zero] = 0.0 # set ignored to zero

        # accumulate statistics from transcript_array
        sums += transcript_array
        square_sums += square(transcript_array)
        divisors += ~transcript_array_is_zero
        mins = minimum(mins, transcript_array_zeros_replaced)
        maxs = maximum(maxs, transcript_array)

    # must be after start is determined
    start = factorized_arrays.start
    ranges = correct_ranges(ranges, start)

    if calc_d_T:
        T_d = sums[newaxis, LABEL_ALIGNED_ONLY_OBS]
        T = sums[newaxis, LABEL_ALIGNED_ONLY_ALIGNED]

    sums = calc_total(sums, ranges, total_datacol)
    square_sums = calc_total(square_sums, ranges, total_datacol)
    divisors = calc_total(divisors, ranges, total_datacol)
    mins = calc_total(mins, ranges, total_datacol, "min")
    maxs = calc_total(maxs, ranges, total_datacol, "max")

    # calculating t or T by using the mean implies that t_d can
    # possibly be bigger than t for a given position, but it is
    # unlikely across a whole gene at the evolutionary distances the
    # whole endeavor will work. This sort of thing can happen in NG86
    # as well; see the example in Ch. 4 of Nei and Kumar for a TGT
    # codon
    if calc_d_T:
        T_d = calc_total(T_d, ranges, total_datacol)
        T = calc_total(T, ranges, total_datacol)
        if total_datacol:
            assert measurement_min == 0.0 # dividing by 3.0 won't work here
            T /= 3.0 # the mean of the three possible changes

    with errstate(invalid="ignore"):
        means = sums / divisors
        sds = calc_sd(sums, square_sums, divisors)

        if calc_d_T:
            p_T = T_d / T
            d_T = distance_jc69(p_T)

    if calc_d_T:
        res = [T, T_d, d_T]
    else:
        res = [means, sds, mins, maxs, divisors]

    # (stat, factor, pos, datacol)
    return array(res), start

def process_arrays(factorized_arrays, ranges, total_datacol, calc_d_T,
                   num_bins, bin_range, measurement_min):
    if num_bins:
        return histogram_arrays(factorized_arrays, ranges, total_datacol,
                                num_bins, bin_range, measurement_min)
    else:
        return aggregate_arrays(factorized_arrays, ranges, total_datacol,
                                calc_d_T, measurement_min)

def calc_stats_sequential(factorized_arrays, *args, **kwargs):
    seqnames = []
    starts = []
    stats_list = []

    for arrayrecord in factorized_arrays:
        seqname = arrayrecord[0]
        seqnames.append(seqname)

        wrapped_arrayrecord = factorized_arrays.wrap(arrayrecord)
        stats_seq, start = process_arrays(wrapped_arrayrecord, *args, **kwargs)
        stats_list.append(stats_seq)
        starts.append(start)

    return seqnames, starts, array(stats_list)

def calc_stats_aggregate(factorized_arrays, *args, **kwargs):
    seqnames = ["all"]
    stats_mean, start = process_arrays(factorized_arrays, *args, **kwargs)

    return seqnames, [start], array([stats_mean])

def calc_sd(sums, square_sums, divisors):
    # this will always give sample sd
    # maybe we should use population sd if no subset is specified?
    numerator = square_sums - (square(sums) / divisors)
    denominator = divisors - 1

    return asqrt(numerator / denominator)

def find_max(inarrays):
    res = NINF

    for inarray_index, inarray in enumerate(inarrays):
        if not inarray_index % 10:
            progress(" %5d", inarray_index)

        res = max(res, inarray.read().max())

    return res

def aggregate_filenames(h5filenames, factorizer, aggregate_func,
                        include_names, ranges, total_datacol, calc_d_T,
                        num_bins, hist_max, measurement_min):
    # XXX: make a generator to add arrays in additional filenames to inarrays
    assert len(h5filenames) == 1
    h5filename = h5filenames[0]

    with h5open(h5filename) as h5file:
        # XXX: start getting these from new file-wide attrs
        first_array = walk_included_nodes(h5file, include_names).next()
        first_attrs = first_array.attrs
        measurement = first_attrs.measurement
        if total_datacol:
            datacolnames = ["all"]
        else:
            datacolnames = list(first_attrs.colnames)

        if num_bins:
            # smallest magnitude usable number (to exclude zeros)
            tiny = finfo(first_array.read().dtype).tiny

            if hist_max is None:
                hist_max = find_max(walk_nodes(h5file))

            bin_range = (tiny, hist_max)
        else:
            bin_range = None

        inarrays = walk_included_nodes(h5file, include_names)
        factorized_arrays = factorizer.factor_arrays(inarrays)
        checked_factorized_arrays = FactorizedArrayChecker(factorized_arrays)

        # XXXopt: add a thread to start reading in inarrays ahead of time to
        #         ease I/O bottleneck
        seqnames, starts, stats = \
            aggregate_func(checked_factorized_arrays, ranges, total_datacol,
                           calc_d_T, num_bins, bin_range, measurement_min)

    return stats, measurement, datacolnames, seqnames, starts, bin_range

def write_header(writer, fieldnames, measurement):
    row = fieldnames[:]

    try:
        row[row.index("measurement")] = measurement
    except ValueError:
        pass

    try:
        if measurement == "prob":
            row[row.index("datacol")] = "state"
        else:
            row[row.index("datacol")] = "mutation"
    except ValueError:
        pass # no datacol column

    writer.writerow(row)

def make_fieldnames(stats, all_columns, calc_d_T, num_bins):
    fieldnames = FIELDNAMES[:]

    if not all_columns:
        shape = stats.shape

        if shape[AXIS_SEQ] == 1:
            fieldnames.remove("seqname")

        if shape[AXIS_FACTOR] == 1:
            fieldnames.remove("factor")

        if shape[AXIS_DATACOL] == 1:
            fieldnames.remove("datacol")

        if calc_d_T:
            fieldnames.remove("measurement")
        else:
            fieldnames.remove("T")
            fieldnames.remove("T_d")
            fieldnames.remove("d_T")

        if calc_d_T or num_bins or (stats[:, STAT_OFFSET_N] <= 1.0).all():
            fieldnames.remove("sd")
            fieldnames.remove("min")
            fieldnames.remove("max")

            if not num_bins:
                fieldnames.remove("n")

    return fieldnames

def slice_value2str(num):
    if num is None:
        return ""

    return str(num)

def range2str(r):
    if isinstance(r, slice):
        vals = [r.start, r.stop]
        if r.step is not None:
            vals.append(r.step)

        return ":".join(map(slice_value2str, vals))
    else:
        return str(r)

# XXX: too many arguments
def report(h5filenames, factorizer, aggregate_func, start_override=None,
           include_names=None, ranges=[], all_columns=False,
           total_datacol=False, calc_d_T=False, num_bins=None, hist_max=None,
           measurement_min=0.0):
    assert not (calc_d_T and num_bins)

    stats, measurement, datacolnames, seqnames, starts, bin_range = \
        aggregate_filenames(h5filenames, factorizer, aggregate_func,
                            include_names, ranges, total_datacol, calc_d_T,
                            num_bins, hist_max, measurement_min)

    if ranges:
        range_strs = [range2str(r) for r in ranges]
        start_override = True

    if num_bins:
        bin_edges = linspace(bin_range[0], bin_range[1], num_bins+1)
        bin_starts = bin_edges[:-1]

    if start_override:
        starts = repeat(start_override)

    fieldnames = make_fieldnames(stats, all_columns, calc_d_T, num_bins)
    fieldname_set = frozenset(fieldnames)

    writer = csv.writer(sys.stdout, dialect="unix-tab")
    write_header(writer, fieldnames, measurement)

    stats_transposed = stats.transpose(AXIS_SEQ, AXIS_FACTOR, AXIS_DATACOL,
                                       AXIS_POS, AXIS_STAT)

    seq_zipper = izip(seqnames, starts, stats_transposed)
    for seqname, start, stats_seq in seq_zipper:
        # arrays should be homogeneous from this point down

        # XXX: spaghetti code ahoy!
        # instead, make a recordarray and adjust in memory
        for factor_label, stats_factor in izip(factorizer, stats_seq):
            # izip() won't produce overlap
            for datacolname, stats_datacol in izip(datacolnames, stats_factor):
                for pos_raw, stats_pos in enumerate(stats_datacol):
                    if ranges:
                        pos = range_strs[pos_raw]
                    else:
                        pos = str(pos_raw + start)

                    if not (calc_d_T or num_bins):
                        pos_mean, pos_sd, pos_min, pos_max, pos_n = stats_pos

                        if pos_n == 0.0:
                            continue

                    outrow = []
                    if "seqname" in fieldname_set:
                        outrow.append(seqname)
                    if "factor" in fieldname_set:
                        outrow.append(factor_label)
                    if "datacol" in fieldname_set:
                        outrow.append(datacolname)

                    outrow.append(pos)

                    if calc_d_T:
                        outrow.extend(map(fmt_float, stats_pos))
                    elif num_bins:
                        # stats_pos is overloaded for bins
                        for bin_index, bin in enumerate(stats_pos):
                            outrow_bin = outrow[:]
                            outrow_bin.append(bin_starts[bin_index])
                            outrow_bin.append(bin)

                            writer.writerow(outrow_bin)

                        continue # don't write outrow again
                    else:
                        outrow.append(fmt_float(pos_mean))

                        if "sd" in fieldname_set:
                            cols = map(fmt_float, [pos_sd, pos_min, pos_max])
                            outrow.extend(cols)
                        if "n" in fieldname_set:
                            outrow.append("%d" % pos_n)

                    writer.writerow(outrow)

def parse_options(args):
    from ._optparse import OptionGroup, OptionParser

    usage = "%prog [OPTION]... FILE"
    version = "%%prog %s" % __version__
    parser = OptionParser(usage=usage, version=version)

    with OptionGroup(parser, "Output control") as group:
        # XXX: eliminate this after another release
        group.add_option("-p", "--start", type=int,
                         metavar="POS",
                         help="[DEPRECATED] call the first position POS")
        group.add_option("-A", "--aggregate", action="store_const",
                         dest="aggregate_func",
                         default=calc_stats_sequential,
                         const=calc_stats_aggregate,
                         help="average results from different sequences "
                         "(sum in histogram mode)")
        group.add_option("-T", "--total", action="store_true",
                         help="total mutation or state")
        group.add_option("--no-total", action="store_false", dest="total",
                         help="report mutation or state individually")
        group.add_option("-C", "--all-columns", action="store_true",
                         help="include all columns in output, even if they are"
                         " uninformative")
        # XXX: should be an optional default value (100)
        group.add_option("-H", "--hist-bins", type=int, metavar="BINS",
                         help="output histograms of BINS bins")

    # all of these options can be included multiple times
    with OptionGroup(parser, "Specify a subset") as group:
        group.add_option("-i", "--include", action="append", dest="include",
                         metavar="ARRAY", help="report only on ARRAY")
        group.add_option("--include-from", action="load", dest="include",
                         metavar="FILE",
                         help="report only on arrays specified in FILE")

        # this will get you -50..49 == 100 positions
        group.add_option("-r", "--range", type=slice, default=[],
                         action="append", metavar="RANGE",
                         help='report only on average results for positions '
                         'RANGE in the form of "-50:50"')

        group.add_option("--hist-max", type=float, metavar="LIMIT",
                         help="calculate histogram bins in the range 0:LIMIT")

        group.add_option("--measurement-min", type=float, metavar="MIN",
                         help="only include data where measurement > MIN",
                         default=0.0)

    # XXX: UI probably a bit confusing here
    with OptionGroup(parser, "Stratification factor control") as group:
        group.add_option("-t", "--tab-delim", metavar="TABFILE",
                         help="stratify on identifiers in TABFILE")
        group.add_option("-a", "--alignment", metavar="FASTAFILE",
                         help="stratify on align slices in FASTAFILE")
        group.add_option("-d", "--distances", action="store_true",
                         help="calculate evolutionary distances")
        group.add_option("-P", "--by-position", action="store_const",
                         dest="alignment_factorizer",
                         const=ByPosAlignmentFactorizer,
                         default=ByNucleotideAlignmentFactorizer,
                         help="stratify by position; disregard nucleotide")
        group.add_option("-s", "--only-substitutions", action="store_const",
                         dest="alignment_factorizer",
                         const=SubsOnlyAlignmentFactorizer,
                         help="only include substitution positions")

    options, args = parser.parse_args(args)

    if len(args) != 1:
        parser.print_usage()
        sys.exit(1)

    if options.start and options.range:
        # XXX: allow this: if you use both, then correct_ranges in advance
        parser.error("can't use --start and --range together")

    if options.distances and options.hist_bins:
        parser.error("can't use --distances and --histogram together")

    if options.distances and not options.alignment:
        parser.error("must use --alignment when using --distances")

    if options.hist_max and not options.hist_bins:
        options.hist_bins = NUM_BINS_DEFAULT

    return options, args

def main(args=sys.argv[1:]):
    options, args = parse_options(args)

    calc_d_T = options.distances
    if calc_d_T:
        assert options.alignment

        # XXX: should eliminate the default in options, set it elsewhere
        # this means no specific option was set
        assert options.alignment_factorizer == ByNucleotideAlignmentFactorizer

        # override that
        options.alignment_factorizer = AlignedOnlyAlignmentFactorizer

    factorizer = choose_factorizer(options)
    include_names = options.include
    start_override = options.start
    aggregate_func = options.aggregate_func
    all_columns = options.all_columns
    ranges = options.range
    num_bins = options.hist_bins
    hist_max = options.hist_max
    total_datacol = options.total
    measurement_min = options.measurement_min

    # many other options are used in factorizers.py

    if num_bins and not ranges:
        ranges = [slice(None)]

    if total_datacol is None and ranges:
        total_datacol = True

    return report(args, factorizer, aggregate_func, start_override,
                  include_names, ranges, all_columns, total_datacol, calc_d_T,
                  num_bins, hist_max, measurement_min)

if __name__ == "__main__":
    sys.exit(main())

if __debug__:
    __pychecker__ = "unusednames=tabdelim"
