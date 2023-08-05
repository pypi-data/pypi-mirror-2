"""Classes representing different Yamaha SY85 bulk dump types."""

# standard library imports
import logging

# private modules
from constants import *
from binutils import read_midi_short


#classes

class SY85BulkDump(object):

    _data_offset = 26
    _name_offset = None

    def __init__(self, type_, data):
        self.name = None
        self.type = type_
        self._data = data
        self._parse_data()

    def _parse_data(self):
        pass

    def __len__(self):
        return len(self._data) + 8

    def __repr__(self):
        return "Name: %-8s Type: %s" % (self.name or "n/a", self.type_name)

    def dump(self, device_id=0):
        datalen = len(self.data)
        logging.debug("Data length: %i", datalen)
        datalen_lsb = chr(datalen & 0x7F)
        datalen_msb = chr((datalen >> 7) & 0x7F)
        checksum = chr(self._create_checksum(self.data))
        return SOX + MANUFACTURER_ID + chr(device_id) + \
            BULKDATATYPES[self.type]['msg_fmt_id'] + \
            datalen_msb + datalen_lsb + self.data + checksum + EOX

    @property
    def data(self):
        if self._name_offset:
            name_offset = self._data_offset + self._name_offset
            name = "%-8s" % (self.name[:self._name_len],)
            return self._data[:name_offset] + name + \
                self._data[name_offset+self._name_len:]
        else:
            return self._data

    @property
    def type_name(self):
        return BULKDATATYPES[self.type]['name']

    def _create_checksum(self, data):
        cs = sum(ord(c) for c in self.data)
        return ((cs & 0x7f) ^ 0x7f) + 1

    def mk_filename(self, prefix=''):
        return "%s %s %s" % (prefix, self.type[4:], self.name)


class SY85TrackData(SY85BulkDump):
    _data_offset = 10

    def mk_filename(self, prefix=''):
        return "%s NSEQ" % prefix


class SY85Setup(SY85BulkDump):
    def mk_filename(self, prefix=''):
        return "%s %s Setup" % (prefix, self.type[4:])


class SY85Rhythm(SY85BulkDump):
    def mk_filename(self, prefix=''):
        return "%s %s Rhythm" % (prefix, self.type[4:])


class SY85SeqDump(SY85BulkDump):
    def mk_filename(self, prefix=''):
        return "%s %s Seq Dump" % (prefix, self.type[4:])


class SY85Patch(SY85BulkDump):
    _name_offset = 73
    _name_len = 8

    def __init__(self, type_, data):
        super(SY85Patch, self).__init__(type_, data)

    def _parse_data(self):
        super(SY85Patch, self)._parse_data()
        self.name = self._parse_name()
        self.program_number = ord(self._data[25])

    def _parse_name(self):
        if self._name_offset is not None:
            start = self._data_offset + self._name_offset
            return self._data[start:start + self._name_len].strip()

class SY85AbstractVoice(SY85Patch):

    def _parse_data(self):
        super(SY85AbstractVoice, self)._parse_data()
        self.bank_number = ord(self._data[24])

    def mk_filename(self, prefix=''):
        return "%s %s-%s-%s%i %s" % (prefix, self.type[4:],
            BANKNAMES[self.bank_number][1], self.group, self.program, self.name)

    def __repr__(self):
        return ("Name: %-8s Type: %s, Bank: %-7s, Slot: %s (%i)"
            % (self.name,
            self.type_name,
            self.bank_name,
            self.slot,
            self.program_number))

    @property
    def group(self):
        return 'ABCDEFGH'[self.program_number / 8]

    @property
    def program(self):
        return self.program_number % 8 + 1

    @property
    def slot(self):
        return '%s%i' % (self.group, self.program)

    @property
    def bank_name(self):
        return BANKNAMES.get(self.bank_number)[0]

    @property
    def data(self):
        data = super(SY85Voice, self).data[:]
        return data[:30] + chr(self.bank_number) + chr(self.program_number) + \
            data[32:]


class SY85Voice(SY85AbstractVoice):
    def _parse_data(self):
        super(SY85Voice, self)._parse_data()
        start = self._data_offset + 119
        self.waveform_bank = ord(self._data[start:start+1]) & 3
        self.waveform_number = read_midi_short(self._data[start+1:start+3])

    def __repr__(self):
        return super(SY85Voice, self).__repr__() + ", Waveform: %s-%s (%i)" % (
            WAVEFORM_BANKS[self.waveform_bank][0], self.waveform,
            self.waveform_number)

    @property
    def waveform(self):
        return WAVEFORM_NAMES[self.waveform_bank][self.waveform_number-1]


class SY85Performance(SY85AbstractVoice):
    pass


class SY85Multi(SY85Patch):
    def mk_filename(self, prefix=''):
        return "%s %s-%02i %s" % (prefix, self.type[4:], self.program_number,
            self.name)

    def __repr__(self):
        return super(SY85Multi, self).__repr__() + \
            ' Slot: %i' % self.program_number


class SY85Sample(SY85Patch):
    def mk_filename(self, prefix=''):
        return "%s %s-%02i %s" % (prefix, self.type[4:], self.program_number,
            self.name)

    def __repr__(self):
        return super(SY85Sample, self).__repr__() + \
            ' Slot: %i' % self.program_number
