"""Enums for the Maschine MK3 FL Studio MIDI script"""

from enum import Enum, IntEnum

from colors import *


__all__ = [
    "PluginColors",
    "ChannelColors",
    "PadMode",
    "FourDEncoderMode",
    "TouchStripMode",
    "Group",
]


# -------- Plugin and channel colors for OMNI/PAD modes, feel free to change these with any others from the list --------
class PluginColors(Enum):
    """Plugin Colors"""

    DEFAULT = Orange1
    HIGHLIGHTED = Orange3


class ChannelColors(Enum):
    """Channel Colors"""

    DEFAULT = White1
    HIGHLIGHTED = White3


# ------------------------------------------------------------------------------------------------------------------------


class PadMode(IntEnum):
    """Pad Modes"""

    OMNI = 0
    KEYBOARD = 1
    CHORDS = 2
    STEP = 3


class FourDEncoderMode(IntEnum):
    """4D Encoder Modes"""

    JOG = 0
    VOLUME = 1
    SWING = 2
    TEMPO = 3


class TouchStripMode(IntEnum):
    """Touch Strip Modes"""

    DISABLED = 0
    PITCH = 1
    MOD = 2
    PERFORM = 3
    NOTES = 4


class Group(IntEnum):
    """Pad Groups"""

    A = 100
    B = 101
    C = 102
    D = 103
    E = 104
    F = 105
    G = 106
    H = 107
