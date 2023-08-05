#!/usr/bin/env python
# -* coding: utf-8 -*-
"""Extract information from a Yamaha SY85 synthesizer disk file."""

__program__ = 'sy85info'
__author__ = 'Christopher Arndt'
__version__ = '1.0b'
__date__ = '$Date: 2010-04-11 23:36:28 +0200 (So, 11. Apr 2010) $'
__revision__ = '$Rev: 441 $'
__copyright__ = '(c) 2010 Christopher Arndt'
__license__ = 'MIT licence'


__usage__ = """\
Usage: %prog [OPTIONS] INPUTFILE...

INPUTFILE is a SY85 disk file (file name extension '.G??', where ?? is a number
01 - 99) containing SY85ALL or SY85SYNALL and, optionally, SY85SEQ and
SY85WVALL data.
"""

# standard library imports
#import logging
import os
import sys

from optparse import OptionParser

from sy85.data.patches import *

def slotname(idx):
    """Return name of bank and program slot for given program number 0..63."""
    bank = "ABCDEFGH"[idx / 8]
    program = idx % 8 + 1
    return "%s%s" % (bank, program)

def parse_perf_bank(data, pos):
    """Extract bank of performances from given data.

    Returns a list of 64 SY85Performance instances.

    """
    bank = []
    for i in range(NUM_PERF):
        perf = SY85Performance(data[pos:pos+SY85Performance.data_len])
        bank.append(perf)
        pos += SY85Performance.data_len
    return pos, bank

def parse_vce_bank(data, pos):
    """Extract bank of voices from given data.

    Returns a list of 63 SY85Voice instances and one SY85DrumVoice instance.

    """
    bank = []
    for i in range(NUM_VCE):
        if i < 63:
            class_ = SY85Voice
        else:
            class_ = SY85DrumVoice
        vce = class_(data[pos:pos + class_.data_len])
        bank.append(vce)
        pos += class_.data_len
    return pos, bank

def parse_multis(data, pos):
    """Extract bank of multi setups from given data.

    Returns a list of 10 SY85Multi instances.

    """
    bank = []
    for i in range(NUM_MULTI):
        multi = SY85Multi(data[pos:pos + SY85Multi.data_len])
        bank.append(multi)
        pos += SY85Multi.data_len
    return pos, bank

def parse_waveforms(data, pos):
    """Extract waveforms from given data.

    Returns a list of up to 64 SY85Waveform instances.

    """
    bank = []
    start = pos
    for i in range(NUM_WAVE):
        wavename = data[pos:pos + SY85Waveform.name_len]
        pos += SY85Waveform.name_len
        if ord(data[start + 0x240 + i*2]) != 0:
            wave = SY85Waveform(wavename)
            bank.append(wave)
    return pos, bank

def parse_dump(data):
    """Parse SY85 SY85All data and extract performances, voices, multis and
    waveforms.

    Returns a SY85All instance.

    """
    if not data.startswith('SY85ALL') or data.startswith('SY85SYNALL'):
        raise ValueError('Invalid data: incorrect file header.')

    dump = SY85All()

    # Internal 1 performances
    pos, bank = parse_perf_bank(data, PERF_OFFSET)
    dump.performances.append(bank)

    # 0-byte padding
    pos += 160

    # Internal 1 voices
    pos, bank = parse_vce_bank(data, pos)
    dump.voices.append(bank)
    # Internal 2 voices
    pos, bank = parse_vce_bank(data, pos)
    dump.voices.append(bank)

    # 0-byte padding
    pos += 340

    # Internal 2 performances
    pos, bank = parse_perf_bank(data, pos)
    dump.performances.append(bank)

    # 0-byte padding
    pos += 160

    # Internal 3 voices
    pos, bank = parse_vce_bank(data, pos)
    dump.voices.append(bank)
    # Internal 4 voices
    pos, bank = parse_vce_bank(data, pos)
    dump.voices.append(bank)

    if data[MULTI_OFFSET:MULTI_OFFSET+7] == 'SY85SEQ':
        pos = MULTI_OFFSET + 0x40
        pos, bank = parse_multis(data, pos)
        dump.multis = bank
        # XXX: not implemented yet
        #pos, bank = parse_patterns(data, pos)

    wave_offset = data[pos:].find('SY85WVALL')
    if wave_offset >= 0:
        pos += wave_offset + 0x20
        pos, bank = parse_waveforms(data, pos)
        dump.waveforms = bank

    return dump

