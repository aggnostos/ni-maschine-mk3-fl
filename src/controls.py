"""Maschine MK3 Control Change (CC) Numbers"""

from enum import IntEnum


__all__ = ["CC"]


class CC(IntEnum):
    """Maschine MK3 Control Change (CC) Numbers Enum"""

    # -------- CONTROL BUTTONS SECTION -------- #
    CHANNEL = 34
    PLUGIN = 35
    ARRANGER = 36
    MIXER = 37
    BROWSER = 38
    FILE_SAVE = 40
    SETTINGS = 41

    # -------- EDIT (ENCODER) SECTION -------- #
    ENCODER_PUSH = 7
    ENCODER_TURN = 8
    ENCODER_UP = 30
    ENCODER_RIGHT = 31
    ENCODER_DOWN = 32
    ENCODER_LEFT = 33

    ENCODER_VOLUME = 44
    ENCODER_SWING = 45
    ENCODER_TEMPO = 47

    # -------- TOUCH STRIP SECTION -------- #
    TOUCH_STRIP = 1

    TOUCH_STRIP_PITCH = 49
    TOUCH_STRIP_MOD = 50
    TOUCH_STRIP_PERFORM = 51
    TOUCH_STRIP_NOTES = 52

    # -------- GROUP SECTION -------- #
    GROUP_A = 100
    GROUP_B = 101
    GROUP_C = 102
    GROUP_D = 103
    GROUP_E = 104
    GROUP_F = 105
    GROUP_G = 106
    GROUP_H = 107

    # -------- TRANSPORT SECTION -------- #
    RESTART = 53
    ERASE = 54
    TAP = 55
    PLAY = 57
    GRID = 56
    REC = 58
    STOP = 59

    # -------- PAD SECTION -------- #
    FIXED_VEL = 81

    # PAD MODES
    PAD_MODE = 80
    KEYBOARD_MODE = 82
    CHORDS_MODE = 84
    STEP_MODE = 83

    PATTERN = 86
    SOLO = 91
    MUTE = 92

    # ---- KNOB PAGE SECTION ---- #
    # BUTTONS
    PRESET_NEXT = 22
    PRESET_PREV = 23
    OCTAVE_DOWN = 26
    OCTAVE_UP = 27
    SEMI_DOWN = 28
    SEMI_UP = 29

    # KNOBS
    MIX_TRACK = 70
    MIX_VOL = 71
    MIX_PAN = 72
    MIX_SS = 73
    CHAN_SEL = 74
    CHAN_VOL = 75
    CHAN_PAN = 76
    FIX_VEL = 77

    # Original Shift button is reserved by Maschine
    # so we assign it to another CC that is not used (FOLLOW)
    SHIFT = 46
