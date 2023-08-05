#!/usr/bin/env python
"""List names of performances, patches and wave sequences contained in a Korg Wavestation (EX,A/D,SR) sysex dump.
"""

from korgws.scripts.listbanks import main

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv[1:]))
