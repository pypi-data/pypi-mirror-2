"""Handler functions for Korg Wavestation sysex messages."""

# korgws/handlers.py

__all__ = [
    'parse_all_patch_dump',
    'parse_all_perf_dump',
    'parse_sysex_data',
    'parse_wvseq_dump',
]

import logging

from korgws.api import *
from korgws.constants import *
from korgws.util import (check_checksum, decode_name, get_logger,
    is_ws_sysex, nibbles2bytes)

log = logging.getLogger(__name__)

def _parse_all_patch_data(data):
    patches = []
    for idx in xrange(0, len(data), SIZE_PATCH_DATA):
        patches.append(WSPatch(data=data[idx:idx + SIZE_PATCH_DATA]))
    return patches

def _parse_all_perf_data(data):
    perfs = []
    for idx in xrange(0, len(data), SIZE_PERF_DATA):
        perfs.append(WSPerformance(data=data[idx:idx + SIZE_PERF_DATA]))
    return perfs

def _parse_wvseq_data(data):
    wvseqdata = []
    wvsteps = []
    wvseqs = []
    for idx in xrange(0, SIZE_ALL_WAVESEQS, SIZE_WAVESEQ_DATA):
        wvseqdata.append(data[idx:idx + SIZE_WAVESEQ_DATA])
    offset = SIZE_ALL_WAVESEQS
    for idx in xrange(0, SIZE_ALL_WAVESEQS, SIZE_WAVESEQ_DATA):
        start = offset + idx * SIZE_WAVESTEP
        wvsteps.append(WSWaveStep(data=data[start:start + SIZE_WAVESTEP]))
    offset = SIZE_ALL_WAVESEQS + SIZE_ALL_WAVESTEPS
    for idx in xrange(LEN_WAVESEQ_BANK):
        start = offset + idx * SIZE_WAVESEQ_NAME
        name = data[start:start + SIZE_WAVESEQ_NAME]
        wvseqs.append(WSWaveSeq(data=name+wvseqdata[idx]))

    return wvseqs, wvsteps

def parse_all_perf_dump(data, banks):
    checksum = ord(data[-1])
    if not check_checksum(data[6:-1], banks):
        log.warning("Invalid checksum %i!", checksum)
    bankname = BANK_NAMES[ord(data[5])]
    bank = banks.setdefault(bankname, WSBank(bankname))
    bank.performances = _parse_all_perf_data(nibbles2bytes(data[6:-1]))

def parse_all_patch_dump(data, banks):
    checksum = ord(data[-1])
    if not check_checksum(data[6:-1], checksum):
        log.warning("Invalid checksum %i!", checksum)
    bankname = BANK_NAMES[ord(data[5])]
    bank = banks.setdefault(bankname, WSBank(bankname))
    bank.patches = _parse_all_patch_data(nibbles2bytes(data[6:-1]))

def parse_wvseq_dump(data, banks):
    checksum = ord(data[-1])
    if not check_checksum(data[6:-1], checksum):
        log.warning("Invalid checksum %i!", checksum)
    bankname = BANK_NAMES[ord(data[5])]
    wvseqs, wvsteps = _parse_wvseq_data(nibbles2bytes(data[6:-1]))
    bank = banks.setdefault(bankname, WSBank(bankname))
    bank.wave_seqs = wvseqs
    bank.wave_steps = wvsteps

def parse_all_data_dump(data, banks):
    """Parse All Data structure and save data objects into bank dict.

    typedef struct
    {
        system			system_all;
        multiset_block	multiset_all;
        mtune_block		mtune_all;
        perfmap_block	perfmap_all;
        performance		perf_ram1[50];
        performance		perf_ram2[50];
        patch			patch_ram1[35];
        patch			patch_ram2[35];
        ws_block		ws_ram1;
        ws_block		ws_ram2;
    } all_data;

    """
    checksum = ord(data[-1])
    if not check_checksum(data[6:-1], checksum):
        log.warning("Invalid checksum %i!", checksum)
    ram1 = WSBank('RAM1')
    ram2 = WSBank('RAM2')
    data = nibbles2bytes(data[5:-1])
    idx = 1813

    ram1.performances = _parse_all_perf_data(data[idx:idx+SIZE_ALL_PERF_DATA])
    idx += SIZE_ALL_PERF_DATA
    ram2.performances = _parse_all_perf_data(data[idx:idx+SIZE_ALL_PERF_DATA])
    idx += SIZE_ALL_PERF_DATA
    
    ram1.patches = _parse_all_patch_data(data[idx:idx+SIZE_ALL_PATCH_DATA])
    idx += SIZE_ALL_PATCH_DATA
    ram2.patches = _parse_all_patch_data(data[idx:idx+SIZE_ALL_PATCH_DATA])
    idx += SIZE_ALL_PATCH_DATA
    
    wvseqs, wvsteps = _parse_wvseq_data(data[idx:idx+SIZE_ALL_WAVESEQ_DATA])
    ram1.wave_seqs = wvseqs
    ram1.wave_steps = wvsteps
    idx += SIZE_ALL_WAVESEQ_DATA
    wvseqs, wvsteps = _parse_wvseq_data(data[idx:idx+SIZE_ALL_WAVESEQ_DATA])
    ram2.wave_seqs = wvseqs
    ram2.wave_steps = wvsteps

    banks[ram1.name] = ram1
    banks[ram2.name] = ram2

def parse_sysex_data(data):
    banks =  {}

    handlers = {
        0x4C: parse_all_patch_dump,
        0x4D: parse_all_perf_dump,
        0x50: parse_all_data_dump,
        0x54: parse_wvseq_dump,
    }

    messages = data.split(EOX)[:-1]
    for i, msg in enumerate(messages):
        if len(msg) >= 8 and is_ws_sysex(msg):
            channel = ord(msg[2]) & 0xF
            msgcode = ord(msg[4])
            try:
                msgtype = MSG_TYPES[msgcode]
            except KeyError:
                log.warning("Message type (%x) not supported." % msgcode)
                continue
            try:
                handler = handlers[msgcode]
                if not callable(handler):
                    raise ValueError("Invalid handler: %r", handler)
            except (KeyError, TypeError, ValueError):
                log.info("Ignoring '%s' message." % msgtype)
            else:
                log.info("Message %02i: channel: %i, type: %s (%i bytes)",
                    i, channel, msgtype, len(msg) + 1)
                handler(msg, banks)
        else:
            log.warning("No Korg Wavestation sysex header found. "
                "Skipping message.")

    return banks