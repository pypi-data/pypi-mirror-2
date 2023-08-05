# -*- coding: ISO-8859-1 -*-
"""This module contains functions for reading and writing the special data types
that a midi file contains.
"""

__all__ = [
    'get_nibbles',
    'set_nibbles',
    'read_bew',
    'write_bew',
    'read_varlen',
    'sizeof_varlen',
    'write_varlen',
    'to_n_bits',
    'to_bytes',
    'from_bytes'
]

# standard library imports
from struct import pack, unpack


# A Nibble has four bits. A byte consists of two nibles.
# hi_nibble==0xF0, lo_nibble==0x0F.
# Especially used for setting channel and event in the first byte of musical
# midi events.

def get_nibbles(byte):
    """Return hi and lo bits in a byte as a tuple.

    >>> get_nibbles(142)
    (8, 14)

    Asserts byte value in byte range
    >>> get_nibbles(256)
    Traceback (most recent call last):
        ...
    ValueError: Byte value out of range 0-255: 256

    """
    if not 0 <= byte <= 255:
        raise ValueError('Byte value out of range 0-255: %s' % byte)
    return (byte >> 4 & 0xF, byte & 0xF)

def set_nibbles(hi_nibble, lo_nibble):
    """Return byte with value set according to hi and lo bits.

    Asserts hi_nibble and lo_nibble in range(16)

    >>> set_nibbles(8, 14)
    142

    >>> set_nibbles(8, 16)
    Traceback (most recent call last):
        ...
    ValueError: Nible value out of range 0-15: (8, 16)

    """
    if not (0 <= hi_nibble <= 15) or not (0 <= lo_nibble <= 15):
        raise ValueError('Nible value out of range 0-15: (%s, %s)'
            % (hi_nibble, lo_nibble))
    return (hi_nibble << 4) + lo_nibble

def read_bew(value):
    """Read string as big endian word.

    Asserts len(value) in [1, 2, 4].

    >>> long(read_bew('aáâã'))
    1642193635L
    >>> read_bew('aá')
    25057

    """
    return unpack('>%s' % {1:'B', 2:'H', 4:'L'}[len(value)], value)[0]

def write_bew(value, length):
    """Write int as big endian formatted string.

    Asserts length in [1, 2, 4].

    Difficult to print the result in doctest, so do a simple roundabout test:

    >>> read_bew(write_bew(25057, 2))
    25057
    >>> long(read_bew(write_bew(1642193635L, 4)))
    1642193635L

    """
    return pack('>%s' % {1:'B', 2:'H', 4:'L'}[length], value)

# Variable Length Data (varlen) is a data format sprayed liberally throughout
# a midi file. It can be anywhere from 1 to 4 bytes long.
# If the 8'th bit is set in a byte another byte follows. The value is stored
# in the lowest 7 bits of each byte. So max value is 4x7 bits = 28 bits.

def read_varlen(value):
    """Convert varlength format to integer.

    Just pass it 0 or more chars that might be a varlen and it will only use
    the relevant chars.

    Use sizeof_varlen(value) to see how many bytes the integer value takes.

    asserts len(value) >= 0
    >>> read_varlen('€@')
    64
    >>> read_varlen('áâãa')
    205042145

    """
    sum = 0
    for byte in unpack('%sB' % len(value), value):
        sum = (sum << 7) + (byte & 0x7F)
        if not 0x80 & byte: break # stop after last byte
    return sum

def sizeof_varlen(value):
    """Return number of bytes an integer will need when converted to varlength.
    """
    if value <= 127:
        return 1
    elif value <= 16383:
        return 2
    elif value <= 2097151:
        return 3
    else:
        return 4

def write_varlen(value):
    """Convert an integer to varlength format."""
    sevens = to_n_bits(value, sizeof_varlen(value))
    for i in range(len(sevens)-1):
        sevens[i] = sevens[i] | 0x80
    return from_bytes(sevens)

def to_n_bits(value, length=1, nbits=7):
    """Return the integer value as a sequence of nbits bytes."""
    bytes = [(value >> (i*nbits)) & 0x7F for i in range(length)]
    bytes.reverse()
    return bytes

def to_bytes(value):
    """Convert a string into a list of byte values."""
    return unpack('%sB' % len(value), value)

def from_bytes(value):
    """Convert a list of bytes into a string."""
    if not value:
        return ''
    return pack('%sB' % len(value), *value)


if __name__ == '__main__':

    # simple test cases

#    print 'read_bew', read_bew('aáâã')
#    print 'write_bew', write_bew(1642193635, 4)

    print 'read_varlen', read_varlen('€@')
    print 'write_varlen', write_varlen(8192)

    print 'read_varlen', read_varlen('áâãa')
    print 'write_varlen', write_varlen(205058401)

#    vartest = '\x82\xF7\x80\x00'
#    print 'to_bytes', to_bytes(vartest)
#    print 'from_bytes', from_bytes([48, 49, 50,])


#    instr = '\xFF\xFF\xFF\x00'
#    print 'read_varlen', read_varlen(instr)
#    inst2 = 268435455
#    print inst2
#    print write_varlen(inst2)
#    print write_varlen(read_varlen(instr))

    s1 = 0x00000000
    print '%08X -' % s1, '00',  write_varlen(s1)
    s2 = 0x00000040
    print '%08X -' % s2, '40',  write_varlen(s2)
    s3 = 0x0000007F
    print '%08X -' % s3, '7F',  write_varlen(s3)
    s4 = 0x00000080
    print '%08X -' % s4, '81 00',  write_varlen(s4)
    s5 = 0x00002000
    print '%08X -' % s5, 'C0 00',  write_varlen(s5)
    s6 = 0x00003FFF
    print '%08X -' % s6, 'FF 7F',  write_varlen(s6)
    s7 = 0x00004000
    print '%08X -' % s7, '81 80 00',  write_varlen(s7)
    s8 = 0x00100000
    print '%08X -' % s8, 'C0 80 00',  write_varlen(s8)
    s9 = 0x001FFFFF
    print '%08X -' % s9, 'FF FF 7F',  write_varlen(s9)
    s10 = 0x00200000
    print '%08X -' % s10, '81 80 80 00', write_varlen(s10)
    s11 = 0x08000000
    print '%08X -' % s11, 'C0 80 80 00', write_varlen(s11)
    s12 = 0x0FFFFFFF
    print '%08X -' % s12, 'FF FF FF 7F', write_varlen(s12)
