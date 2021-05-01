import numpy as np
DETECTOR_MASKS = {
    0: 0x00000001,
    1: 0x00000002,
    2: 0x00000004,
    3: 0x00000008,
    4: 0x00000010,
    5: 0x00000020,
    6: 0x00000040,
    7: 0x00000080,
    8: 0x00000100,
    9: 0x00000200,
    10: 0x00000400,
    11: 0x00000800,
    12: 0x00001000,
    13: 0x00002000,
    14: 0x00004000,
    15: 0x00008000,
    16: 0x00010000,
    17: 0x00020000,
    18: 0x00040000,
    19: 0x00080000,
    20: 0x00100000,
    21: 0x00200000,
    22: 0x00400000,
    23: 0x00800000,
    24: 0x01000000,
    25: 0x02000000,
    26: 0x04000000,
    27: 0x08000000,
    28: 0x10000000,
    29: 0x20000000,
    30: 0x40000000,
    31: 0x80000000
}

QUARTER_DETECTORS = {
    0: np.array([1, 2, 5, 6, 7, 11, 12, 13])-1,
    1: np.array([3, 4, 8, 9, 10, 14, 15, 16]) - 1,
    2: np.array([20, 21, 22, 26, 27, 28, 31, 32]) - 1,
    3: np.array([17, 18, 19, 23, 24, 25, 29, 30]) - 1
}
PIXEL_IDS = {
    0: 0x001,
    1: 0x002,
    2: 0x004,
    3: 0x008,
    4: 0x010,
    5: 0x020,
    6: 0x040,
    7: 0x080,
    8: 0x100,
    9: 0x200,
    10: 0x400,
    11: 0x800
}

ASIC_MASKS = {
    2: 0x00000004,
    4: 0x00000010,
    6: 0x00000040,
    7: 0x00000080,
    9: 0x00000200,
    10: 0x00000400,
    12: 0x00001000,
    13: 0x00002000,
    14: 0x00004000,
    16: 0x00010000,
    17: 0x00020000,
    19: 0x00080000,
    20: 0x00100000,
    22: 0x00400000,
    23: 0x00800000,
    24: 0x01000000,
    25: 0x02000000,
    27: 0x08000000,
    28: 0x10000000,
    31: 0x80000000,
    26: 0x04000000,
    15: 0x00008000,
    8: 0x00000100,
    1: 0x00000002,
    29: 0x20000000,
    18: 0x00040000,
    5: 0x00000020,
    0: 0x00000001,
    30: 0x40000000,
    21: 0x00200000,
    11: 0x00000800,
    3: 0x00000008
}

PIXEL_MASK = [
     0x04000000,
     0x00008000,
     0x00000100,
     0x00000002,
     0x20000000,
     0x00040000,
     0x00000020,
     0x00000001,
     0x40000000,
     0x00200000,
     0x00000800,
     0x00000008
]

SMALL_PIXEL_MASK_HEX=hex(sum(PIXEL_MASK[8:12]))
BIG_PIXEL_MASK_HEX=hex(sum(PIXEL_MASK[0:8]))
ALL_PIXEL_MASK=hex(sum(PIXEL_MASK))

def get_group_mask(group_id):
    detectors=QUARTER_DETECTORS[group_id]
    mask=0
    for detector in detectors:
        mask|=DETECTOR_MASKS[detector]
    return hex(mask)

def syslog(text):
    print('syslog "{}"'.format(text))
def send_tc(text):
    print('tcsend {} checks {{SPTV DPTV CEV}} ack {{ACCEPT COMPLETE}}'.format(text))

def wait(n):
    print('waittime +{}'.format(n))
def comment(text):
    print('#{}'.format(text))
def info(text):
    print('#{}'.format(text))
