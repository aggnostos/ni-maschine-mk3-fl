from enum import IntEnum

__all__ = ["Pad"]


class Pad(IntEnum):
    """Maschine MK3 Pad Buttons Enum"""

    UNDO = 0
    REDO = 1
    QUANTIZE = 4
    QUANTIZE_HALF = 5
    SEMI_DOWN = 12
    SEMI_UP = 13
    OCTAVE_DOWN = 14
    OCTAVE_UP = 15
