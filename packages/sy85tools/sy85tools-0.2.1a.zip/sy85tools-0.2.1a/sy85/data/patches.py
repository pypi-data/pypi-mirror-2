# -*- coding: UTF-8 -*-
#
# sy85/data/patches.py
#

from itertools import chain


PERF_OFFSET = 0x14a
MULTI_OFFSET = 0x10000

PERF_DATA_LEN = 168
PERF_NAME_LEN = 8
PERF_NAME_OFFSET = 49

LAYER_DATA_OFFSET = 60
LAYER_DATA_LEN = 27

VCE_DATA_LEN = 162
VCE_NAME_LEN = 8
VCE_NAME_OFFSET = 49

DVCE_DATA_LEN = 552

NUM_PERF = 64
NUM_VCE = 64
NUM_MULTI = 10
NUM_WAVE = 64

PATCH_BANKS = {
    'perf': [
        ('I1', 'Internal I'),
        ('I2', 'Internal II'),
    ],
    'voice': [
        ('I1', 'Internal I'),
        ('I2', 'Internal II'),
        ('I3', 'Internal III'),
        ('I4', 'Internal IV'),
    ],
}

WAVEFORM_BANKS = [
    ('P1', 'Preset 1'),
    ('P2', 'Preset 2'),
    ('C', 'Card'),
    ('I', 'Internal')
]

TG500_PRESET_PERF_NAMES = [
    [ # Preset 1
        "CO Dream ", # 00
        "KY Piano ", # 01
        "SP Aztec ", # 02
        "SC Wyrz ", # 03
        "CH Choir ", # 04
        "BA Pick1 ", # 05
        "ST Rosin ", # 06
        "BR Stab ", # 07
        "CO Soire ", # 08
        "OR Bee ", # 09
        "SP Lush ", # 10
        "SC Rude ", # 11
        "CH Breth ", # 12
        "BA Swap ", # 13
        "ST Octvs ", # 14
        "BR Pro5 ", # 15
        "CO Orch ", # 16
        "KY Digi1 ", # 17
        "SP Faery ", # 18
        "SC Talk ", # 19
        "CH OohAh ", # 20
        "BA Pick2 ", # 21
        "ST Pitz ", # 22
        "BR Sfz ", # 23
        "CO Sable ", # 24
        "KY Roady ", # 25
        "SP Slide ", # 26
        "SC Klav ", # 27
        "CH Vespa ", # 28
        "BA -Fret ", # 29
        "ST Rings ", # 30
        "BR Forte ", # 31
        "CO Jazzr ", # 32
        "OR Gimme ", # 33
        "SP Lite ", # 34
        "SC Buzz ", # 35
        "CH Munch ", # 36
        "BA Rezzo ", # 37
        "ST Dark ", # 38
        "BR Saw ", # 39
        "CO E.S.P ", # 40
        "KY Elek ", # 41
        "SP Stars ", # 42
        "SC Snaps ", # 43
        "CH Abyss ", # 44
        "BA Mini ", # 45
        "ST 2002 ", # 46
        "BR Obie ", # 47
        "CO Pnooh ", # 48
        "OR Nave ", # 49
        "SP Ace ", # 50
        "SC Point ", # 51
        "CH Comet ", # 52
        "BA Guppy ", # 53
        "ST Big ", # 54
        "BR Fatti ", # 55
        "CO Inca ", # 56
        "KY Funky ", # 57
        "SP Vekta ", # 58
        "SC Pizza ", # 59
        "CH Oral ", # 60
        "BA Doom ", # 61
        "ST Tron ", # 62
        "BR Swell ", # 63
    ],
    [ # Preset 2
        "CO Ncert ", # 00
        "KY Loud ", # 01
        "SP Carol ", # 02
        "SL Mitey ", # 03
        "ME Orion ", # 04
        "GT Amped ", # 05
        "SE Rolls ", # 06
        "WN Tenor ", # 07
        "CO DXStr ", # 08
        "OR Sine ", # 09
        "SP Venus ", # 10
        "SL Chick ", # 11
        "ME Glitz ", # 12
        "GT Strat ", # 13
        "SE C-tar ", # 14
        "WN Sacks ", # 15
        "CO Stass ", # 16
        "KY Digi2 ", # 17
        "SP Whino ", # 18
        "SL L7 ", # 19
        "ME Honto ", # 20
        "GT Phunk ", # 21
        "SE Xeno ", # 22
        "WN Alto ", # 23
        "CO Megin ", # 24
        "KY Jerry ", # 25
        "SP Hinx ", # 26
        "SL Eazy ", # 27
        "ME Mars ", # 28
        "GT Rock ", # 29
        "SE Storm ", # 30
        "WN Panic ", # 31
        "CO Gospl ", # 32
        "OR Cheap ", # 33
        "SP Pluto ", # 34
        "SC Clank ", # 35
        "ME Ecko ", # 36
        "GT Harm ", # 37
        "SE Zoom ", # 38
        "BR Reeds ", # 39
        "CO Ethos ", # 40
        "KY PnoMW ", # 41
        "SP Synth ", # 42
        "FI Santo ", # 43
        "ME Alien ", # 44
        "GT El12 ", # 45
        "SE Delay ", # 46
        "BR Lips ", # 47
        "CO Kings ", # 48
        "KY Calio ", # 49
        "SP Anlog ", # 50
        "SC Wind ", # 51
        "ME Spark ", # 52
        "GT 12Str ", # 53
        "SE Flies ", # 54
        "BR Miles ", # 55
        "CO Happi ", # 56
        "KY Digi3 ", # 57
        "SP Arpeg ", # 58
        "TP Bells ", # 59
        "ME Hit ", # 60
        "GT Acstc ", # 61
        "SE Hero ", # 62
        "BR Fanfr ", # 63
    ]
]