class Bunch(dict):
    """Simple but handy collector of a bunch of named stuff."""

    def __repr__(self):
        keys = self.keys()
        keys.sort()
        args = ', '.join(['%s=%r' % (key, self[key]) for key in keys])
        return '%s(%s)' % (self.__class__.__name__, args)

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)

    __setattr__ = dict.__setitem__

    def __delattr__(self, name):
        try:
            del self[name]
        except KeyError:
            raise AttributeError(name)

class SY85Object(Bunch):
    """Abstract base class for SY85 patch data objects."""

    name_offset = PERF_NAME_OFFSET
    name_len = PERF_NAME_LEN

    def __init__(self, data, *args, **kw):
        super(SY85Object, self).__init__(*args, **kw)
        self._parse_data(data)

    def _parse_data(self, data):
        self.name = data[self.name_offset:self.name_offset + self.name_len].strip()
        self.data = data

class SY85Performance(SY85Object):
    """A SY85 performance program patch.

    A performance contains 4 voice layers, which reference voice slots in
    the (internal, preset or card) voice banks.

    """
    name_offset = PERF_NAME_OFFSET
    name_len = PERF_NAME_LEN
    data_len = PERF_DATA_LEN

    def _parse_data(self, data):
        super(SY85Performance, self)._parse_data(data)
        self.layers = []
        for i in range(4):
            layer_offset = LAYER_DATA_OFFSET+i*LAYER_DATA_LEN
            layer_data = self.data[layer_offset:layer_offset+LAYER_DATA_LEN]
            self.layers.append(SY85Layer(layer_data))

class SY85Layer(SY85Object):
    """A SY85 performance voice layer.

    This references a voice slot by bank and program number and can be
    active or de-activated. If the 'preset' attribute is True, the referenced
    voice is from the preset banks (TG500 only).

    """
    def _parse_data(self, data):
        self.active = bool(ord(data[1]) & 128)
        self.program = ord(data[1]) & 127
        self.bank = ord(data[0]) & 3
        self.preset = bool(ord(data[0]) & 8)
        self.data = data

class SY85Voice(SY85Object):
    """A SY85 voice program patch.

    A voice has a single oscillator, which uses a preset, internal (i.e. from
    sample memory) or card waveform.

    """
    name_offset = VCE_NAME_OFFSET
    name_len = VCE_NAME_LEN
    data_len = VCE_DATA_LEN

    def _parse_data(self, data):
        super(SY85Voice, self)._parse_data(data)
        self.wavebank = ord(self.data[87]) & 3
        self.waveform = ord(self.data[88])

class SY85DrumVoice(SY85Object):
    """A SY85 drum voice program patch.

    A drum voice is always stored in slot H8 of a voice bank and can use a
    different waveform, effect level, panning etc. for each note.

    """
    data_len = DVCE_DATA_LEN

class SY85Multi(SY85Object):
    """A SY85 multi setup program patch.

    A multi is multi-timbral setup of 16 performances or voices assigned to
    the 8 sequencer tracks (plus drum track no. 9) and mapped to the 16 MIDI
    channels.

    """
    data_len = 198

class SY85Pattern(SY85Object):
    """A SY85 drum pattern for the drum track (no.9 of the SY85's sequencer.

    Not supported by the TG500.

    """
    data_len = 198

class SY85Waveform(SY85Object):
    """A SY85 waveform from the preset ROM, card ROM or sample RAM.

    A waveform is a multi-sample, i.e. a collection of individual samples
    mapped accross the keyboard.

    """
    data_len = 8
    name_offset = 0


