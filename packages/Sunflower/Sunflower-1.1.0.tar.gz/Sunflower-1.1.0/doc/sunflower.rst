=========================
 Sunflower documentation
=========================
:Author: Michael M. Hoffman <mmh1 at washington dot edu>
:Organization: University of Washington
:Address: Department of Genome Sciences, PO Box 355065, Seattle, WA 98195-5065, United States of America
:Copyright: 2009-2010 Michael M. Hoffman

.. include:: <xhtml1-symbol.txt>

For an overview of the science of Sunflower, please see the paper:

  Hoffman MM, Birney E. 2010. An effective model for natural selection
  in promoters. *Genome Res.* 20(5):685-692.
  http://genome.cshlp.org/content/20/5/685

You can also ask Michael for a copy of his PhD thesis, which explains
in more detail.

Quick start
===========
.. note: do not include indents when copying the code below:

After installation (see README), try these commands::

  sunflower --resource human test/data/brca_tss.fna brca.h5
  sunreport --include=BRCA2 brca.h5 > brca2.sunreport.tab

If you want to look at the output in R, try this::

  library(lattice)
  d.brca2 = read.delim("brca2.sunreport.tab")
  xyplot(prob ~ pos | state, d.brca2, type = "l")

The workflow
============
Typical use of Sunflower involves the following workflow:

  1. (optional) Model construction with :program:`pwm2sfl`
  2. (optional) Model recomposition with :program:`sunrecompose`
  3. Simulating transcription factor binding with :program:`sunflower`

     1. Simulating transcription factor binding to a reference
        sequence (``sunflower``)
     2. Simulating binding to two sequences and computing the distance
        between their probability distributions (``sunflower --diff``)
     3. Exhaustively simulating all possible mutations to a sequence
        and computing the distance between probability distributions
        (``sunflower --mutate``)

  4. (optional) Reporting :program:`sunflower` output with :program:`sunreport`

All of these programs have built-in help, which you can access with
their :option:`--help` options.

File extensions
---------------
The following file extensions are used by Sunflower and its component programs:

  .sfl
    Sunflower model
  .h5
    HDF5 data (such as Sunflower output)
  .pck
    Python pickle


pwm2sfl
=======
.. program:: pwm2sfl

The :program:`pwm2sfl` command converts position weight matrices (PWM) in the
ASCII format used by the JASPAR_ database into a hidden Markov model
for use within Sunflower. The model can be altered in many ways--some
of which can be done using programs in the Sunflower distribution.
Other more arbitrary alterations are outside the scope of this
document. Please note that the use of :program:`pwm2sfl` is optional, since
Sunflower has built-in models for a variety of biological data.

The only argument to :program:`pwm2sfl` specifies a directory setup in
the JASPAR format, containing PWMs. For an example directory, see the
files in
http://jaspar.genereg.net/html/DOWNLOAD/MatrixDir/JASPAR_CORE_2008.zip\ .

There are a couple of options to specify that the Sunflower model
should be made from only a subset of the PWMs in the specified
directory. The :option:`--species`\=\ *species* option specifies a
species, while the :option:`--sysgroup`\=\ *sysgroup* option specifies
a taxon such as ``vertebrate``, ``insect``, or ``plant``, according to
the index in the matrix directory. For greater control in the included
PWMs, edit the `matrix_list.txt` file.

Model parameters
----------------

There are two options to specify parameters of the model. The
:option:`--revcom` option adds an extra petal to the model for each
PWM containing its reverse complement, thereby allowing the simulation
of competitive binding and steric hindrance on both strands of DNA.
The :option:`--unbound`\=\ *prob* option sets the prior probability of
transition to the unbound state to *prob*, and the prior probability
of transitioning to the other petals to uniform portions of (1 -
*prob*). It can be used to simulate different levels of transcription
factor concentrations--setting *prob* lower means higher TF
concentrations.

Output
------

The :option:`--output`\=\ places the output Sunflower model in *file*.
The default output filename is ``jaspar.sfl``.

Usage summary
-------------

::

  Usage: pwm2sfl [OPTION...] MATRIXDIR

  Options:
    --version             show program's version number and exit
    -h, --help            show this help message and exit

    Input limiters:
      -s SPECIES, --species=SPECIES
                          include matrices marked from SPECIES
      -S SYSGROUP, --sysgroup=SYSGROUP
                          include matrices marked from SYSGROUP

    Model parameters:
      -r, --revcom        add reverse complement of all PWMs to model
      -u PROB, --unbound=PROB
                          prior probability of unbound state (default 0.9)

    Output:
      -o FILE, --output=FILE
                          output model to FILE (default jaspar.sfl)


