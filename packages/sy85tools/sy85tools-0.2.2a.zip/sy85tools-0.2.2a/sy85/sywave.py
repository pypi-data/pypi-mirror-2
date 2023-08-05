#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import struct

from converters.smf import *

SYWAVE_HEADER = (
    ('10s', 'file_id'),         # 0 - 9
    ('6x',),                    # 10 - 15
    ('B', '_highkey_a'),        # 16
    ('B', '_highkey_b'),        # 17
    ('B', 'orig_key'),          # 18
    ('x',),                     # 19
    ('B', '_pitch_a'),          # 20
    ('B', '_pitch_b'),          # 21
    ('2x',),                    # 22: Guess: 00 00
    ('B', 'loop_type'),         # 24: Bitwise loop info.
    ('B', '_sy_loop_start_hi'), # 25: This is in HML sequence
    ('B', '_sy_loop_start_mid'),# 26
    ('B', '_sy_loop_start_lo'), # 27
    ('B', '_sy_loop_end_mid'),  # 28: this is in MLH sequence
    ('B', '_sy_loop_end_lo'),   # 29
    ('B', '_sy_loop_end_hi'),   # 30
    ('B', '_sample_no_hi'),     # 31: No of Samples - 1 in HML sequence
    ('B', '_sample_no_mid'),    # 32
    ('B', '_sample_no_lo')      # 33
    ('B', 'volume'),            # 34: Attenuation of sample (127 - Volume)
    ('9x',),                    # 35 - 43: Guess: 01 3F 00 00 00 28 3F 3F FF
    ('B', 'sample_format'),     # 44: 8 or 16 (bits per sample)
    ('B', '_sample_period_lo'), # 45: This is reciprocal of sample
    ('B', '_sample_period_mid'),# 46: frequency stored as 7-Bit data,
    ('B', '_sample_period_hi'), # 47: same as MIDI Sample Dump
    ('B', '_sample_len_lo'),    # 48: Stored as 7-Bit data
    ('B', '_sample_len_mid'),   # 49: same as MIDI Sample Dump
    ('B', '_sample_len_hi'),    # 50
    ('B', '_loop_start_lo'),    # 51: Stored as 7-Bit data, same
    ('B', '_loop_start_mid'),   # 52: as MIDI Sample Dump
    ('B', '_loop_start_hi'),    # 60
    ('B', '_loop_end_lo'),      # 54: Stored as 7-Bit data, same
    ('B', '_loop_end_mid'),     # 55: as MIDI Sample Dump
    ('B', '_loop_end_hi'),      # 56
    ('x',),                     # 57: Always 7F
    ('B', '_small_blocks_a'),   # 58: No of 40 sample blocks
    ('B', '_small_blocks_b'),   # 59: No of 40 sample blocks
    ('B', '_big_blocks_a'),     # 60: No of 512 sample blocks
    ('B', '_big_blocks_b'),     # 61: No of 512 sample blocks
    ('2x',),                    # 62: Always 00 7D
    ('B', '_low_key_a'),        # 64: Low key of mapped sample
    ('B', '_low_key_b'),        # 65:
    ('958x',),                  # 66: Filled with Nulls
)

def parse_struct(structdef, data):
    fmt = "".join(x[0] for x in structdef)
    fields = (x[1] for x in structdef if len(x) >= 2 and x[1])
    return dict(zip(fields, struct.unpack(fmt, data[:struct.calcsize(fmt)])))

class SYWave(object):
    def __init__(self, fn):
        sywave = open(fn)
        header = parse_struct(SYWAVE_HEADER, sywave.read(1024))
        sywave.close()
        self.__dict__.update(header)

    @property
    def loop_end(self):
        return (self._loop_end_hi << 16 | self._loop_end_mid << 8 |
                self._loop_end_lo)

    @property
    def loop_start(self):
        return (self._loop_start_hi << 16 | self._loop_start_mid << 8 |
                self._loop_start_lo)

def main(args):
    from pprint import pprint
    sywave = SYWave(args[0])
    pprint(sywave.__dict__)
    print "Loop start:", sywave.loop_start
    print "Loop end:", sywave.loop_end
    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
