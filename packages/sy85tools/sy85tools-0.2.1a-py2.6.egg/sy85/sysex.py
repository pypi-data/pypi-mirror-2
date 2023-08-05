"""Classes and functions for representing and handling SY85 sysex bulk dumps."""

# standard library imports
import logging
import struct

from itertools import chain

# private modules
import bulktypes
from constants import *
from binutils import bin, read_midi_short

# exceptions

class SysexParseError(Exception):
    pass
class UnsupportedSysexType(SysexParseError):
    pass
class UnsupportedBulkType(SysexParseError):
    pass
class ChecksumError(SysexParseError):
    pass


#functions

def is_yamaha_sysex(data):
    """Return True if given data looks like a Yamaha Sysex bulk dump."""
    return len(data) >= 8 and data.startswith(SOX + MANUFACTURER_ID)


# classes

class SY85SysexContainer(dict):

    bulk_types = [
        'voices',
        'drumvoices',
        'performances',
        'multis',       # i.e. "Songs" in Yamahaese
        'songs',        # i.e. sequencer data
        'rhythms',
        'seq_dumps',
        'synth_setups',
        'seq_setups',
        'samples'
    ]

    def __init__(self, strict=False):
        super(SY85SysexContainer, self).__init__()
        for type_ in self.bulk_types:
            self[type_] = []
        self.strict = strict

    @classmethod
    def fromfile(cls, fn, strict=False):
        if isinstance(fn, basestring):
            fn = open(fn, 'rb')
        inst = cls(strict)
        inst.parse_sysex_data(fn.read())
        return inst

    def parse_sysex_data(self, data):
        chunks = data.split(SOX)[1:]
        for i, chunk in enumerate(chunks):
            try:
                typecode, data, checksum = self.parse_sysex_chunk(SOX+chunk)
            except SysexParseError, exc:
                if self.strict:
                    raise
                else:
                    logging.warning('Parse error chunk %i: %s', i, exc)
        if not chunks:
            raise SysexParseError("No valid sysex chunks found.")

    def parse_sysex_chunk(self, data):
        if not is_yamaha_sysex(data):
            raise SysexParseError("Unrecognized data format.")
        data = data.rstrip(EOX)
        header, data, checksum = data[:6], data[6:-1], ord(data[-1])
        sox, man_id, dev_id, msg_fmt_id, bc_msb, bc_lsb = \
            struct.unpack('6B', header)
        typecode = data[4:10]
        bc = read_midi_short(bc_msb, bc_lsb)

        # sanity checks
        if chr(msg_fmt_id) not in (MSG_ID_BULK_DUMP, MSG_ID_NSEQ_DUMP):
            raise UnsupportedSysexType(
                "Only sysex bulk dump messages are supported.")
        if len(data) != bc:
            # XXX:  calculate correct length for NSEQ msgs
            if not typecode in ['0065RY', '0065SQ'] or bc != 538:
                raise SysexParseError("Bogus data length, chunk type %s. "
                    "Read: %i, actual: %i" % (typecode, bc, len(data)))
        self._check_checksum(data, checksum)
        logging.debug("Adding chunk of type %s" % typecode)
        self.add_chunk(typecode, data)
        return typecode, data, checksum

    def add_chunk(self, typecode, data):
        try:
            typename = BULKDATATYPES[typecode]['name']
        except KeyError:
            raise UnsupportedBulkType(
                "Bulk message type not supported: %s" % typecode)
        container_name = typename.lower().replace(' ', '_') + 's'
        container = self.get(container_name)
        bulkclass = getattr(bulktypes, BULKDATATYPES[typecode]['classname'])
        container.append(bulkclass(typecode, data))

    def _check_checksum(self, data, checksum):
        checkbyte = (sum([ord(c) for c in data]) + checksum) & 0x7F
        if checkbyte:
            raise ChecksumError("Checksum error: %s (%i), result: %s" %
                (bin(checksum), checksum, bin(checkbyte)))

    @property
    def chunks(self):
        return chain(*[self[type_] for type_ in self.bulk_types])

    def dump(self, output=None):
        """Dump all chunks to given file or return them as a string if no file is given."""

        data = [chunk.dump() for chunk in self.chunks]
        if output:
            if isinstance(output, file):
                fo = output
            else:
                fo = open(output, 'wb')
            fo.write("".join(data))
            if not isinstance(output, file):
                fo.close()
        else:
            return "".join(data)