TG500_INT_PERF_NAMES = [
    [ # Internal 1
        "CO Aster ", # 00
        "AP Piano ", # 01
        "SP Mtrix ", # 02
        "SC Skank ", # 03
        "ME Sprk2 ", # 04
        "BA Drive ", # 05
        "BR Fnfr2 ", # 06
        "SE Devil ", # 07
        "ST Moin ", # 08
        "FI Dulcm ", # 09
        "CO Bells ", # 10
        "KY Knock ", # 11
        "SP Fanta ", # 12
        "SC Elec1 ", # 13
        "ME Gokrk ", # 14
        "BA Susud ", # 15
        "BR Forth ", # 16
        "SE Swmp ", # 17
        "ST Legat ", # 18
        "GT Pedal ", # 19
        "CO Gloom ", # 20
        "OR Cool ", # 21
        "SP Flash ", # 22
        "SC Gob ", # 23
        "ME Max ", # 24
        "BA Sldge ", # 25
        "BR Synth ", # 26
        "SE Wall ", # 27
        "ST Accat ", # 28
        "GT Steel ", # 29
        "CO India ", # 30
        "OR Rock ", # 31
        "SP Atrio ", # 32
        "SC Woody ", # 33
        "ME Chorl ", # 34
        "GT Round ", # 35
        "BR Sfz2 ", # 36
        "SE Rado ", # 37
        "ST LgSm ", # 38
        "SL Meteo ", # 39
        "CO Clock ", # 40
        "OR Mite ", # 41
        "SP Wind ", # 42
        "SC Arred ", # 43
        "ME Chom ", # 44
        "CO FMpad ", # 45
        "BR Tpts ", # 46
        "SE Indst ", # 47
        "CO Nuage ", # 48
        "SP Lodge ", # 49
        "SC Oz ", # 50
        "CO Japan ", # 51
        "KY Hrpzi ", # 52
        "SL Sqsaw ", # 53
        "BR CShrn ", # 54
        "CO Laura ", # 55
        "CO Orch2 ", # 56
        "ME Hits ", # 57
        "ST Solo ", # 58
        "CO Soul ", # 59
        "GT Wires ", # 60
        "OR Pan ", # 61
        "BR 3 Osc ", # 62
        "CO Fire", # 63
    ]
]

