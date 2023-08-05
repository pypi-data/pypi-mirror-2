"Misc utility functions for the korgws package."""

# korgws/util.py

__all__ = [
    'NullHandler',
    'check_checksum',
    'decode_name',
    'is_ws_sysex',
    'nibbles2bytes'
]

import logging

from korgws.constants import *


class NullHandler(logging.Handler):
    def emit(self, record):
        pass

def get_logger(name='korgws'):
    log = logging.getLogger(name)
    log.addHandler(NullHandler())
    return log

def is_ws_sysex(data):
    return (data[:2] == SOX + KORG_ID and 
        ord(data[2]) >> 4 == FORMAT_ID and
        data[3] == WS_ID)

def nibbles2bytes(data):
    assert not len(data) % 2
    bytes = []
    for i in xrange(0, len(data), 2):
        bytes.append(((ord(data[i+1]) & 0xF) << 4) | (ord(data[i]) & 0xF))
    return ''.join(chr(c) for c in bytes)

def decode_name(name):
    name = name.replace('\x00', ' ').replace('\x7F', ' ').rstrip()
    return name.decode('latin1', 'replace')

def check_checksum(data, checksum):
    return checksum == sum(ord(i) for i in data) % 128
    