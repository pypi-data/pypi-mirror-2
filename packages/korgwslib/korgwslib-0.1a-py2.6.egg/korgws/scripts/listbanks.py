#!/usr/bin/env python
"""List names of performances, patches and wave sequences contained in a Korg Wavestation (EX,A/D,SR) sysex dump.
"""

__author__ = 'Christopher Arndt'
__version__ = '0.1b'
__revision__ = '$Rev:$'
__copyright__ = 'MIT license'
__usage__ = 'Usage: wssyxlist [OPTIONS] SYSEX-FILE...'

import logging
import sys

from glob import glob
from operator import attrgetter
from optparse import OptionParser

from korgws.constants import *
from korgws.handlers import *
from korgws.util import get_logger

log = get_logger()

def print_bank(bank):
    caption = "Performances %s" % bank.name
    print caption
    print "-" * len(caption)
    print
    for i, wsobj in enumerate(bank.performances):
        print "%02i: %s" % (i, wsobj.name)
    print

    caption = "Patches %s" % bank.name
    print caption
    print "-" * len(caption)
    print
    for i, wsobj in enumerate(bank.patches):
        print "%02i: %s" % (i, wsobj.name)
    print

    caption = "Wave Sequences %s" % bank.name
    print caption
    print "-" * len(caption)
    print
    for i, wsobj in enumerate(bank.wave_seqs):
        print "%02i: %s" % (i, wsobj.name)
    print


def main(args):
    parser = OptionParser(usage=__usage__, version=__version__)
    parser.add_option('-v', '--verbose', action="store_true",
        dest='verbose', help='Output debugging information to stderr')
    parser.add_option('-g', '--filename-globs', action="store_true",
        dest='globs', help='Interpret filenames as shell wildcards')
    options, args = parser.parse_args(args=args)

    if not args:
        parser.print_help()
        return 2

    if options.verbose:
        h = logging.StreamHandler(sys.stderr)
        f = logging.Formatter('%(message)s')
        h.setFormatter(f)
        log.addHandler(h)
        log.setLevel(logging.DEBUG)

    if options.globs:
        for fn in args[:]:
            args.remove(fn)
            args.extend(glob(fn))

    for syxfn in sorted(args):
        print "File: %s" % syxfn
        print '=' * (len(syxfn) + 6)
        print
        syxfo = open(syxfn, 'rb')
        banks = parse_sysex_data(syxfo.read())
        syxfo.close()
        for bank in sorted(banks.values(), key=attrgetter('name')):
            print_bank(bank)
        print

    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
