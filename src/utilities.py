from enum import Enum

import midi
import device
import plugins

from consts import PAD_COUNT
from enums import ControllerColor
from pads import PadMode, PadModeColor

__all__ = [
    "_midi_out_msg_note_on",
    "_midi_out_msg_control_change",
    "_on_off",
    "_percent_to_bipolar",
    "_bipolar_to_percent",
    "_is_enum_value",
    "_get_grid",
    "_get_channel_color",
    "_print_on_refresh_flags",
]


def _midi_out_msg_note_on(
    note: int,
    velocity: int,
    channel: int = 0,
) -> None:
    """
    Send a MIDI NOTE ON (144) message to the device.

    This is a thin wrapper around `device.midiOutMsg` that sends a NOTE ON
    message on the specified MIDI channel. A velocity of 0 is treated by
    MIDI devices as NOTE OFF.

    Args:
        note (int): MIDI note number (0–127).
        velocity (int): Note velocity (0–127). A value of 0 acts as NOTE OFF.
        channel (int, optional): MIDI channel (0–15). Defaults to 0.

    Returns:
        None
    """
    device.midiOutMsg(
        midi.MIDI_NOTEON,
        channel,
        note,
        velocity,
    )


def _midi_out_msg_control_change(
    control: int,
    value: int,
    channel: int = 0,
) -> None:
    """
    Send a MIDI CONTROL CHANGE (CC) (176) message to the device.

    This is a thin wrapper around `device.midiOutMsg` that sends a Control
    Change message on the specified MIDI channel.

    Args:
        control (int): MIDI controller number (0–127).
        value (int): Controller value (0–127).
        channel (int, optional): MIDI channel (0–15). Defaults to 0.

    Returns:
        None
    """
    device.midiOutMsg(
        midi.MIDI_CONTROLCHANGE,
        channel,
        control,
        value,
    )


def _on_off(condition: bool) -> int:
    """Helper to convert boolean to MIDI on/off value
    Args:
        condition (bool): Condition to evaluate
    Returns:
        int: 127 if condition is True, else 0
    """
    return 127 if condition else 0


def _percent_to_bipolar(percent: int) -> float:
    """Convert a percent value (0-100) to a bipolar value (-1.0 to 1.0)"""
    return (percent / 50.0) - 1.0


def _bipolar_to_percent(bipolar: float) -> int:
    """Convert a bipolar value (-1.0 to 1.0) to a percent value (0-100)"""
    return round((bipolar + 1.0) * 50)


def _is_enum_value(enum_cls: type[Enum], value: object) -> bool:
    """Check if a value is a valid member of the given Enum class"""
    try:
        enum_cls(value)
        return True
    except ValueError:
        return False


def _get_grid(page: int) -> range:
    """Get the step grid range for a given offset (page)"""
    lower_step = page * PAD_COUNT
    return range(lower_step, lower_step + PAD_COUNT)


def _get_channel_color(
    channel: int,
    pad_mode: PadMode,
    highlighted: bool,
) -> int:
    """
    Return the LED color for a channel or plugin pad.

    Args:
        channel: Channel index to test for plugin validity.
        pad_mode: Current pad mode.
        highlighted: Whether the pad should use the highlighted color.

    Returns:
        MIDI color value for the pad LED.
    """
    if plugins.isValid(channel):
        color = PadModeColor[str(pad_mode.name)]
    else:
        color = ControllerColor.WHITE_2
    return color if highlighted else color - 2


def _print_on_refresh_flags(flags: int) -> None:
    """Print debugging output for refresh flags"""

    if flags & midi.HW_Dirty_Mixer_Sel:
        print("HW_Dirty_Mixer_Sel")
    if flags & midi.HW_Dirty_Mixer_Display:
        print("HW_Dirty_Mixer_Display")
    if flags & midi.HW_Dirty_Mixer_Controls:
        print("HW_Dirty_Mixer_Controls")
    if flags & midi.HW_Dirty_FocusedWindow:
        print("HW_Dirty_FocusedWindow")
    if flags & midi.HW_Dirty_Performance:
        print("HW_Dirty_Performance")
    if flags & midi.HW_Dirty_LEDs:
        print("HW_Dirty_LEDs")
    if flags & midi.HW_Dirty_Patterns:
        print("HW_Dirty_Patterns")
    if flags & midi.HW_Dirty_Tracks:
        print("HW_Dirty_Tracks")
    if flags & midi.HW_Dirty_ControlValues:
        print("HW_Dirty_ControlValues")
    if flags & midi.HW_Dirty_Colors:
        print("HW_Dirty_Colors")
    if flags & midi.HW_Dirty_Names:
        print("HW_Dirty_Names")
    if flags & midi.HW_Dirty_ChannelRackGroup:
        print("HW_Dirty_ChannelRackGroup")
    if flags & midi.HW_ChannelEvent:
        print("HW_ChannelEvent")