class SY85All(Bunch):
    """Container for all objects in a SY86All data file.

    A SY85All file contains two banks of 64 performances, four banks of 63
    voices plus one drum voice and optionally 10 multi setups, sequencer data
    drum patterns and custom waveforms and samples.

    """
    def __init__(self):
        self.performances = []
        self.voices = []
        self.multis = []
        self.patterns = []
        self.waveforms = []

    def get_waveform_name(self, wavebank, waveform=None, default='<unknown>'):
        """Return name of waveform given by wavebank and waveform number.

        If the first argument is a SY85Voice instance, the wavebank and
        waveform number will be the ones referenced by that voice. If the
        wavebank number refers to the internal waveform bank (i.e 3 = sample
        RAM), the waveform name will be looked up in the list of waveform
        objects in this instance's 'waveforms' attribute, else in the list of
        ROM preset waveforms. If it is not found there either (probably a
        waveform from a PCM ROM card), the optional 'default' argument is
        returned (defaults to '<unknown>').

        """
        if isinstance(wavebank, SY85Voice):
            waveform = wavebank.waveform
            wavebank = wavebank.wavebank
        try:
            if wavebank == 3:
                return self.waveforms[waveform]['name'] + '*'
            else:
                return WAVEFORM_NAMES[wavebank][waveform-1]
        except LookupError:
             return default

    def get_voice_name(self, bank, program=None, default='<unknown>',
            preset=False):
        """Return name of voice given by bank and program number.

        If the first instance is a SY86Layer instance, the bank and program
        number will be the ones referenced by that layer. If the optional
        'preset' argument (default: False) or the corresponding attribute on
        a given SY85Layer instance is True, the voice name is looked up from
        the list of voice names in the preset banks (TG500 only), else in the
        banks stored in this instance's 'banks' attribute. If it is not found
        there either (probably a voice from a RAM/ROM card), the optional
        'default' argument is returned (defaults to '<unknown>').

        """
        if isinstance(bank, SY85Layer):
            program = bank.program
            preset = bank.preset
            bank = bank.bank
        try:
            if preset:
                return PRESET_VOICE_NAMES[bank][program]
            else:
                return self.voices[bank][program].name
        except LookupError:
             return default

    def format(self, formatter):
        """Format the data of this instance with the given formatter object.

        A formatter is an object that provides several methods that will be
        called when iterating over the data. Look at the 'BankPrinter' class
        for a simaple example, which prints a listing of all stored objects
        to standard out.

        """
        formatter.start_dump()
        formatter.start_section("perf")
        self.format_banks(formatter, self.performances)
        formatter.end_section("perf")
        formatter.start_section("voice")
        self.format_banks(formatter, self.voices)
        formatter.end_section("voice")
        if self.multis:
            formatter.start_section("multi")
            self.format_banks(formatter, [self.multis])
            formatter.end_section("multi")
        if self.waveforms:
            formatter.start_section("wave")
            self.format_banks(formatter, [self.waveforms])
            formatter.end_section("wave")
        formatter.end_dump()

    def format_banks(self, formatter, banks):
        """Format given banks of performances, voices, multis or waveforms
        using formatter.

        This will iterate over each bank and each object in each bank. At the
        start of each bank the 'start_bank' method of the formatter is called
        and passed the bank number. Then an appropriate 'handle_*' method is
        called on the formatter for each object in the bank, where '*' is a
        short name of the object to handle, e.g. 'handle_voice'. Formatter
        objects must support 'handle_*' methods for the following object types:

        * performance
        * voice
        * drumvoice
        * multi
        * pattern
        * waveform

        Each method is passed a dictionary with the data of the object to
        format.

        """
        for bankno, bank in enumerate(banks):
            formatter.start_bank(bankno)

            for i, patch in enumerate(bank):
                data = dict(no=i)
                data.update(patch)
                if isinstance(patch, (SY85Performance, SY85Voice, SY85DrumVoice)):
                    data['slot'] = slotname(i)
                if isinstance(patch, SY85Voice):
                    data['waveformname'] = self.get_waveform_name(patch)
                    formatter.handle_voice(data)
                elif isinstance(patch, SY85DrumVoice):
                    formatter.handle_drumvoice(data)
                elif isinstance(patch, SY85Performance):
                    data['layernames'] = []
                    for layer in patch.layers:
                        name = self.get_voice_name(layer)
                        data['layernames'].append(name)
                    formatter.handle_performance(data)
                elif isinstance(patch, SY85Multi):
                    formatter.handle_multi(data)
                elif isinstance(patch, SY85Pattern):
                    formatter.handle_pattern(data)
                elif isinstance(patch, SY85Waveform):
                    formatter.handle_waveform(data)

            formatter.end_bank(bankno)

