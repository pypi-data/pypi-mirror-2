#!/usr/bin/env python
from __future__ import division

__version__ = "$Revision: 366 $"

# Copyright 2007 Michael M. Hoffman <hoffman+software@ebi.ac.uk>

from itertools import izip
import re
import sys
from warnings import filterwarnings

from MySQLdb import IntegrityError
from dboptions import DbOptionParser, connect
import docsql
from numpy import empty, uint8

from . import Driver, DriverHelpFormatter, defline_identifier

QUANTIZATION_SCALE = 255.0

class Insert_tf(docsql.Insert):
    """
    INSERT INTO tf SET name=%s
    """

class Select_tf_id(docsql.SelectOneCell):
    """
    SELECT tf_id FROM tf WHERE name=%s
    """

class Insert_seq_region(docsql.Insert):
    """
    INSERT INTO seq_region SET name=%s
    """

class Select_seq_region_id(docsql.SelectOneCell):
    """
    SELECT seq_region_id FROM seq_region WHERE name=%s
    """

class Insert_prob(docsql.Insert):
    """
    INSERT DELAYED INTO prob (tf_id, seq_region_id, seq_region_start,
                              seq_region_end, probs)
    VALUES (%s, %s, %s, %s, %s)
    """

def get_rowid(insert, select, name, connection):
    try:
        cursor = insert(name, connection=connection)
        return cursor.lastrowid
    except IntegrityError:
        return select(name, connection=connection)

class RowAppender(object):
    """
    converts 0-based to offset 1-based and appends
    """

    def __init__(self, sequence, tf_id, seq_region_id, start):
        self.sequence = sequence
        self.tf_id = tf_id
        self.seq_region_id = seq_region_id
        self.start = start

    def __call__(self, start, end, values):
        self.sequence.append([self.tf_id,
                              self.seq_region_id,
                              start + self.start,
                              end + self.start - 1,
                              values])

# 19 bytes or greater
# XXX: there's a pathological case where you have something that looks like
# [19A, 1B, 19A]
# you would be better off representing it as
# AAAAAAAAAAAAAAAAAAABAAAAAAAAAAAAAAAAAAA
# because the 1B uses so much space
#
# this would add extra code complexity to deal with properly; probably
# not worth it
re_charrun = re.compile(r"(.)\1{17,}")
class SQLDriver(Driver):
    def __init__(self, command_args, *args, **kwargs):
        options, command_args = self.parse_options(command_args)
        self.dboptions = options.dboptions

        Driver.__init__(self, [], *args, **kwargs)

    @staticmethod
    def get_option_parser():
        usage = ("%prog --driver=DRIVER [OPTION...] MODEL SEQFILE "
                 "[DRIVEROPTION...]")
        return DbOptionParser(usage=usage, formatter=DriverHelpFormatter())

    def parse_options(self, args):
        parser = self.get_option_parser()
        options, args = parser.parse_args(args)

        if len(args) != 0:
            self.print_usage()
            sys.exit(1)

        return options, args

    def __enter__(self):
        connection = connect(self.dboptions)
        self.connection = connection
        self.tf_ids = [get_rowid(Insert_tf, Select_tf_id, colname, connection)
                       for colname in self.colnames]

        return self

    def __exit__(self, *exc_info):
        self.connection.close()

    # XXXopt:
    # reimplement run-length encoding from
    # http://projects.scipy.org/pipermail/numpy-discussion/2007-October/029378.html
    def __call__(self, arr, (defline, seq)):
        name = defline_identifier(defline)
        connection = self.connection

        seq_region_id = get_rowid(Insert_seq_region, Select_seq_region_id,
                                  name, connection=connection)

        start = self.defline_start(defline)
        assert start >= 1

        # uses floor to quantize
        quantized_array = (arr * QUANTIZATION_SCALE).astype(uint8)

        rows = []
        for tf_id, tf_vec in izip(self.tf_ids, quantized_array.T):
            values = tf_vec.tostring()
            appender = RowAppender(rows, tf_id, seq_region_id, start)

            charrun_start = None
            charrun_end = 0

            for m_charrun in re_charrun.finditer(values):
                charrun_start = m_charrun.start()

                # append previous unencoded chunk
                if charrun_start != charrun_end:
                    values_chunk = values[charrun_end:charrun_start]
                    appender(charrun_end, charrun_start, values_chunk)

                charrun_end = m_charrun.end()

                # append encoded chunk
                appender(charrun_start, charrun_end, m_charrun.group(1))

            values_end = len(values)

            # append last unencoded chunk
            if charrun_start != values_end:
                values_chunk = values[charrun_end:]
                appender(charrun_end, values_end, values_chunk)

        Insert_prob(many=rows, connection=connection)

def main(args=sys.argv[1:]):
    pass

if __name__ == "__main__":
    sys.exit(main())
