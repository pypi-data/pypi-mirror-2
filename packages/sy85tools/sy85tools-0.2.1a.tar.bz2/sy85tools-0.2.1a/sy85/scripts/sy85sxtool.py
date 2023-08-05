#!/usr/bin/env python
"""A command line tool to handle MIDI sysex dumps from the Yamaha SY85 synth."""

__program__ = 'sy85sxtool'
__author__ = 'Christopher Arndt'
__version__ = '1.0'
__date__ = '$Date: 2010-04-11 20:26:35 +0200 (Sun, 11. Apr 2010) $'
__revision__ = '$Rev: 440 $'
__copyright__ = '(c) 2009 Christopher Arndt'
__license__ = 'MIT licence'

__usage__ = """\
Usage: %prog [OPTIONS] COMMAND FILE...

where COMMAND is one of 'list', 'explode', 'rename'. Use 'help COMMAND'
to show the help message for a given command.\
"""

# standard library imports
import logging
import os
import sys

from optparse import OptionParser

# private modules
from sysex import *


# functions

def read_sysex_file(filename, strict=False):
    try:
        return SY85SysexContainer.fromfile(filename, strict)
    except SysexParseError, exc:
        logging.error("Error parsing file '%s': %s", filename, exc)
    except (IOError, OSError), exc:
        logging.error("Could not open file '%s': %s", filename, exc)

def save_chunk_to_file(chunk, filename, overwrite=False):
    """Save a sysex chunk to a file with given filename."""
    if not os.path.exists(filename) or overwrite:
        try:
            fo = open(filename, 'wb')
        except (OSError, IOError), exc:
            logging.error("Could not open file '%s' for writing: %s",
                filename, exc)
        else:
            fo.write(chunk.dump())
            fo.close()
    else:
        logging.warning("File '%s' already exists. Not overwriting.", filename)

# command functions

def do_explode(args, options):
    """Read SY95 sysex dump(s) and write out separate files for each chunk.

    sy85sxtool [-f|--force] [--strict] [-o|--output=DIR] explode FILE...

    Each chunk will be written to a file with a name according to the following
    format: CCC TT-BB-SS NN.syx

    CCC = Chunk number, e.g. "064" (3 digits)
    TT  = Type code, e.g. "VC" (=Voice) or "MU" (=Multi) (2 chars)
    BB  = Bank type and number, e.g. "I2" (1 char, one digit) (if applicable)
    SS  = Slot, e.g. "A4" or "G6" (1 char, one digit) (if applicable)
    NN  = Name or denomination, e.g. "SP Makro" or "Seq Dump" (up to 8 chars)

    """
    if not args:
        do_help('explode')
    for fn in args:
        logging.info("Processing file: %s...", fn)
        syx = read_sysex_file(fn, options.strict)
        if not syx: continue
        for i, chunk in enumerate(syx.chunks):
            outfn = chunk.mk_filename("%03i" % i) + '.syx'
            if options.outfile:
                outfn = os.path.join(options.outfile, outfn)
            logging.info("Writing chunk %03i to file '%s'.", i, outfn)
            save_chunk_to_file(chunk, outfn, options.overwrite)
        logging.info("Chunks written: %03i", i+1)

def do_help(args, options=None):
    """Print help message for given action name."""
    try:
        if isinstance(args, list):
            args = args.pop(0)
        helptext = ACTIONS[args].__doc__.strip()
        if helptext:
            print helptext
        else:
            print "There is no help available for this command."
        print ("\nUse option --help for general help on available options and "
            "their explanation.")
    except IndexError:
        print "Use 'help COMMAND' to show the help message for COMMAND."
    except KeyError, exc:
        print "Unknown commmand %s" % exc
        return 2

