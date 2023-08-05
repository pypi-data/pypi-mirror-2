#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Setup file for the sy85 package."""

import sys

scripts = ["scripts/genlistings", "scripts/sy85sxtool", "scripts/sy85info"]

if sys.platform.startswith('win'):
    from distutils.core import setup
    import py2exe
    platform_opts = dict(
        options = {'py2exe': {'bundle_files': 1}},
        console = scripts,
        zipfile = None)
else:
    from setuptools import setup
    platform_opts = dict(scripts=scripts)

setup(name = 'sy85tools',
    version = '0.2.1a',
    description = 'Collection of tools to handle MIDI sysex and other files '
        'for the Yamaha SY85',
    keywords = 'midi, sysex',
    author = 'Christopher Arndt',
    author_email = 'chris@chrisarndt.de',
    url = 'http://chrisarndt.de/projects/sy85tools/',
    download_url = 'http://chrisarndt.de/projects/sy85tools/download/',
    license = "MIT license",
    long_description = """\
A Python package and some command line tools to deal with MIDI sysex dumps and
disk files produced and read by the classic Yamaha SY85 synthesizers.
""",
    platforms = "POSIX, Windows, MacOS X",
    classifiers = [
      'Development Status :: 3 - Alpha',
      'Environment :: Console',
      'Intended Audience :: Developers',
      'Intended Audience :: Other Audience',
      'License :: OSI Approved :: MIT License',
      'Operating System :: Microsoft :: Windows',
      'Operating System :: POSIX',
      'Operating System :: MacOS :: MacOS X',
      'Programming Language :: Python',
      'Topic :: Multimedia :: Sound/Audio :: Conversion',
      'Topic :: Multimedia :: Sound/Audio :: MIDI',
      'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    packages = ['sy85', 'sy85.converters', 'sy85.data', 'sy85.scripts'],
    zip_safe = True,
    **platform_opts
)
