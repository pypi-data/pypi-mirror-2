from data.patches import *

SOX = '\xF0'
EOX = '\xF7'
MANUFACTURER_ID = '\x43'
MSG_ID_BULK_DUMP = '\x7A'
MSG_ID_NSEQ_DUMP = '\x0A'

BULKDATATYPES = {
    '0040SA': dict(
        name='Sample',
        msg_fmt_id=MSG_ID_BULK_DUMP,
        classname='SY85Sample'),
    '0065DR': dict(
        name='Drumvoice',
        msg_fmt_id=MSG_ID_BULK_DUMP,
        classname='SY85AbstractVoice'),
    '0065MU': dict(
        name='Multi',
        msg_fmt_id=MSG_ID_BULK_DUMP,
        classname='SY85Multi'),
    '0065PF': dict(
        name='Performance',
        msg_fmt_id=MSG_ID_BULK_DUMP,
        classname='SY85Performance'),
    '0065RY': dict(
        name='Rhythm',
        msg_fmt_id=MSG_ID_BULK_DUMP,
        classname='SY85Rhythm'),
    '0065SS': dict(
        name='Seq Setup',
        msg_fmt_id=MSG_ID_BULK_DUMP,
        classname='SY85Setup'),
    '0065SQ': dict(
        name='Seq Dump',
        msg_fmt_id=MSG_ID_BULK_DUMP,
        classname='SY85SeqDump'),
    # SY-85
    '0065SY': dict(
        name='Synth Setup',
        msg_fmt_id=MSG_ID_BULK_DUMP,
        classname='SY85Setup'),
    '0065VC': dict(
        name='Voice',
        msg_fmt_id=MSG_ID_BULK_DUMP,
        classname='SY85Voice'),
    # TG-500
    '0066SY': dict(
        name="Synth Setup",
        msg_fmt_id=MSG_ID_BULK_DUMP,
        classname='SY85Setup'),
    'NSEQ  ': dict(
        name='Song',
        msg_fmt_id=MSG_ID_NSEQ_DUMP,
        classname='SY85TrackData'),
    'NSEQ1 ': dict(
        name='Song',
        msg_fmt_id=MSG_ID_NSEQ_DUMP,
        classname='SY85TrackData'),
}

BANKNAMES = {
    0: ('Internal I', 'I1'),
    1: ('Card I', 'C1'),
    3: ('Internal II', 'I2'),
    4: ('Card II', 'C2'),
    6: ('Internal III', 'I3'),
    7: ('Card III', 'C3'),
    9: ('Internal IV', 'I4'),
   10: ('Card IV', 'C4'),
  127: ('Edit buffer', 'E')
}

CSV_FIELDS_COMMON = [
    (None, 'Filename'),
    (None, 'Chunk no.'),
    (None, 'Length'),
    ('type_name', 'Type'),
    ('name', 'Name')
]

CSV_FIELDS_PATCH = [
    ('bank_number', 'Bank no.'),
    ('bank_name', 'Bank name'),
    ('program_number', 'Program no.'),
    ('slot', 'Slot')
]

CSV_FIELDS_VOICE = CSV_FIELDS_PATCH + [
    ('waveform_number', 'Waveform no.'),
    ('waveform', 'Waveform'),
    ('waveform_bank', 'Waveform bank')
]