Optimized for JASPAR directory layout.

.. _JASPAR: http://jaspar.cgb.ki.se/

sunrecompose
============
.. program:: sunrecompose

The :program:`sunrecompose` command allows you to change the emission
probabilities of the unbound state. It uses input from the
:program:`fastacomposition` command of the Exonerate_ package. Our use
patterns showed little change in results when using
:program:`sunrecompose`, so it is optional. The provided model
resources (see :ref:`sunflower-model-specification`) are adjusted
using this process, however, for maximum verisimilitude.

.. they actually do not use sunrecompose, but do the recomposition on the fly

Usage summary
-------------

::

  Usage: sunrecompose [OPTION]... FASTACOMPOSITION IN-SFL OUT-SFL

  Options:
    --version       show program's version number and exit
    -h, --help      show this help message and exit
    -R, --resource  get IN-SFL from a resource that comes with the Sunflower
                    distribution instead of a file

.. _Exonerate: http://www.ebi.ac.uk/~guy/exonerate/

sunflower
=========
.. program:: sunflower

:program:`sunflower` is the heart of the Sunflower distribution, as you might
expect from the name. It takes a DNA sequence file in Fasta format
with a model produced by :program:`pwm2sfl` to simulate the binding of
transcription factors in the model to the sequence.

Major modes
-----------

:program:`sunflower` can be run in one of three different modes, as outlined
in the workflow section above. The default mode is a simple simulation
of TF binding to the reference sequence. This stores as output the
posterior probability that a particular position is bound by a
TF.

You can also run in :option:`--diff` mode which computes the TF
binding profile for two sequences, calculating their relative
entropies as a distance. Note that the relative entropy is not a
symmetric measurement, so it matters which sequence you use as the
argument *seqfile* and which you use as part of the option
:option:`--diff`\=\ *seqfile2*. The distance is saved in the same kind
of array as reference mode results but the array has only one element
in it. The contents of *seqfile2* name a Fasta file that contains
sequences of the same length as those in *seqfile*, with definition
lines that have a common first words between the two files. For
example, if you have this in *seqfile*::

  >ENSG00000987654 EXAMPLE3 reference sequence
  ACGTACGTACGTACGT

you might have this in *seqfile2* to compare::

  >ENSG00000987654 alternate allele of EXAMPLE3 gene
  AAAAACGTACGTACGT

The :option:`--mutate` mode completes the same process but produces the
alternate sequence by mutating the reference sequence one base at a
time to exhaustively try all possible single-base mutations. The
results--the relative entropy calculation per base--are placed in an
output store much as they are for reference mode.

Distributed computing
---------------------

If you are running :program:`sunflower` on multiple sequences, and have the
Poly_ package installed, you can use a distributed computing
environment such as Platform LSF.

.. _sunflower-model-specification:

Model specification
-------------------

The first argument to :program:`sunflower` specifies the model file to
use, previously created by :program:`pwm2sfl`. If you use the
:option:`--resource` option, *model* will not be read from the local
filesystem, but instead from a built-in list of resources. There are
three core model resources which were built from the JASPAR CORE PWMs
assigned to the appropriate sysgroups (vertebrate, insect, or plant):

  * `jaspar/core/vertebrate`
  * `jaspar/core/insect`
  * `jaspar/core/plant`

Additionally, there are a number of aliases which start with one of
the models above and recompose the unbound state emission
probabilities much as :program:`sunrecompose` does:

