"""Misc utility functions for handling binary data."""

__all__ = ['bin', 'read_midi_short']

from struct import pack, unpack


def bin(x):
    """Format given number (int or long) as binary in the form 0bxx.

    """
    if x < 0:
        return '-' + bin(-x)
    out = []
    if x == 0:
        out.append('0')
    while x > 0:
        out.append('01'[x & 1])
        x >>= 1
        pass
    try:
        return '0b' + ''.join(reversed(out))
    except NameError, ne2:
        out.reverse()
    return '0b' + ''.join(out)

def read_midi_short(msb, lsb=0):
    if isinstance(msb, str):
        msb, lsb = unpack('>BB', msb)
    return (msb << 7) | lsb