class BankPrinter(object):
    """Formatter for printing a listing of a SY85All object."""

    sections = {
        'perf': "Performances",
        'voice': "Voices",
        'multi': "Multi Setups",
        'wave': "Waveforms"
    }

    def __init__(self, stream=sys.stdout, **kw):
        self.cur_sect = None
        self.stream = stream
        self.data = kw

    def write(self, s, ln=True):
        self.stream.write(s + '\n' if ln else '')

    def start_dump(self):
        if 'filename' in self.data:
            self.write("Filename: %s" % os.path.basename(self.data['filename']))
            self.write('')

    def end_dump(self):
        pass

    def start_section(self, type):
        self.cur_sect = type
        caption = self.sections.get(type, 'Unknown Type')
        self.write(caption)
        self.write("=" * len(caption))
        self.write('')

    def end_section(self, type):
        self.cur_sect = None
        self.write('')

    def start_bank(self, bankno):
        if self.cur_sect not in ('voice', 'perf'):
            return
        try:
            caption = PATCH_BANKS.get(self.cur_sect, [])[bankno][1]
        except (IndexError, ValueError):
            caption = 'Invalid Bank'
        self.write(caption)
        self.write("-" * len(caption))
        self.write('')

    def end_bank(self, bankno):
        self.write('')

    def handle_voice(self, data):
        data['wave'] = "%s-%03i %s" % (WAVEFORM_BANKS[data['wavebank']][0],
            data['waveform'], data['waveformname'])
        self.write("%(no)02i: %(slot)s - %(name)-8s\t%(wave)s" % data)

    def handle_performance(self, data):
        layers = []
        for i, layer in enumerate(data['layers']):
            if layer.active:
                slot = slotname(layer.program)
                bank = PATCH_BANKS['voice'][layer.bank][0]
                layers.append("%s-%s %s" % (
                    bank, slot, data['layernames'][i]))
            else:
                layers.append("<off>")
        data['layers'] = ", ".join(layers)
        self.write("%(no)02i: %(slot)s - %(name)-8s\t%(layers)s" % data)

    def handle_drumvoice(self, data):
        self.write("%(no)02i: %(slot)s - %(name)-8s\t(Drum voice)" % data)

    def handle_multi(self, data):
        data['no'] += 1
        self.write("%(no)02i: %(name)-8s" % data)

    def handle_waveform(self, data):
        data['no'] += 1
        self.write("%(no)02i: %(name)-8s" % data)

    def handle_pattern(self, data):
        pass

def main(args):
    optparser = OptionParser(prog=__program__, usage=__usage__,
      version=__version__, description=__doc__)
    optparser.add_option("-o", "--output", metavar="FILE",
      dest="outfile", help="Write output to FILE (default: standard out).")
    # XXX: Not implemented yet
    #optparser.add_option("-v", "--verbose",
    #  action="store_true", dest="verbose", default=False,
    #  help="Print what's going on to stdout.")
    #optparser.add_option("--csv",
    #    action="store_true", dest="csv",
    #    help="Format listing as comma-separated values (CVS).")

    (options, args) = optparser.parse_args(args=args)

    if not args:
        optparser.print_help()
        return 2
    else:
        infile = args.pop(0)

    # XXX: Not implemented yet
    #if options.verbose:
    #    logging.basicConfig(level=logging.DEBUG)
    #else:
    #    logging.basicConfig(level=logging.WARNING)

    try:
        data = open(infile, 'rb').read()
    except:
        print sys.stderr, "Could not read input file '%s'." % infile
        return 1

    if options.outfile:
        outstream = open(options.outfile, 'w')
    else:
        outstream = sys.stdout

    try:
        dump = parse_dump(data)
        dump.format(BankPrinter(outstream, filename=infile))
    finally:
        if options.outfile:
            outstream.close()

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
