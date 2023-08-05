# -*- coding: UTF-8 -*-
"""\
Korg Wavestation Sysex handling library
=======================================

This package provides an API to handle MIDI system exclusive data for the
Korg Wavestation line of synthesizers.

Currently it can read performance, patch and wavesequence data and provides
methods to query basic information from these objects.

This software is still in alpha stage, so much intended functionality is still
missing. For the moment, the most useful part is an included script to list
performances, patches and wave sequences in Wavestation sysex dump files.

"""

version = "0.1a"
description = __doc__.splitlines()[0]
long_description = __doc__
author = "Christopher Arndt"
email = "chris@chrisarndt.de"
url = "http://chrisarndt.de/projects/korgwslib"
download_url = url + "/download/"
copyright = "Copyright 2010 Christopher Arndt"
license = "MIT"