=============  ========================  =============================================================================
Resource name  Core model                Sequences used for composition
=============  ========================  =============================================================================
`aedes`        `jaspar/core/insect`      `Aedes/aedes_1_softmasked_supercontig.fa`
`anopheles`    `jaspar/core/insect`      `Anopheles/genome/agamP3/chromosomes_agamP3_rm_dust_soft/*.fa`
`chicken`      `jaspar/core/vertebrate`  `Large/Gallus_gallus/WASHUC2/Gallus_gallus.WASHUC2.softmasked.fa`
`chimp`        `jaspar/core/vertebrate`  `Chimp/2.1/genome/softmasked_dusted.fa`
`dog`          `jaspar/core/vertebrate`  `Dog/BROADD2/genome/softmasked_dusted/toplevel.fa`
`fruitfly`     `jaspar/core/insect`      `Drosophila/bdgp4.3/drosophila_melanogaster_bdgp43_softmask_dusted_chr.fasta`
`human`        `jaspar/core/vertebrate`  `Human/NCBI36/genome/unmasked/*.fa`
`fugu`         `jaspar/core/vertebrate`  `Fugu/v3/fugu.v3.mask.trf.dust.fa`
`medaka`       `jaspar/core/vertebrate`  `Oryzias_latipes/MEDAKA1/oryzias_latipes.MEDAKA1.norep.fa`
`mouse`        `jaspar/core/vertebrate`  `Mouse/NCBIM37/genome/unmasked/toplevel.fa`
`rat`          `jaspar/core/vertebrate`  `Rat/RGSC3_4/softmasked_dusted/*.fa`
`rhesus`       `jaspar/core/vertebrate`  `Rmacaque/MMUL_2/genome/softmasked_dusted.fa`
`zebrafish`    `jaspar/core/vertebrate`  `Fish/Zv7/genome/zv7_softmasked_dusted.fa`
=============  ========================  =============================================================================

The sequences referred to above are in the form of filenames used
internally at the Wellcome Trust Sanger Institute for the Ensembl
project, but you can probably figure out the version of the assembly
used for the composition measuring process.

Sequence selection
------------------

Several options specify a subset of sequences to run on. The
:option:`--include`\=\ *identifier* option limits the sequences used
in *seqfile* to only those that match *identifier* in the first word of
their definition line. This option can be used multiple times to
include several sequences. The :option:`--include-from`\=\ *filename*
option uses a newline-delimited file to read a list of identifiers
that are included in the same way.

The :option:`--exclude`\=\ *identifier* option workis similarly to
exclude sequences with matching definition lines, after the action of
all of the :option:`--include` and :option:`--include-from` options if
they are used, or from the complete set of sequences in *seqfile* if
they are not. The :option:`--exclude-from`\=\ *filename* option gets
the list of identifiers from the newline-delimited textfile referred
to by *filename*.

Input range
-----------

The :option:`--range`\=\ *slice* option allows you to specify a slice
of the input sequnce to perform simulations on. If you are using
:option:`--mutate` mode, it is important to have some guard sequence
on either side of the mutated sequence (anywhere from 100 bp-300 bp)
to avoid edge effects, if you, say, arbitrarily cut your sequence in
the middle of a strong transcription factor binding site. The
difference between the probability distributions of the reference and
mutated sequence will be computed including the guard sequence but no
mutations will be simulated there.

The :option:`--range`\=\ *slice* option also applies to the other
modes, where it exhibits a slightly different behavior, slicing away
the excluded stuff before any computation.

The *slice* is specified as a Python slice, meaning that it is
zero-based, and half-open. As an example, specifying `-1000:1000`
means a 2000 bp slice with 1000 bp on either side of the TSS, starting
with position -1000 and ending with position 999 (which would be
called +1000 in coordinate systems where the first transcribed
position is called +1 instead of 0, as Sunflower does).

Reference mode options
----------------------

When simulating TF competition and binding to DNA, Sunflower generates
a vector of probability for each nucleotide in the input sequence.
This vector includes two components for each column of each PWM--one
for the PWM read in the forward direction, and one for its reverse
complement. Each component as an identifier such as ``TBP.f0``, which
means the first column of the TBP PWM (in the forward direction) or
``FOXA2.r2``, which is the third column of the reverse complement of
the FOXA2 PWM.

These quantities are only the probability that a particular nucleotide
is bound by a particular PWM column and orientation. In contrast, it
is often useful to have probabilities that a nucleotide is bound by
*any* column of a PWM in any orientation, which greatly reduces the
amount of output. This is, in fact, the default that
:program:`sunflower` uses, adding together all of the forward and
backward states for a particular TF, and leading to a combined state
output. This takes the form of a smaller vector that has a single
component for each PWM, named, for example, simply ``TBP`` or
``FOXA2``. To disable this feature and produce full output for each
PWM column and orientation, use the :option:`--separate-state-groups`
option, which instead saves states individually.