PRESET_VOICE_NAMES = [
    [ # Preset I
        "AP Grand", # 00
        "AP Chors", # 01
        "AP Dance", # 02
        "AP Rock", # 03
        "AP Tack", # 04
        "AP Touch", # 05
        "BA Wood", # 06
        "BA Pitz", # 07
        "BA Fingr", # 08
        "BA Frtls", # 09
        "BA Pick1", # 10
        "BA Pick2", # 11
        "BA Slap", # 12
        "BA Thump", # 13
        "BA Syn 1", # 14
        "BA Syn 2", # 15
        "BA Syn 3", # 16
        "BA Syn 4", # 17
        "BA Syn 5", # 18
        "BA Syn 6", # 19
        "BA Syn 7", # 20
        "BA Syn 8", # 21
        "BA Syn 9", # 22
        "BA Syn 10", # 23
        "BA Syn 11", # 24
        "BA Syn 12", # 25
        "BR Trump", # 26
        "BR Mute", # 27
        "BR Horn", # 28
        "BR Tromb", # 29
        "BR Tuba", # 30
        "BR TpEns", # 31
        "BR Tpts", # 32
        "BR TpSfz", # 33
        "BR Stab", # 34
        "BR EnsSF", # 35
        "BR East", # 36
        "BR Syn 1", # 37
        "BR Syn 2", # 38
        "BR Syn 3", # 39
        "BR Syn 4", # 40
        "BR Saw", # 41
        "BR SawSF", # 42
        "BR Swell", # 43
        "BR Tooth", # 44
        "BR Rezz", # 45
        "BR Toto", # 46
        "BR Wow", # 47
        "CH Aah", # 48
        "CH Ooh", # 49
        "CH Pure", # 50
        "CH Breth", # 51
        "CH Ghost", # 52
        "CH Quire", # 53
        "CH Vespa", # 54
        "CH Vocod", # 55
        "Fl Blue1", # 56
        "Fl Blue2", # 57
        "Fl Dudel", # 58
        "Fl DulcD", # 59
        "Fl DulcM", # 60
        "Fl Harp", # 61
        "Fl Kalim", # 62
        "DR Kit", # 63
    ],
    [ # Preset II
        "Fl Lip", # 00
        "Fl Sitar", # 01
        "GT Nylon", # 02
        "GT Dark", # 03
        "GT Steel", # 04
        "GT 12Str", # 05
        "GT Jazz", # 06
        "GT Strt1", # 07
        "GT Strt2", # 08
        "GT Strt3", # 09
        "GT Mute", # 10
        "GT Harm", # 11
        "GT Comp1", # 12
        "GT Comp2", # 13
        "GT Dist", # 14
        "GT Warm", # 15
        "GT Wah", # 16
        "GT Feed", # 17
        "KY EP 1", # 18
        "KY EP 2", # 19
        "KY EP 3", # 20
        "KY EP 4", # 21
        "KY EP 5", # 22
        "KY EP 6", # 23
        "KY EP 7", # 24
        "KY EP 8", # 25
        "KY EP 9", # 26
        "KY EP 10", # 27
        "KY EP 11", # 28
        "KY EP 12", # 29
        "KY Clav1", # 30
        "KY Clav2", # 31
        "KY Hrpsi", # 32
        "KY Acrdn", # 33
        "KY Cali1", # 34
        "KY Cali2", # 35
        "ME Bottl", # 36
        "ME Gizmo", # 37
        "ME Grind", # 38
        "ME Hand", # 39
        "ME Kali", # 40
        "ME Mello", # 41
        "ME Orch1", # 42
        "ME Orch2", # 43
        "ME OrchR", # 44
        "ME Soro", # 45
        "ME Templ", # 46
        "ME Tink", # 47
        "ME Tomi", # 48
        "ME Voics", # 49
        "OR Jaz B", # 50
        "OR Smoke", # 51
        "OR Airy", # 52
        "OR Dist", # 53
        "OR Cheap", # 54
        "OR Pipes", # 55
        "OR Click", # 56
        "OR Perc", # 57
        "SC Aha!", # 58
        "SC Bari", # 59
        "SC Bell", # 60
        "SC Clav", # 61
        "SC Digi1", # 62
        "DR Zones", # 63
    ],
    [ # Preset III
        "SC Digi2", # 00
        "SC Digi3", # 01
        "SC Ecko", # 02
        "SC Fingr", # 03
        "SC Housy", # 04
        "SC Jrney", # 05
        "SC Metal", # 06
        "SC Mute", # 07
        "SC Pan", # 08
        "SC Perc", # 09
        "SC Rezz", # 10
        "SC Spike", # 11
        "SC Sqiff", # 12
        "SC Synnr", # 13
        "SC Topia", # 14
        "SC Vocal", # 15
        "SC Vox", # 16
        "SC Wires", # 17
        "SC Wondr", # 18
        "SE Alert", # 19
        "SE Templ", # 20
        "SE BDup", # 21
        "SE Chou", # 22
        "SE Demon", # 23
        "SE Dropr", # 24
        "SE Gobln", # 25
        "SE Heli", # 26
        "SE Hell", # 27
        "SE Hyena", # 28
        "SE Indus", # 29
        "SE It", # 30
        "SE Noize", # 31
        "SE Pops", # 32
        "SE Rain", # 33
        "SE Rezo", # 34
        "SE S&H", # 35
        "SE Star", # 36
        "SE Up&Up", # 37
        "SE Wind", # 38
        "SL Cutty", # 39
        "SL Digi", # 40
        "SL Dist", # 41
        "SL Hamma", # 42
        "SL Lead", # 43
        "SL Lyle", # 44
        "SL Pulse", # 45
        "SL Saw 1", # 46
        "SL Saw 2", # 47
        "SL Squar", # 48
        "SL Sync", # 49
        "SL Whisl", # 50
        "SP Abyss", # 51
        "SP Big", # 52
        "SP Exita", # 53
        "SP Freqs", # 54
        "SP Glass", # 55
        "SP Goner", # 56
        "SP Hyper", # 57
        "SP Makro", # 58
        "SP Mello", # 59
        "SP Movie", # 60
        "SP Nasty", # 61
        "SP Nehan", # 62
        "DR GMIDI", #63
    ],
    [ # Preset IV
        "SP Paddy", # 00
        "SP Phaze", # 01
        "SP Poly", # 02
        "SP SawSt", # 03
        "SP Slow", # 04
        "SP Smoky", # 05
        "SP Space", # 06
        "SP Sqare", # 07
        "SP Sweep", # 08
        "SP Sweet", # 09
        "SP Vizon", # 10
        "SP Wine", # 11
        "ST Violn", # 12
        "ST JeanL", # 13
        "ST Sectn", # 14
        "ST Power", # 15
        "ST Deep", # 16
        "ST Dark", # 17
        "ST Brite", # 18
        "ST Arco", # 19
        "ST Sfz", # 20
        "ST Pizz", # 21
        "ST Tron", # 22
        "ST Anlog", # 23
        "ST Sizzl", # 24
        "ST Synth", # 25
        "ST Thin", # 26
        "ST Combo", # 27
        "TP Glock", # 28
        "TP Xylo", # 29
        "TP Vibes", # 30
        "TP Tubal", # 31
        "TP Hands", # 32
        "TP Siam", # 33
        "TP Steel", # 34
        "TP Loggy", # 35
        "TP Bambu", # 36
        "TP Mrmba", # 37
        "TP Timp", # 38
        "TP Syn", # 39
        "TP SynDr", # 40
        "TP Tinkl", # 41
        "TP Agone", # 42
        "TP Angle", # 43
        "WN Sopr", # 44
        "WN Alto", # 45
        "WN Tenor", # 46
        "WN Bari", # 47
        "WN SaxSF", # 48
        "WN Picc", # 49
        "WN Flute", # 50
        "WN Pan", # 51
        "WN Clari", # 52
        "WN Oboe", # 53
        "WN Basso", # 54
        "WN Recor", # 55
        "WN Breth", # 56
        "Ml Crash", # 57
        "MI EPNP", # 58
        "Ml Hiss", # 59
        "Ml Ride", # 60
        "MW EGBia", # 61
        "AT EGBia", # 62
        "DR Efect", # 63
    ]
]

