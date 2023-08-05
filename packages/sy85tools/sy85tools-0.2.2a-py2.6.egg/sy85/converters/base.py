# -*- coding: UTF-8 -*-

__all__ = [
    'b_lookup',
    'b_range',
    'bitflag',
    'frange',
    'l_range',
    'lookup',
    'read_byte',
    'read_midi_short',
    'read_string',
    's_lookup',
    's_range',
    's_signed',
    'subbyte_lookup',
    'subbyte_range',
    'value_range'
]

import math
from struct import pack,unpack


def frange(limit1, limit2=None, increment=1.0):
    """Range function that accepts floats (and integers).

    Usage::

        frange(-2, 2, 0.1)
        frange(10)
        frange(10, increment = 0.5)

    The returned value is an iterator. Use ``list(frange)`` for a list.

    Source: http://code.activestate.com/recipes/66472/#c7
    """

    if limit2 is None:
        limit2, limit1 = limit1, 0.0
    else:
        limit1 = float(limit1)
    count = int(math.ceil(limit2 - limit1) / increment)
    return (limit1 + n*increment for n in xrange(count))


def read_bew(value):
    """Read string as big endian word.

    Asserts len(value) in [1, 2, 4].

    >>> long(read_bew('aáâã'))
    1642193635L
    >>> read_bew('aá')
    25057

    """
    return unpack('>%s' % {1:'B', 2:'H', 4:'L'}[len(value)], value)[0]

def read_byte(c):
    """Convert single-char string into integer by reading it as signed byte."""
    return unpack('b', c)[0]

def read_midi_short(msb, lsb=0):
    if isinstance(msb, str):
        msb, lsb = unpack('BB', msb)
    return (msb << 7) | (lsb & 0x7f)

def lookup(value, *args):
    """Look up 'value' as index or key in given dict, list or argument list."""
    try:
        if isinstance(args[0], (dict, list)):
            return args[0][value]
        else:
            return args[value]
    except (IndexError, KeyError):
        raise KeyError("Value not in map: %i", value)

def value_range(value, minval=0, maxval=100, step=1):
    """Return value with index 'value' from the list 'minval'->'maxval'/'step'.
    """
    if minval < value > maxval:
        raise ValueError("Value not in range: %i" % value)
    if isinstance(minval, float) or isinstance(maxval, float):
        return list(frange(minval, maxval+1, step))[value]
    else:
        return list(xrange(minval, maxval+1, step))[value]

def b_lookup(value, *args):
    value = read_byte(value)
    return value, lookup(value, *args)

def b_range(value, minval=0, maxval=127, *args):
    return value_range(read_byte(value), minval, maxval, *args)

def subbyte_range(value, bitmask, minval=0, maxval=127, *args):
    value = read_byte(value) & bitmask
    return value_range(value, minval, maxval, *args)

def subbyte_lookup(value, bitmask, *args):
    value = read_byte(value) & bitmask
    return value, lookup(value, *args)

def s_lookup(value, *args):
    value = read_midi_short(value)
    return value, lookup(value, *args)

def s_range(value, minval=0, maxval=255, *args):
    value = read_midi_short(value)
    return value_range(value, minval, maxval, *args)

def s_signed(value, minval=-127, maxval=127, *args):
    value = read_midi_short(value)
    value = -(value & 0x7f) if value & 0x80 else value & 0x7f
    if minval < value > maxval:
        raise ValueError("Value not in range: %i" % value)
    return value

def l_range(value, minval=0, maxval=2139062143):
    value = read_bew(value)
    if minval < value > maxval:
        raise ValueError("Value not in range: %i", value)
    return value

def read_string(value, *args):
    return value

def bitflag(value, bit, *args):
    return read_bew(value) & (1 << bit) > 0
