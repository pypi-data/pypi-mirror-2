========================================
 Sunflower infrequently asked questions
========================================

Documentation
=============
Is there any other documentation?

  Michael's thesis is available on request, which explains some of the
  theory behind Sunflower and some use cases.

Pwm2sfl
=======
What would I do if I wanted to run one particular Jaspar matrix or a
set of 3?

  Setup a directory that contains only those matrices and use
  :program:`pwm2sfl` to produce a new model. Then use that instead of
  resource ``human``. Someone on the ``sunflower-users`` mailing list may
  volunteer a script that will do this already.

Is this planned as a feature in pwm2sfl eventually?

  Yes, eventually.

Can I change the weighting of different transcription factor
transition probability priors?

  Alison M. Meynert has written :program:`sunpriors`, which should
  accomplish this.

What format are PWM matrix files in?
  The same as that used for JASPAR. It has a list of matrices with all
  the metadata and a file for each matrix. If you want to make your
  own, I recommend starting with a directory of JASPAR matrices and
  then hacking it.

Sunflower
=========
Which model should I use?
  It's best to use a species-specific model for your data as it will
  have G+C content information incorporated. Sunflower includes a
  number of resources for different animal species.

What if there's not already a model for my species?

  Use the ``sunrecompose`` program to incorporate the G+C information.

What are the different modes you can run ``sunflower`` in?

  * ``sunflower`` without ``--mutate`` gives you an *absolute* measurement of
    binding probability.
  * ``sunflower --mutate`` gives you a *relative* measurement of how
    the above measurement changes with respect to a mutation.  These
    should be symmetric for point mutations--the value for the
    mutation to T when running Sunflower on the reference sequence
    should be the same as the value of the mutation to C when running
    on the variant. Note that this will not be true if there are other
    nearby substitutions in the variant haplotype.

Why am I getting a measurement for each transcription factor instead
of each mutation?

  Use the ``--mutate`` option.

I am trying to interpret the output for the ``--mutate`` option.
Can you tell me why there are only values for certain positions?

  If you have an A in position 3, you will not get a value for A there
  because there is no change from the reference sequence. Remember,
  Sunflower measures the change in binding profile due to a
  mutation. If a value were measured it would be 0 since there is no
  change.

  If you want a value for each position without considering which
  mutation you are measuring, try the ``--total`` option to
  ``sunreport``, which will get you an average.

What do the values in ``--mutate`` mode mean?

  The higher the value, the greater an effect the simulated mutation
  will have on the binding profile. This is value summed over *all*
  sites, and will include the knock-on effects of a SNP in positions
  beyond.

How short a sequence can I use?

  If you have, say, a transcription factor with a 20-bp motif that is
  binding to your SNP position at the last bit of the motif, Sunflower
  will not find it because you are not giving enough flanking
  sequence. And if you only give it enough to catch that TF, you'll
  miss the competitive effects of other TFs acting on upstream or
  downstream regions of sequence. This is why I very conservatively
  suggest using 300 bp of padding sequence on each side of the
  sequences you are interested in.

  The --range option only produces output for a certain range, so if you
  were feeding in 601 bp sequences but you're only interested in the
  position in the middle, you could do something like --range 300:-300
  or --range 300:301. Then you will only get output for position 300
  (zero-based coordinates).

  I should only simulate mutations and recalculate for positions in the
  range... but I don't yet. It's on the todo list.

How can I make ``--mutate`` mode run faster?

  You can get a considerable speedup in ``--mutate`` mode by using
  ``python -O $(which sunflower)`` instead of just ``sunflower``. This
  turns off some belt-and-braces assertions I've added that check that
  all probabilities sum to 1 after each forward-backward run. Here's
  an example on two sequences of 2000 bp each::

    $ time python -O $(which sunflower) --mutate --resource human test/data/brca_tss.fna brca.h5

    real    47m14.683s
    user    46m5.152s
    sys     1m8.458s

    $ time python $(which sunflower) --mutate --resource human test/data/brca_tss.fna brca.h5

    real    115m22.098s
    user    110m13.558s
    sys     5m6.794s

  After I have some optional automated tests to do the same thing at
  install time this will be done by default.

I want to compare two haplotypes, not exhaustively simulate every
possible mutation.

  Run ``sunflower`` in non-mutate mode for both sequences. This will
  get you the unbound posterior probabilities. You could either
  subtract at each point, square it, and sum to get the
  sum_sqdiff_unbound result ``sunflower`` uses. Or you could do any
  other sort of calculation you want.

Why don't the probabilities add up to 1?

  Don't worry about it, everything is fine. :)

  By default Sunflower only stores the first state in each TF column,
  and if you added up all the other states you would get
  1.0. Sunflower will automatically double-check this unless you tell
  it not to. If you want to verify it yourself, you can do something
  like this, using the --states option of sunflower to save
  everything::

    $ sunflower --states='^(?!silent$)' --resource human \
          --include=BRCA1 test/data/brca_tss.fna brca.h5
    $ sunreport --no-total brca.h5 | filter 'pos == "73"' | cut -f 3 \
    | nohead \
    | python -c 'import sys; print sum([float(x) for x in sys.stdin.read().split()])'
    1.0

  How do you tell Sunflower not to do these checks if you want it to
  go faster? Use ``python -O $(which sunflower)`` instead of just
  ``sunflower``. This runs it in no-belts-no-braces mode.

