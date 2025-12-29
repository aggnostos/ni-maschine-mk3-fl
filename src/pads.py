from enum import IntEnum, IntFlag

from enums import ControllerColor

__all__ = ["PadAction", "PadMode", "PadModeColor"]


class PadAction(IntEnum):
    """Maschine MK3 Pad Buttons Enum"""

    UNDO = 0
    REDO = 1
    QUANTIZE = 4
    QUANTIZE_HALF = 5
    SEMI_DOWN = 12
    SEMI_UP = 13
    OCTAVE_DOWN = 14
    OCTAVE_UP = 15


class PadMode(IntFlag):
    """Pad Modes (bitwise flags)"""

    PAD = 0x1
    OMNI = 0x2
    KEYBOARD = 0x4
    CHORDS = 0x8
    STEP = 0x10
    SOLO = 0x20
    MUTE = 0x40


class PadModeColor(IntEnum):
    """Pad Mode Colors (any ControllerColor value with _2 suffix)"""

    PAD = ControllerColor.ORANGE_2
    OMNI = ControllerColor.LIGHT_ORANGE_2
    KEYBOARD = ControllerColor.BLUE_2
    CHORDS = ControllerColor.PLUM_2
    STEP = ControllerColor.PURPLE_2
    SOLO = ControllerColor.LIME_2
    MUTE = ControllerColor.MINT_2
