"""Enums for the Maschine MK3 FL Studio MIDI script"""

from enum import Enum

from colors import *


__all__ = [
    "PluginColors",
    "ChannelColors",
    "PadMode",
    "FourDEncoderMode",
    "TouchStripMode",
]


# -------- Plugin and channel colors for OMNI/PAD modes, feel free to change these with any others from the list --------
class PluginColors(Enum):
    """Plugin Colors"""

    DEFAULT = Green1
    HIGHLIGHTED = Green3


class ChannelColors(Enum):
    """Channel Colors"""

    DEFAULT = White1
    HIGHLIGHTED = White3


# ------------------------------------------------------------------------------------------------------------------------


class PadMode(Enum):
    """Pad Modes"""

    OMNI = 0
    KEYBOARD = 1
    CHORDS = 2
    STEP = 3


class FourDEncoderMode(Enum):
    """4D Encoder Modes"""

    JOG = 0
    VOLUME = 1
    SWING = 2
    TEMPO = 3


class TouchStripMode(Enum):
    """Touch Strip Modes"""

    DISABLED = 0
    PITCH = 1
    MOD = 2
    PERFORM = 3
    NOTES = 4
