============
 To-do list
============

Roadmap
=======
RELEASE
- pwm2sfl back to basics

RELEASE
- develop new model datastructure

Other
=====
- misc fixes
  - move ALPHABET_ENUM to sunflower.hmm

- model
  - use HDF5 to store SFL files instead of pickle
  - add version counter to file format
  - make OO

- pwm2sfl
  - start requiring output filename
  - make logprobs_transition matrix unnecessary
  - allow specification of probs_transition separately
  - deal with Ns/other ambiguous
  - create matrices based on filenames if there's no matrix_list.txt
  - add tissue-specific matrices
  - add TRANSFAC import (ask Matt Hestand for script)
  - cooperativity stuff goes into a driver or separate program
  - investigate shift from log space to storing exponents separately
    with new NumPy datatype
  - change model to allow starting in any state
  - add specification of ``--include`` matrices
  - fix: doesn't like extra newlines at the end

  - new model file structure
    - see e-mail to Alison
    - optimization: precompute ae values for different symbols before
      running through
    - change base of what c_f points to depending on current symbol

    for each c_{f,x_i} = c_f[x_i]:
        for each j:
            sum(f[k]*ae)

- sunscramble
  - new program

- simulator
  - add --no-poly
  - turn off assertions for speedup--use only in testing
  - profile switching npy_intp -> int (typedef)
  - clip attr.seq with array
  - implement ``--range`` for mutate mode
  - make HDF5 output compressable, using appropriate Lustre chunksize
  - drop-off heuristics
    * start with graph of how change trails off as position increasing
    * compare dropoff with machine epsilon
  - add way to deal with Ns in sequence
  - add file-wide stats: start, shape, measurement, min, max, mean, n; then
    announce deprecation of previous sunreport
  - add driver ``sunreport``
  - add driver list option
  - allow specification of per-nucleotide prior emission probs
  - summarize relative entropy only of starting/ending states

- h5cat
  - propagate file-wide stats if they are consistent

- report
  - throw an error when running sunreport on --diff mode results
  - check that --no-total is working
  - refactor output code into a recordarray
  - start including tf and dir columns instead of state
  - start using file-wide stats (new point release)
  - SQL output
  - .wig output
  - HDF5 output
  - allow multiple length sequences in non-average mode
    (check that stats_seq can be a heterogeneous iterator)

- sundot
  - produce graphs of sunflower models

- deployment
  - why isn't tables being automatically downloaded without specifying URL?
  - move call_inner to C
  - address Pyrex warnings
  - fix install not installing numpy issue, but keep my workaround
    from automatically installing even on --help (see Phillip J. Eby's
    suggestions on Gmane)
  - try to get other upstream stuff fixed
    - ask Cygwin to include INFINITY (now defined in newlib)

- local deployment
  - EBI
    - make a local install/source file and announce

- tests
  - need some unit tests

- doc
  - add descriptions to command-line programs (use optparse)
  - produce docutils output

- R
  - make an R package
    - add as a project in the repos root
    - remember configure.args when installing hdf5

- XXX notes
- XXXopt notes

Notes
=====
NumPy 1.0.3.1 contains bug fixes that we probably don't need to require.

Documentation
=============
* add workflow/file block diagram