The :option:`--states`\=\ *regex* option allows you to specify a
regular expression *regex* to control the states written to disk.
Saving all the states would take much disk space, and be wasteful
since TBP.f1 is much like TBP.f0, shifted over once.

File output
-----------

By default, :program:`sunflower` stores its output in HDF5 format for further
processing (for example, by :program:`sunreport`). It stores the output in a
number of array datasets, named by the "seqname," of the input
sequence, which is the first word of its definition line.

By default Sunflower saves a copy of the input sequence attached to
the output array. To disable this feature, and thereby save a small
amount of disk space, use the :option:`--no-sequence` option.

Database output
---------------
:program:`sunflower` has a plugin driver architecture for storing
output in formats other than HDF5. Only one additional driver is
included in the Sunflower distribution--a driver for storing output in
a MySQL database, which can be used by other applications such as a
`Distributed Annotation System`_ server (not included). To use it, use
the :option:`--driver=mysql` option.

To use MySQL output, specify :option:`--driver=mysql`. You can specify
the host and port to connect to with :option:`--host`\=\ *host* and
:option:`--port`\=\ *port*. Specify the username and password with
:option:`--user`\=\ *user* and :option:`--password`\=\ *password*.
Specify the database name with :option:`--database`\=\ *database*.

Use :option:`--driver-help` for a list of options that can be set with
the driver, such as database username and password. The available
options are also described in :ref:`sunflower-usage-summary` below.

Tab-delimited output
--------------------

Another driver is tab-delimited output, which works well for
:option:`--mutate` mode and obviates the need for running
:program:`sunreport`. This was contributed by Alison Meynert. To use
it, use the :option:`--driver=tabdelim` option.

.. _sunflower-usage-summary:

Usage summary
-------------

::

  Usage: sunflower [OPTION...] MODEL SEQFILE OUTFILE
         sunflower [OPTION...] --driver=DRIVER MODEL SEQFILE [DRIVEROPTIONS...]

  Options:
    --version             show program's version number and exit
    -h, --help            show this help message and exit

    Model:
      -R, --resource      get MODEL from a resource that comes with the
                          sunflower distribution instead of a file

    Sequence:
      -i DEFLINE, --include=DEFLINE
                          run only on DEFLINE
      --include-from=FILE
                          run only on specified deflines from FILE
      -x DEFLINE, --exclude=DEFLINE
                          don't run on DEFLINE
      --exclude-from=FILE
                          don't run on specified deflines from FILE

    Comparison mode:
      -m, --mutate        iteratively mutate input sequences
      -2 SEQFILE2, --diff=SEQFILE2
                          compute difference between sequences in SEQFILE and
                          SEQFILE2

    Output options:
      -s POS, --start=POS
                          call the first position POS
      -S REGEX, --states=REGEX
                          only write states matching REGEX
      --separate-state-groups
                          don't add together .f0, .f1, .r0, etc.
      -r SLICE, --range=SLICE
                          only write positions in SLICE (ignores start values)
      --no-sequence       don't write seq attribute of output (saves space)

    Output driver:
      -d DRIVER, --driver=DRIVER
                          set output format
      --driver-help       get driver-specific help

    Database options:
      -d DRIVER, --driver=DRIVER
                          use driver DRIVER
      -D DATABASE, --database=DATABASE
                          use database DATABASE
      -h HOST, --host=HOST
                          connect to host HOST
      -p PASSWORD, --password=PASSWORD
                          login with password PASSWORD
      -P PORT, --port=PORT
                          use port PORT
      -u USER, --user=USER
                          login with user USER

.. _`Distributed Annotation System`: http://www.biodas.org/wiki/Main_Page
.. _Poly: http://www.ebi.ac.uk/~hoffman/software/poly/

sunreport
=========
.. program:: sunreport

The :program:`sunreport` command tabulates the HDF5 results of
:program:`sunflower` in reference or :option:`--mutate` mode, and
produces tab-delimited text output. This tabulation function is
separated from the main :program:`sunflower` command to allow a
diverse set of analyses to be quickly run from the results of a single
computationally expensive :program:`sunflower` run. You do not use
:program:`sunreport` to get results from :option:`--diff` mode, which
you must access directly from the HDF5 output.

Since it is agnostic to the labels in the results file it uses as
input, they can be a TF binding profile, as produced by :program:`sunflower`
in reference mode, or the new nucleobase at a point mutation, as
produced by ``sunflower --mutate``.

