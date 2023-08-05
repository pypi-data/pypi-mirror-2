# -*- coding: UTF-8 -*-
"""Generic functions for reading/writing binary data with arbitrary
fixed-field-length formats.
"""

import converters
import logging

from data import voice

SOX = '\xF0'
MANUFACTURER_ID = '\x43'

class NullHandler(logging.Handler):
    def emit(self, record):
        pass

log = logging.getLogger(__name__)
log.addHandler(NullHandler())

def is_yamaha_sysex(data):
    """Return True if given data looks like a Yamaha sysex bulk dump."""
    return len(data) >= 8 and data.startswith(SOX + MANUFACTURER_ID)

def read_patch(data, format):
    """Parse given binary data according to format specified in format.

    Returns a dictionary with data field number as key and an 2-item tuple
    with the data field name and the converted data field value as the value.

    """
    def add_value(patch, param_no, name, value):
        if isinstance(value, tuple):
            value = (name,) + value
        else:
            value = (name, value)
        if param_no in patch:
            if not isinstance(patch[param_no], list):
                patch[param_no] = [patch[param_no]]
            patch[param_no].append(value)
        else:
            patch[param_no] = value

    patch = dict()
    for line in format:
        offset, length, param_no, name, cv_func_name = line[:5]
        if param_no is None:
            continue
        cv_func_args = line[5:]
        cv_func = getattr(converters, cv_func_name)
        value = data[line[0]:line[0]+line[1]]
        try:
            # some patch formats have several settings stored in a bitfield
            # under the same parameter number. We collect them in a list.
            value = cv_func(value, *cv_func_args)
            add_value(patch, param_no, name, value)
        except Exception, exc:
            log.error("Exception while calling converter function '%s' for "
                "param #%i (offset %i). Saving raw binary value.\nError: %s",
                cv_func_name, param_no, offset, exc)
            log.debug("Raw value: %r", value)
            add_value(patch, param_no, name, value)
            raise
    return patch

def make_logger():
    # define a Handler which writes INFO messages or higher to the sys.stderr
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    # set a format which is simpler for console use
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    # tell the handler to use this format
    console.setFormatter(formatter)
    # add the handler to the root logger
    logging.getLogger(__name__).addHandler(console)
    return console


if __name__ == '__main__':
    import sys
    import pprint

    make_logger()

    syx = open(sys.argv[1], 'rb').read()
    if is_yamaha_sysex(syx):
        try:
            vc = read_patch(syx[32:-2], voice.VOICE_SYSEX_FORMAT)
            pprint.pprint(vc)
        except Exception, exc:
            print "Voice parsing failed: %s" % exc
            raise
    else:
        print "Sysex format not recognized."
        sys.exit(2)