def do_list(args, options):
    """Read SY95 sysex dump(s) and list information about each contained chunk.

    sy85sxtool [--strict] [-o|--output=FILE [-f|--force]] [--csv] list FILE...

    In plain text format, for each chunk the following info is listed:

    Chunk: <chunk no.> Name: <name> Type: <type>

    For (drum) voices and performances additionally:

    Bank: <bank>, Slot: <group><program> (<program no.>)

    For multis and samples:

    Slot: <program no.>

    """
    if not args:
        do_help('list')
    if options.outfile:
        if not os.path.exists(options.outfile) or options.overwrite:
            try:
                outfile = open(options.outfile, 'w')
            except (IOError, OSError):
                logging.error("Could not open file '%s' for writing.",
                    options.outfile)
                return 1
        else:
            logging.error("File '%s' already exists. Use -f to overwrite.",
                options.outfile)
            return 1
    else:
        outfile = sys.stdout
    if options.voices:
        options.csv_fields = CSV_FIELDS_VOICE
    else:
        options.csv_fields = CSV_FIELDS_PATCH

    if options.csv:
        import csv
        csv_fields = CSV_FIELDS_COMMON + options.csv_fields
        csvwriter = csv.writer(outfile)
        csvwriter.writerow([x[1] for x in csv_fields])
    for fn in args:
        bn = os.path.basename(fn)
        if not options.csv:
            outfile.write("File: %s\n" % bn)
            outfile.write("-" * (6+len(bn)) + '\n')
        syx = read_sysex_file(fn, options.strict)
        if not syx: continue
        i = 0
        for i, chunk in enumerate(syx.chunks):
            if options.voices and chunk.type != '0065VC':
                continue
            if options.csv:
                csv_values = [bn, i, len(chunk)] + [getattr(chunk, n, None)
                    for n in [x[0] for x in csv_fields] if n]
                csvwriter.writerow(csv_values)
            else:
                logging.debug("Listing chunk %i, type %s", i, chunk.type)
                outfile.write("Chunk %03i: %r\n" % (i, chunk))
        if not options.csv:
            outfile.write("Total number of valid chunks: %03i\n" % (i+1,))
    if not outfile is sys.stdout:
        outfile.close()

def do_rename(args, options):
    """Rename the given (drum) voice, performance, multi or sample.

    sy85sxtool [-f|--force] [--strict] [-o|--output=FILE] rename \
                                        FILE [CHUNK-NUMBER|OLDNAME] NEWNAME

    Examples:

        sy85sxtool -o customset.syx rename factory.syx 0 'SP Mikro'

    or:

        sy85sxtool -o co_cream.syx rename co_dream.syx 'CO Cream'

    or:

        sy85sxtool -o customset.syx rename factory.syx 'CO Dream' 'CO Test'

    """
    if not len(args) >= 2:
        do_help('rename')
        return 2
    syx = read_sysex_file(args.pop(0), options.strict)
    if len(args) >= 2:
        try:
            chunk_no = int(args[0])
        except ValueError:
            logging.error("Invalid chunk number")
            return 1
        name = args[1]
    else:
        chunk_no = None
        name = args[0]
    if syx:
        for i, chunk in enumerate(syx.chunks):
            if chunk_no is None:
                chunk.name = name[:8]
                break
            elif i == chunk_no:
                chunk.name = name[:8]
                break
            #else:
            #    loggin.error("Sysex file contains more than one chunk. "
            #        "You must specify a chunk number to rename")
        if options.outfile and os.path.exists(options.outfile) and \
                not options.overwrite:
            loggin.error("File '%s' already exists. Not overwriting.",
                options.outfile)
        else:
            newsyx = syx.dump(options.outfile)
            if not options.outfile:
                sys.stdout.write(newsyx)

# map command line COMMAND names to functions which handle each action

ACTIONS = dict(
    explode = do_explode,
    help = do_help,
    list = do_list,
    rename = do_rename,
)


# main programm entry point

def main(args):
    optparser = OptionParser(prog=__program__, usage=__usage__,
      version=__version__, description=__doc__)
    optparser.add_option("-v", "--verbose",
      action="store_true", dest="verbose", default=False,
      help="Print what's going on to stdout.")
    optparser.add_option("--strict",
      action="store_true", dest="strict",
      help="Use strict sysex parsing and abort on parsing errors.")
    optparser.add_option("-o", "--output", metavar="PATH",
      dest="outfile", help="Write output to PATH.")
    optparser.add_option("-f", "--force",
        action="store_true", dest="overwrite",
        help="Overwrite existing files.")
    optparser.add_option("--csv",
        action="store_true", dest="csv",
        help="Format chunk list as comma-separated values (CVS).")
    optparser.add_option("--voices",
        action="store_true", dest="voices",
        help="List only voices.")

    (options, args) = optparser.parse_args(args=args)

    if options.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.WARNING)

    try:
        return ACTIONS[args.pop(0)](args, options)
    except (IndexError, KeyError), exc:
        raise
        logging.warning(exc)
        optparser.print_help()
        return 2


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]) or 0)