TG500_INTERNAL_VOICE_NAMES = [
    [ # Internal I
        "AP Brite", # 00
        "AP Dark", # 01
        "AP Chrs2", # 02
        "BA Pluck", # 03
        "BA Soul", # 04
        "BA Stick", # 05
        "BA Low", # 06
        "BA Head", # 07
        "BA Tri", # 08
        "BR Punch", # 09
        "BR TpSf1", # 10
        "BR Movin", # 11
        "BR Ruber", # 12
        "BR CS80", # 13
        "BR Strai", # 14
        "BR Lush", # 15
        "BR TpSf2", # 16
        "CH Quiet", # 17
        "CH Kwire", # 18
        "CH Spirt", # 19
        "CHAnalg", # 20
        "CH VoxPc", # 21
        "DR Tom", # 22
        "Fl Banjo", # 23
        "Fl Koto", # 24
        "Fl Sitr2", # 25
        "Fl Tamba", # 26
        "GT Fingr", # 27
        "GT Amod", # 28
        "GT Strat", # 29
        "GT Pedal", # 30
        "GT Dist2", # 31
        "KY Hrpzi", # 32
        "KY EP 13", # 33
        "KY EP 14", # 34
        "KY EP 15", # 35
        "KY EP 16", # 36
        "KY EP 17", # 37
        "KY EP 18", # 38
        "KY Harm", # 39
        "KY SyClv", # 40
        "ME Bnshe", # 41
        "ME Bubbl", # 42
        "ME Hit", # 43
        "ME Marin", # 44
        "ME Mojo", # 45
        "ME Poot", # 46
        "ME Sweep", # 47
        "ME Tabla", # 48
        "ME Treml", # 49
        "ME Angel", # 50
        "ME Whisl", # 51
        "OR Door0", # 52
        "OR Jazz", # 53
        "OR Pipe", # 54
        "OR Rock", # 55
        "OR Smoth", # 56
        "SC Anti", # 57
        "SC Bell2", # 58
        "SC Bhind", # 59
        "SC Blot", # 60
        "SC Chop", # 61
        "SC Klav", # 62
        "DR Revrs", # 63
    ],
    [ # Internal II
        "SC Hool", # 00
        "SC Hand", # 01
        "SC WooDX", # 02
        "SC Wire", # 03
        "SC Pain", # 04
        "SC Pluck", # 05
        "SC Reflx", # 06
        "SC Sprkl", # 07
        "SC Thumb", # 08
        "SC Uzzy", # 09
        "SC Vxcla", # 10
        "SC Walk", # 11
        "SC Wits", # 12
        "SC Wow", # 13
        "SE Alien", # 14
        "SE Clox", # 15
        "SE Crck", # 16
        "SE Crsh", # 17
        "SE Duel", # 18
        "SE Fear", # 19
        "SE Roll", # 20
        "SE Lava", # 21
        "SE Laze", # 22
        "SE Mono", # 23
        "SE Saw", # 24
        "SE Swmp", # 25
        "SE Vaqum", # 26
        "SE Vektr", # 27
        "SE Zip", # 28
        "SL lck", # 29
        "SL 2VCO1", # 30
        "SL Ash", # 31
        "SL Glnt", # 32
        "SL Oth", # 33
        "SL Sqsaw", # 34
        "SL Ut", # 35
        "SP 1980", # 36
        "SP Decay", # 37
        "SP Ear", # 38
        "SP Glas2", # 39
        "SP It", # 40
        "SP Lash", # 41
        "SP Latt", # 42
        "SP Lonly", # 43
        "SP Lyle", # 44
        "SP Melo", # 45
        "SP Nsty2", # 46
        "SP Oscil", # 47
        "SP Ray", # 48
        "SP SloMo", # 49
        "ST Cello", # 50
        "ST Cntra", # 51
        "ST Chamb", # 52
        "ST Arco2", # 53
        "ST High", # 54
        "ST Anlg2", # 55
        "TP Bell", # 56
        "TP Clock", # 57
        "TP GSvib", # 58
        "TP Tabla", # 59
        "TP Boink", # 60
        "WN Flut1", # 61
        "WN Flut2", # 62
        "DR Voice" # 63
    ]
]

