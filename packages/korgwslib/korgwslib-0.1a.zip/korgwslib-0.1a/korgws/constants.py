"""Constants for the korgws package."""

# korgws/contants.py

SOX = '\xF0'
EOX = '\xF7'
KORG_ID = '\x42'
WS_ID = '\x28'
FORMAT_ID = 3


BANK_NAMES = [
    'RAM1',
    'RAM2',
    'ROM1',
    'CARD',
    'RAM3'
]

MSG_TYPES = {
    # parameters and object data dumps
    0x41: "Parameter Change Message",
    0x42: "Parameter Change Message Expanded",
    0x40: "Single Patch Dump",
    0x49: "Single Performance Dump",
    0x4C: "All Patch Dump",         # within bank
    0x4D: "All Performance Dump",   # within bank
    0x50: "All Data Dump",          # system, patch, performance, wave sequence
    0x51: "System Setup Dump",
    0x54: "All Wave Sequence Dump", # within bank
    0x5A: "Micro Tune Scales Dump",
    0x5C: "System Setup Dump Expanded",
    0x55: "Multi Mode Setup Dump",
    0x5D: "Performance Map Dump ",
    0x5E: "Multi Mode Setup Dump Expanded",
    0x5F: "Performance Map Dump Expanded",
    # commands and responses
    0x23: "Data Load Completed",
    0x24: "Data Load Error",
    0x11: "Patch Write Command",
    0x1A: "Performance Write Command",
    0x21: "Write Complete Message",
    0x22: "Write Error Message",
    0x5B: "Multi Mode Setup Select",
    # dump requests
    0x06: "Multi Mode Setup Dump Request",
    0x07: "Performance Map Dump Request",
    0x08: "Micro Tune Scales Dump Request",
    0x0C: "Wave Sequence Data Dump Request",
    0x0E: "System Setup Dump Request",
    0x0F: "All Data Dump Request",
    0x10: "Single Patch Dump Request",
    0x19: "Single Performance Dump Request",
    0x1C: "All Patch Dump Request",
    0x1D: "All Performance Dump Request",
}

LEN_PATCH_BANK = 35
LEN_PERF_BANK = 50
LEN_WAVESEQ_BANK = 32
LEN_WAVESTEP_LIST = 501

SIZE_PERF_DATA = 181
SIZE_PERF_NAME = 16
SIZE_PATCH_DATA = 426
SIZE_PATCH_NAME = 16
SIZE_WAVESEQ_DATA = 16
SIZE_WAVESTEP = 16
SIZE_WAVESEQ_NAME = 8

SIZE_ALL_PERF_DATA = SIZE_PERF_DATA * LEN_PERF_BANK
SIZE_ALL_PATCH_DATA = SIZE_PATCH_DATA * LEN_PATCH_BANK
SIZE_ALL_WAVESEQS = SIZE_WAVESEQ_DATA * LEN_WAVESEQ_BANK
SIZE_ALL_WAVESTEPS = SIZE_WAVESTEP * LEN_WAVESTEP_LIST
SIZE_ALL_WAVESEQ_NAMES = SIZE_WAVESEQ_NAME * LEN_WAVESEQ_BANK
SIZE_ALL_WAVESEQ_DATA = (SIZE_ALL_WAVESEQS + SIZE_ALL_WAVESTEPS +
    SIZE_ALL_WAVESEQ_NAMES)
