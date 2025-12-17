"""Enums for the Maschine MK3 FL Studio MIDI script"""

from enum import IntEnum

__all__ = [
    "ControllerColor",
    "PluginColor",
    "ChannelColor",
    "PadMode",
    "FourDEncoderMode",
    "TouchStripMode",
    "PadGroup",
]


class ControllerColor(IntEnum):
    """Maschine MK3 LED Colors"""

    BLACK_0 = 0
    BLACK_1 = 1
    BLACK_2 = 2
    BLACK_3 = 3
    RED_0 = 4
    RED_1 = 5
    RED_2 = 6
    RED_3 = 7
    ORANGE_0 = 8
    ORANGE_1 = 9
    ORANGE_2 = 10
    ORANGE_3 = 11
    LIGHT_ORANGE_0 = 12
    LIGHT_ORANGE_1 = 13
    LIGHT_ORANGE_2 = 14
    LIGHT_ORANGE_3 = 15
    WARM_YELLOW_0 = 16
    WARM_YELLOW_1 = 17
    WARM_YELLOW_2 = 18
    WARM_YELLOW_3 = 19
    YELLOW_0 = 20
    YELLOW_1 = 21
    YELLOW_2 = 22
    YELLOW_3 = 23
    LIME_0 = 24
    LIME_1 = 25
    LIME_2 = 26
    LIME_3 = 27
    GREEN_0 = 28
    GREEN_1 = 29
    GREEN_2 = 30
    GREEN_3 = 31
    MINT_0 = 32
    MINT_1 = 33
    MINT_2 = 34
    MINT_3 = 35
    CYAN_0 = 36
    CYAN_1 = 37
    CYAN_2 = 38
    CYAN_3 = 39
    TURQUOISE_0 = 40
    TURQUOISE_1 = 41
    TURQUOISE_2 = 42
    TURQUOISE_3 = 43
    BLUE_0 = 44
    BLUE_1 = 45
    BLUE_2 = 46
    BLUE_3 = 47
    PLUM_0 = 48
    PLUM_1 = 49
    PLUM_2 = 50
    PLUM_3 = 51
    VIOLET_0 = 52
    VIOLET_1 = 53
    VIOLET_2 = 54
    VIOLET_3 = 55
    PURPLE_0 = 56
    PURPLE_1 = 57
    PURPLE_2 = 58
    PURPLE_3 = 59
    MAGENTA_0 = 60
    MAGENTA_1 = 61
    MAGENTA_2 = 62
    MAGENTA_3 = 63
    FUCHSIA_0 = 64
    FUCHSIA_1 = 65
    FUCHSIA_2 = 66
    FUCHSIA_3 = 67
    WHITE_0 = 68
    WHITE_1 = 69
    WHITE_2 = 70
    WHITE_3 = 71


# -------- Plugin and channel colors for OMNI/PAD modes, feel free to change these with any others from the list --------
class PluginColor(IntEnum):
    """Plugin Colors"""

    DEFAULT = ControllerColor.ORANGE_1
    HIGHLIGHTED = ControllerColor.ORANGE_3


class ChannelColor(IntEnum):
    """Channel Colors"""

    DEFAULT = ControllerColor.WHITE_1
    HIGHLIGHTED = ControllerColor.WHITE_3


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


class PadGroup(IntEnum):
    """Pad Groups"""

    A = 100
    B = 101
    C = 102
    D = 103
    E = 104
    F = 105
    G = 106
    H = 107