WAVEFORMS = {
    'Preset 1': [
        ('Piano', (
            'Piano', # 1 - Tone Generator A
        )),
        ('Key', (
            'HardEp', # 2 - Tone Generator A
            'HardEpLp', # 3 - Tone Generator A
            'SoftEp', # 4 - Tone Generator A
            'SoftEpLp', # 5 - Tone Generator A
            'SynthEp', # 6 - Tone Generator A
            'SynthEpLp', # 7 - Tone Generator A
            'Clavi 1', # 8 - Tone Generator A
            'Clavi 1Lp', # 9 - Tone Generator A
            'Clavi 2', # 10 - Tone Generator A
            'Clavi 2Lp', # 11 - Tone Generator A
            'Harpsi', # 12 - Tone Generator A
            'HarpsiLp', # 13 - Tone Generator A
            'Acrdion', # 14 - Tone Generator A
            'AcrdionLp', # 15 - Tone Generator A
            'Organ 1', # 16 - Tone Generator A
            'Organ 1Lp', # 17 - Tone Generator A
            'PrcOrg1', # 18 - Tone Generator B
            'PrcOrg1Lp', # 19 - Tone Generator B
            'PrcOrg2', # 20 - Tone Generator A
            'PrcOrg2Lp', # 21 - Tone Generator A
            'RockOrg', # 22 - Tone Generator A
            'Pipe Wv', # 23 - Tone Generator A
            'Pipe WvLp', # 24 - Tone Generator A
        )),
        ('Brass', (
            'Trumpet', # 25 - Tone Generator A
            'TrumpetLp', # 26 - Tone Generator A
            'MuteTp', # 27 - Tone Generator A
            'MuteTpLp', # 28 - Tone Generator A
            'Trombone', # 29 - Tone Generator B
            'TromBneLp', # 30 - Tone Generator B
            'Horn', # 31 - Tone Generator A
            'Tuba', # 32 - Tone Generator A
            'TpEns', # 33 - Tone Generator A
            'TpEnsLp', # 34 - Tone Generator A
            'BrsEns', # 35 - Tone Generator A
            'BrsEnsLp', # 36 - Tone Generator A
        )),
        ('Woodwind', (
            'Baritone', # 37 - Tone Generator A
            'BaritneLp', # 38 - Tone Generator A
            'Tenor', # 39 - Tone Generator A
            'TenorLp', # 40 - Tone Generator A
            'AltoSax', # 41 - Tone Generator A
            'AltoSaxLp', # 42 - Tone Generator A
            'Soprano', # 43 - Tone Generator A
            'SopranoLp', # 44 - Tone Generator A
            'Clarinet', # 45 - Tone Generator A
            'Bassoon', # 46 - Tone Generator A
            'Oboe', # 47 - Tone Generator A
            'EngHorn', # 48 - Tone Generator A
            'Piccolo', # 49 - Tone Generator A
            'Recorder', # 50 - Tone Generator A
            'Flute', # 51 - Tone Generator A
            'Panflute', # 52 - Tone Generator A
            'PnFluteLp', # 53 - Tone Generator A
        )),
        ('String', (
            'Strings1', # 54 - Tone Generator A
            'Strngs1Lp', # 55 - Tone Generator A
            'Strings2', # 56 - Tone Generator A
            'Violin', # 57 - Tone Generator A
            'Viola', # 58 - Tone Generator A
            'Pizz', # 59 - Tone Generator A
        )),
        ('Acoustic Guitar', (
            'GtrSteel', # 60 - Tone Generator A
            'GtrStelLp', # 61 - Tone Generator A
            'GtrNyln', # 62 - Tone Generator A
            'GtrNylnLp', # 63 - Tone Generator A
            '12String', # 64 - Tone Generator A
            '12StrngLp', # 65 - Tone Generator A
        )),
        ('Electric Guitar', (
            'EgSngl1', # 66 - Tone Generator A
            'EgSngl1Lp', # 67 - Tone Generator A
            'EgSngl2', # 68 - Tone Generator B
            'EgSngl2Lp', # 69 - Tone Generator B
            'EgMute1', # 70 - Tone Generator A
            'EgMute2', # 71 - Tone Generator B
            'EgComp', # 72 - Tone Generator A
            'EgCompLp', # 73 - Tone Generator A
            'EgHarm1', # 74 - Tone Generator A
            'EgHarm1Lp', # 75 - Tone Generator A
            'EgHarm2', # 76 - Tone Generator A
            'EgHarm2Lp', # 77 - Tone Generator A
        )),
        ('Bass', (
            'WoodBass', # 78 - Tone Generator A
            'FingBs', # 79 - Tone Generator B
            'FingBsLp', # 80 - Tone Generator B
            'PickBs1', # 81 - Tone Generator B
            'PickBs1Lp', # 82 - Tone Generator B
            'PickBs2', # 83 - Tone Generator B
            'PickBs2Lp', # 84 - Tone Generator B
            'FretLess', # 85 - Tone Generator B
            'FretLs Lp', # 86 - Tone Generator B
            'ThumpBs', # 87 - Tone Generator B
            'ThumpBsLp', # 88 - Tone Generator B
            'SlapBs', # 89 - Tone Generator B
            'SlapBsLp', # 90 - Tone Generator B
        )),
        ('Folk instruments', (
            'Dulcimer', # 91 - Tone Generator A
            'DulcimrD', # 92 - Tone Generator A
            'DlcmSplt', # 93 - Tone Generator A
            'Kalimba', # 94 - Tone Generator A
            'Sitar', # 95 - Tone Generator A
            'Harp', # 96 - Tone Generator A
        )),
        ('Synthesizer', (
            'SynBrs1', # 97 - Tone Generator A
            'SynBrs1Lp', # 98 - Tone Generator A
            'SynBrs2', # 99 - Tone Generator A
            'SynBrs2Lp', # 100 - Tone Generator A
            'SynBrs3', # 101 - Tone Generator A
            'SynBrs3Lp', # 102 - Tone Generator A
            'SynBrs4', # 103 - Tone Generator A
            'SynBrs4Lp', # 104 - Tone Generator A
            'SynBrsWv', # 105 - Tone Generator A
            'SynBs1', # 106 - Tone Generator B
            'SynBs1Lp', # 107 - Tone Generator B
            'SynBs2', # 108 - Tone Generator B
            'SynBs2Lp', # 109 - Tone Generator B
            'SynBs3', # 110 - Tone Generator B
            'SynBs3Lp', # 111 - Tone Generator B
            'SynBs4', # 112 - Tone Generator B
            'SynBs4Lp', # 113 - Tone Generator B
            'SynBs5', # 114 - Tone Generator B
            'SynBs5Lp', # 115 - Tone Generator B
            'SynBs6', # 116 - Tone Generator B
            'SynBs6Lp', # 117 - Tone Generator B
            'SynBs7', # 118 - Tone Generator B
            'SynBs7Lp', # 119 - Tone Generator B
            'SynBs8', # 120 - Tone Generator B
            'SynBs8Lp', # 121 - Tone Generator B
            'SynBs9', # 122 - Tone Generator B
            'SynBs9Lp', # 123 - Tone Generator B
            'SynBs10', # 124 - Tone Generator B
            'SynBs10Lp', # 125 - Tone Generator B
            'Pad 1', # 126 - Tone Generator B
            'Pad 1Lp', # 127 - Tone Generator B
            'Pad 2', # 128 - Tone Generator B
            'Pad 3', # 129 - Tone Generator B
            'Pad 4', # 130 - Tone Generator B
            'Pad 5', # 131 - Tone Generator B
            'SynLead1', # 132 - Tone Generator A
            'SynLead2', # 133 - Tone Generator B
            'SynStWv', # 134 - Tone Generator B
            'DistWv', # 135 - Tone Generator B
            'DistWvLp', # 136 - Tone Generator B
        )),
        ('Choir', (
            'ChoirAa', # 137 - Tone Generator A
            'ChoirAaLp', # 138 - Tone Generator A
            'ChoirOo', # 139 - Tone Generator A
            'ChoirOoLp', # 140 - Tone Generator A
            'Itopia', # 141 - Tone Generator A
        )),
        ('Ideophone', (
            'Glocken', # 142 - Tone Generator A
            'HandBell', # 143 - Tone Generator A
            'HndBellLp', # 144 - Tone Generator A
            'Marimba', # 145 - Tone Generator A
            'SteelDrm', # 146 - Tone Generator A
            'Tubular', # 147 - Tone Generator A
            'TubularLp', # 148 - Tone Generator A
            'Vibes', # 149 - Tone Generator A
            'Xylophon', # 150 - Tone Generator A
        )),
        ('Drum', (
            'BD1', # 151 - Tone Generator B
            'BD2', # 152 - Tone Generator B
            'BD3', # 153 - Tone Generator B
            'BD4', # 154 - Tone Generator B
            'BD5', # 155 - Tone Generator B
            'BD6', # 156 - Tone Generator B
            'BD7', # 157 - Tone Generator B
            'BD8', # 158 - Tone Generator B
            'SD1', # 159 - Tone Generator B
            'SD2', # 160 - Tone Generator B
            'SD3', # 161 - Tone Generator B
            'SD4', # 162 - Tone Generator B
            'SD5', # 163 - Tone Generator B
            'SD6', # 164 - Tone Generator B
            'SD7', # 165 - Tone Generator B
            'SD8', # 166 - Tone Generator B
            'SD9', # 167 - Tone Generator B
            'SD side', # 168 - Tone Generator B
            'Tom1', # 169 - Tone Generator B
            'Tom2', # 170 - Tone Generator B
            'HH Open', # 171 - Tone Generator B
            'HH Pedal', # 172 - Tone Generator B
            'HH light', # 173 - Tone Generator B
            'HH mid', # 174 - Tone Generator B
            'HH heavy', # 175 - Tone Generator B
            'Crash', # 176 - Tone Generator B
            'Ride', # 177 - Tone Generator B
            'RideBell', # 178 - Tone Generator B
            'AnlgTom', # 179 - Tone Generator B
            'HHopAnlg', # 180 - Tone Generator B
            'HHclAnlg', # 181 - Tone Generator B
            'Scratch', # 182 - Tone Generator B
            'RezClick', # 183 - Tone Generator B
            'VcDrmBD', # 184 - Tone Generator B
            'VcDrmSD', # 185 - Tone Generator B
        )),
        ('Percussion', (
            'AgogoHi', # 186 - Tone Generator A
            'Bongo', # 187 - Tone Generator A
            'Cabasa', # 188 - Tone Generator A
            'CongaLo', # 189 - Tone Generator A
            'CongaMt', # 190 - Tone Generator A
            'CongaSlp', # 191 - Tone Generator A
            'AnaConga', # 192 - Tone Generator A
            'Clap', # 193 - Tone Generator A
            'Clave', # 194 - Tone Generator A
            'AnaCwbl', # 195 - Tone Generator A
            'Cowbell', # 196 - Tone Generator A
            'Maracas', # 197 - Tone Generator A
            'Tmbrine', # 198 - Tone Generator A
            'Timpani', # 199 - Tone Generator A
            'TemplBlk', # 200 - Tone Generator A
            'Timbale', # 201 - Tone Generator A
            'Timbale2', # 202 - Tone Generator A
            'Triangle', # 203 - Tone Generator A
            'Whistle', # 204 - Tone Generator B
        )),
        ('Special effect', (
            'SE Bottle', # 205 - Tone Generator B
            'E.P. Np', # 206 - Tone Generator B
            'Bamboo', # 207 - Tone Generator B
            'Temp Ra', # 208 - Tone Generator B
            'Typist', # 209 - Tone Generator B
            'VoiceAtk', # 210 - Tone Generator A
            'ChouCho', # 211 - Tone Generator B
            'Vox Bell', # 212 - Tone Generator B
            'Mellow', # 213 - Tone Generator B
            'Bell Mix', # 214 - Tone Generator B
            'Seq1', # 215 - Tone Generator B
            'Seq2', # 216 - Tone Generator B
            'OrchHit1', # 217 - Tone Generator B
            'OrchHit2', # 218 - Tone Generator B
            'Noise', # 219 - Tone Generator B
        )),
        ('Oscillator', (
            'AnlgSaw1', # 220 - Tone Generator A
            'AnlgSaw2', # 221 - Tone Generator A
            'Pulse 10', # 222 - Tone Generator A
            'Pulse 25', # 223 - Tone Generator A
            'Pulse 50', # 224 - Tone Generator A
            'Digital1', # 225 - Tone Generator A
            'Digital2', # 226 - Tone Generator A
            'Digital3', # 227 - Tone Generator A
            'Digital4', # 228 - Tone Generator A
            'Digital5', # 229 - Tone Generator A
            'Digital6', # 230 - Tone Generator A
            'Digital7', # 231 - Tone Generator A
            'Digital8', # 232 - Tone Generator A
            'Digital9', # 233 - Tone Generator A
            'Digitl10', # 234 - Tone Generator A
            'Digitl11', # 235 - Tone Generator A
            'Digitl12', # 236 - Tone Generator A
            'DigiVox1', # 237 - Tone Generator B
            'DigiVox2', # 238 - Tone Generator B
            'DigiVox3', # 239 - Tone Generator B
            'DigiVox4', # 240 - Tone Generator B
            'DigiVox5', # 241 - Tone Generator B
            'DigiWild', # 242 - Tone Generator B
            'Tri', # 243 - Tone Generator B
            'Sin', # 244 - Tone Generator B
        ))
    ],
    'Preset 2': [
        ('Piano', (
            'Piano2', # 1 - Tone Generator B
        )),
        ('Key', (
            'SynClavi', # 2 - Tone Generator B
        )),
        ('Brass', (
            'Trumpet2', # 3 - Tone Generator B
            'TrmPet2LP', # 4 - Tone Generator B
        )),
        ('Woodwind', (
            'Flute2', # 5 - Tone Generator B
        )),
        ('String', (
            'Chamber', # 6 - Tone Generator B
            'Cello', # 7 - Tone Generator B
            'CelloLp', # 8 - Tone Generator B
            'CntraBs', # 9 - Tone Generator B
            'CntraBsLp', # 10 - Tone Generator B
        )),
        ('Acoustic Guitar', (
            'GtrFngr', # 11 - Tone Generator B
            'GtrFngrLp', # 12 - Tone Generator B
        )),
        ('Electric Guitar', (
            'EgHumBk', # 13 - Tone Generator B
            'EgHumBkLp', # 14 - Tone Generator B
        )),
        ('Ideophone', (
            'Celesta', # 15 - Tone Generator B
        )),
        ('Drum', (
            'Drum BD9', # 16 - Tone Generator B
            'Brush', # 17 - Tone Generator B
            'SD10', # 18 - Tone Generator B
            'Tom3', # 19 - Tone Generator B
            'Tom4', # 20 - Tone Generator B
            'Tom5', # 21 - Tone Generator B
            'VcDrmHHc', # 22 - Tone Generator B
            'VcDrmHHo', # 23 - Tone Generator B
            'Chaina', # 24 - Tone Generator B
        )),
        ('Percussion', (
            'Perc. Guiro', # 25 - Tone Generator B
            'Guiro2', # 26 - Tone Generator B
            'Tabla', # 27 - Tone Generator B
            'Tabla2', # 28 - Tone Generator B
            'Cuica H', # 29 - Tone Generator B
            'Cuica L', # 30 - Tone Generator B
            'VibraSlp', # 31 - Tone Generator B
        )),
        ('Special effects', (
            'OrchHit3', # 32 - Tone Generator B
            'BellRing', # 33 - Tone Generator B
            'Seq3', # 34 - Tone Generator B
        )),
        ('Oscillator', (
            'LongSaw', # 35 - Tone Generator B
            'SawSqu', # 36 - Tone Generator B
            'SquSaw', # 37 - Tone Generator B
            'BellWv', # 38 - Tone Generator B
            'BellWv2', # 39 - Tone Generator B
            'EpWv1', # 40 - Tone Generator B
            'EpWv2', # 41 - Tone Generator B
            'EpWv3', # 42 - Tone Generator B
            'EpWv4', # 43 - Tone Generator B
            'EpWv5', # 44 - Tone Generator B
            'EpWv6', # 45 - Tone Generator B
            'VoxG2Wv', # 46 - Tone Generator B
            'VoxE3Wv', # 47 - Tone Generator B
            'OrgWv1', # 48 - Tone Generator B
            'OrgWv2', # 49 - Tone Generator B
            'OrgWv3', # 50 - Tone Generator B
        ))
    ],
    'Card': [],
    'Internal': []
}

