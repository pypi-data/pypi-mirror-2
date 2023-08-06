# Time-stamp: <2011-03-01 18:21:42 Jake Biesinger>

AREM_VERSION = "AREM 1.0.1"
MAX_PAIRNUM = 1000
MAX_LAMBDA  = 100000
FESTEP      = 20

from array import array

if array('h',[1]).itemsize == 2:
    BYTE2 = 'h'
else:
    raise Exception("BYTE2 type cannot be determined!")

if array('H',[1]).itemsize == 2:
    UBYTE2 = 'H'
else:
    raise Exception("UBYTE2 (unsigned short) type cannot be determined!")

if array('i',[1]).itemsize == 4:
    BYTE4 = 'i'
elif array('l',[1]).itemsize == 4:
    BYTE4 = 'l'
else:
    raise Exception("BYTE4 type cannot be determined!")

if array('f',[1]).itemsize == 4:
    FBYTE4 = 'f'
elif array('d',[1]).itemsize == 4:
    FBYTE4 = 'd'
else:
    raise Exception("FBYTE4 type cannot be determined!")

def breakpoint():
    """Drop-in debugger, preferring ipython pdb.
    """
    try:
        import ipdb as pdb
    except ImportError:
        import pdb
    pdb.set_trace()