Output fields
-------------

Depending on which options are used, :program:`sunreport` will produce
tabulations with different fields, and different (but related)
semantics for those fields. The definitions of the fields follow:

=======================  ======================================================
Field name               Description
=======================  ======================================================
``seqname``              first word of sequence definition line from Fasta file
``factor``               some sort of discrete variable used to stratify
                         results
``state``                name of a state or collection of states in the HMM
``mutation``             nucleobase mutated to at a particular position
``pos``                  position relative to the transcription start site
``prob``                 (average) posterior probability of the model in the
                         state
``sum_relent_ref_mut``   (average) relative entropy ref\ |rarr|\ mut at a
                         position (little *t*)
``sd``                   standard deviation of ``prob`` or
                         ``sum_relent_ref_mut``
``min``                  minimum of ``prob`` or ``sum_relent_ref_mut``
``max``                  maximum of ``prob`` or ``sum_relent_ref_mut``
``n``                    number of datapoints used to calculate ``prob`` or
                         ``sum_relent_ref_mut``
``T``                    inherent propensity to transcriptional change
``T_d``                  actual amount of transcriptional change (a
                         sum of ``sum_relent_ref_mut`` over a region
``d_T``                  a substitution distance for transcriptional
                         change (see paper)
=======================  ======================================================

The :option:`--all-columns` option causes almost all of these fields
to be output, even when they have missing values or are the same
throughout the output.

Major modes
-----------

:program:`sunreport` has several major modes.

* the default, where the values of each label (TF binding state or
  mutation nucleobase) is reported at each position of each array.
* you can use the :option:`--aggregate` option to average results from all
  of the arrays together. The resulting tabulation can be plotted for
  an aggregation plot.
* histogram mode, specified with :option:`--hist-bins` and
  :option:`--hist-max`, which reports not the actual values in the
  results, but how many of them fall into various bins of a histogram.

.. _sunreport-stratification:

Stratification
--------------

:program:`sunreport` can tabulate its output by a number of different
factors, averaging or taking histograms within the subset of data
columns specified by the stratification factor. Use of these options
will add a ``factor`` column to ``sunreport``\'s output, indicating
which factor the average or histogram was calculated over.

The :option:`--tab-delim`\=\ *file* option specifies a headerless
tab-delimited text file, which contains two columns: the first
contains an identifier as used elsewhere in the Sunflower workflow,
and the second contains a label to be used for aggregation. For
example, one might wish to separate identifiers into CpG islands and
CpG deserts. This can be done with a file that has each used
transcript identifier in the first column, and either ``CpG island``
or ``CpG desert`` in the second column.  All of the
identifiers with the same factor label will be combined together
during tabulation.

The :option:`--alignment`\=\ *file* option stratifies on alignment
slices in FASTA file *file*. These slices must have the same
identifier and sequence lengths as the sequence records of the
original reference sequence provided to :program:`sunflower`. This can
be used to compare simulated mutations against the actual
substitutions observed between the reference species (for example,
human), and another related species (for example, dog). The
:option:`--by-position` option causes the stratification to be done on
whether a position is mutated or not in the comparison species, rather
than the (position, nucleotide) pair. As an example, if the human
nucleotide at a position were ``A`` and the dog nucleotide were ``C``,
then the normal :option:`--alignment` mode would consider the A\
|rarr|\ C to be associated with the observed mutation factor, but A\
|rarr|\ G, and A\ |rarr|\ T not to. With :option:`--by-position`, they
would all be associated with the observed mutation factor, but another
position where the human and dog nucleotides are identical would not be.

The :option:`--distances` option calculates the evolutionary distances
*T*, |T_d|, and |d_T|, adding a new column for each. It must be used
with the :option:`--alignment` option. The
:option:`--only-substitutions` option omits all rows except for those
where an observed substitution occurs.

By default, :program:`sunreport` usually produces output for each
mutation (for example A |rarr| C, G, or T). The :option:`--total`
option causes all of these to be added together. The ``mutation``
column always has ``all`` as its value when this happens.

.. |T_d| replace:: *T*\ :sub:`d`

.. |d_T| replace:: *d*\ :sub:`T`

.. TODO: need to do emphasis within subscript--ask on docutils mailing list

Totals of mutation mode output
------------------------------

When :program:`sunflower` is run in mutation mode, it produces output
for each mutation (for example A |rarr| C, G, or T). Then
:program:`sunreport` produces output for each mutation as well. The
:option:`--total` option instead produces output for each base pair,
summing up the results from all of the possible mutations.

Input range
-----------

Much like in :program:`sunflower`, the :option:`--include`\=\
*identifier* option limits the Sunflower output arrays used as input
to only those that match *identifier* in the first word of their
definition line. This option can be used multiple times to include
several sequences. The :option:`--include-from`\=\ *filename* option
uses a newline-delimited file to read a list of identifiers that are
included in the same way.

The :option:`--range` option allows the specification of ranges to be
used for averages. For example, ``--range=-50:50`` specifies that
averages are calculated on the 100 base pairs beginning with -50 and
ending with +49 inclusive (with the first position after the TSS
designated as 0, not +1). In the output the ``pos`` column will be
``-50:50`` for these rows. You may repeat this option to specify an
arbitrary number of ranges, with something like ``--range=-50:50
--range=-100:100``. If :option:`--range` is used, then
:option:`--total` is automatically set.

The :option:`--measurement-min`\=\ *min* option specifies that only
data where the measurement (either ``prob`` or ``sum_relent_ref_mut``)
is greater than *min*.

When :option:`--range` is specified the default switches to
:option:`--total` (see :ref:`sunreport-stratification` above). To
override this and generate estimates for each mutation type, use the
:option:`--no-total` option.

Usage summary
-------------

::

  Usage: sunreport [OPTION]... FILE

  Options:
    --version             show program's version number and exit
    -h, --help            show this help message and exit

    Output control:
      -p POS, --start=POS
                          [DEPRECATED] call the first position POS
      -A, --aggregate     average results from different sequences (sum in
                          histogram mode)
      -T, --total         total mutation or state
      --no-total          report mutation or state individually
      -C, --all-columns   include all columns in output, even if they are
                          uninformative

    Specify a subset:
      -i ARRAY, --include=ARRAY
                          report only on ARRAY
      --include-from=FILE
                          report only on arrays specified in FILE
      -r RANGE, --range=RANGE
                          report only on average results for positions RANGE in
                          the form of "-50:50"
      -H BINS, --hist-bins=BINS
                          output histograms of BINS bins
      --hist-max=LIMIT    calculate histogram bins in the range 0:LIMIT
      --measurement-min=MIN
                          only include data where measurement > MIN

    Stratification factor control:
      -t TABFILE, --tab-delim=TABFILE
                          stratify on identifiers in TABFILE
      -a FASTAFILE, --alignment=FASTAFILE
                          stratify on align slices in FASTAFILE
      -d, --distances     generate evolutionary distances
      -P, --by-position   stratify by position; disregard nucleotide
      -s, --only-substitutions
                          only include substitution positions

Sunreport is an optional step. If you are processing large amounts of
data, it may be more efficient to access the HDF5 output of
:program:`sunflower` directly, for example using the ``hdf5`` package in R,
or PyTables in Python, or HDF5 in C, C++, or Java.

Acknowledgments
===============
Thanks to Alison M. Meynert for code contributions (in
:program:`pwm2sfl`, :mod:`sunflower.coop`, :mod:`sunflower.priors`)
and Guy Slater (:program:`fastacomp`, used in generating resources).

JASPAR data included by kind permission of Boris Lenhard. If you use
this data, please cite:

  Vlieghe D, Sandelin A, De Bleser PJ, Vleminckx K, Wasserman WW, van
  Roy F, Lenhard B. "A new generation of JASPAR, the open-access
  repository for transcription factor binding site profiles." *Nucleic
  Acids Res.* 2006 January 1; 34(Database issue): D95-D97.

This material is based upon work supported under a National Science
Foundation Graduate Research Fellowship. Any opinions, findings,
conclusions or recommendations expressed in this publication are those
of the author(s) and do not necessarily reflect the views of the
National Science Foundation.

License
=======
Sunflower is available under the GPLv2 license.

Contact
=======
Please write to <mmh1 at washington edu> know if you have any comments
on the installation, use, or documentation of Sunflower. I would love
to know if you get it working on a system not listed above.

If you need support with your use of Sunflower, please the
<sunflower-users@ebi.ac.uk> mailing list. Using the mailing list will
get your question answered more quickly. It also allows us to pool
knowledge and reduce getting the same inquiries over and over.