WAVEFORM_NAMES = [list(chain(*(x[1] for x in WAVEFORMS[bank])))
    for bank in (x[1] for x in WAVEFORM_BANKS)]
del chain, bank

CS_PARAMETERS = [
    "No_Assign",
    "CT_MW_Pmod",
    "CT_MW_Amod",
    "CT_MW_Fmod",
    "CT_MW_Coff",
    "CT_MW_EGBs",
    "CT_FC_Pmod",
    "CT_FC_Amod",
    "CT_FC_Fmod",
    "CT_FC_Coff",
    "CT_FC_EGBs",
    "CT_AT_Pmod",
    "CT_AT_Amod",
    "CT_AT_Fmod",
    "CT_AT_Coff",
    "CT_AT_EGBs",
    "CT_AT_PtBs",
    "CT_PBRange",
    "CT_VLLoLim",
    "TotalLevel",
    "EF_SendLvl",
    "OS_FrqFine",
    "OS_Random",
    "PEG_Rate1",
    "PEG_Rate2",
    "PEG_Rate3",
    "PEG_RlsRt",
    "PEG_Level0",
    "PEG_Level1",
    "PEG_Level2",
    "PEG_Level3",
    "PEG_RlsLvl",
    "PEG_Range",
    "PEG_LvlVel",
    "PEG_RtVel",
    "LFO_Speed",
    "LFO_Delay",
    "LFO_Pmod",
    "LFO_Amod",
    "LFO_Fmod",
    "LFO_Wave",
    "LFO_Phase",
    "LFO_SpdVel",
    "LFO_SpdRnd",
    "AEG_Rate1",
    "AEG_Rate2",
    "AEG_Rate3",
    "AEG_Rate4",
    "AEG_RlsRt",
    "AEG_Level2",
    "AEG_Level3",
    "AEG_LvlVel",
    "AEG_RtVel",
    "FLT_Reso",
    "FLT_CofVel",
    "FLT_ARVel",
    "FLT_Band",
    "FLT_CofFrq",
    "FLT_Rate1",
    "FLT_Rate2",
    "FLT_Rate3",
    "FLT_Rate4",
    "FLT_RlsRt1",
    "FLT_RlsRt2",
    "FLT_Level0",
    "FLT_Level1",
    "FLT_Level2",
    "FLT_Level3",
    "FLT_Level4",
    "FLT_RlsLv1",
    "FLT_RlsLv2",
    "OS_NoteSft",
    "FLT_BPLvl1",
    "FLT_BPLvl2",
    "FLT_BPLvl3",
    "FLT_BPLvl4"
]
