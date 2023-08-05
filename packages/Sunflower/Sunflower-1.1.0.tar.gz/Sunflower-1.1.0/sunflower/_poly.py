#!/usr/bin/env python
from __future__ import division

"""
_poly: provides pass-through substitute functions for Poly

chunk() ordinarily gets a work chunk for a distributed system
substitute() substitutes special identifiers in filename
"""

__version__ = "$Revision: 49 $"

# Copyright 2007 Michael M. Hoffman <hoffman+software@ebi.ac.uk>

import sys

def _chunk(collection):
    return collection

def _substitute(text):
    return text

try:
    from poly import chunk, substitute
except ImportError:
    chunk = _chunk
    substitute = _substitute

def main(args=sys.argv[1:]):
    pass

if __name__ == "__main__":
    sys.exit(main())
