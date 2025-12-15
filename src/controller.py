"""NI Maschine MK3 Controller abstract class"""

import ui
import midi
import mixer
import channels
import transport

from colors import *
from controls import *
from utilities import *

__all__ = ["Controller"]


class Controller:
    """Represents the state of the Maschine MK3 controller"""

    _channel_page: int
    """Current channel page (0-15) for channel rack pad display"""

    _plugin_picker_active: bool
    """Indicates whether the plugin picker is currently active"""

    def __init__(self):
        self._channel_page = 0
        self._plugin_picker_active = False

    def OnInit(self) -> None:
        self._init_led_states()
        self._sync_led_states()
        self._sync_channel_rack_controls()
        self._sync_mixer_controls()

    def OnDeInit(self) -> None:
        self._deinit_led_states()

    def OnRefresh(self, flags: int) -> None:
        print(f"flags: {flags}")
        if flags & midi.HW_Dirty_Mixer_Sel:
            print("flags & midi.HW_Dirty_Mixer_Sel")
        if flags & midi.HW_Dirty_Mixer_Display:
            print("midi.HW_Dirty_Mixer_Display")
        if flags & midi.HW_Dirty_Mixer_Controls:
            print("midi.HW_Dirty_Mixer_Controls")
        if flags & midi.HW_Dirty_FocusedWindow:
            print("midi.HW_Dirty_FocusedWindow")
        if flags & midi.HW_Dirty_Performance:
            print("midi.HW_Dirty_Performance")
        if flags & midi.HW_Dirty_LEDs:
            print("midi.HW_Dirty_LEDs")
            self._sync_led_states()
        if flags & midi.HW_Dirty_Patterns:
            print("midi.HW_Dirty_Patterns")
        if flags & midi.HW_Dirty_Tracks:
            print("midi.HW_Dirty_Tracks")
        if flags & midi.HW_Dirty_ControlValues:
            print("midi.HW_Dirty_ControlValues")
            if not self._plugin_picker_active:
                self._sync_channel_rack_controls()
        if flags & midi.HW_Dirty_Colors:
            print("midi.HW_Dirty_Colors")
        if flags & midi.HW_Dirty_Names:
            print("midi.HW_Dirty_Names")
        if flags & midi.HW_Dirty_ChannelRackGroup:
            print("midi.HW_Dirty_ChannelRackGroup")
        if flags & midi.HW_ChannelEvent:
            print("midi.HW_ChannelEvent")
            self._sync_channel_rack_pads()
            if not self._plugin_picker_active:
                self._sync_channel_rack_controls()

    def _init_led_states(self) -> None:
        self._deinit_led_states()

        for i in range(30, 34):
            _midi_out_msg_control_change(i, Green3)

        # fmt: off
        _midi_out_msg_control_change(CC_TOUCH_STRIP, int(transport.getSongPos() * 127))
        _midi_out_msg_control_change(CC_PAD_GROUP_A, White1)
        _midi_out_msg_control_change(CC_PAD_MODE, 127)
        _midi_out_msg_control_change(CC_FIX_VEL, 100)
        # fmt: on

    @staticmethod
    def _deinit_led_states() -> None:
        """De-initializes the LED states on the Maschine MK3 device"""
        for i in range(127):
            _midi_out_msg_control_change(i, Black0)
            _midi_out_msg_note_on(i, Black0)

    def _sync_led_states(self) -> None:
        """Syncs the LED states with the current FL Studio state"""

        # fmt: off
        _midi_out_msg_control_change(CC_CHANNEL,  _on_off(ui.getVisible(midi.widChannelRack)))
        _midi_out_msg_control_change(CC_ARRANGER, _on_off(ui.getVisible(midi.widPlaylist)))
        _midi_out_msg_control_change(CC_MIXER,    _on_off(ui.getVisible(midi.widMixer)))
        _midi_out_msg_control_change(CC_SAMPLING, _on_off(ui.getVisible(midi.widBrowser)))
        _midi_out_msg_control_change(CC_PLAY,     _on_off(transport.isPlaying()))
        _midi_out_msg_control_change(CC_REC,      _on_off(transport.isRecording()))
        _midi_out_msg_control_change(CC_FOLLOW,   _on_off(ui.isMetronomeEnabled()))
        _midi_out_msg_control_change(CC_STOP,     _on_off(not transport.isPlaying()))
        _midi_out_msg_control_change(CC_LOOP,     _on_off(bool(transport.getLoopMode())))
        _midi_out_msg_control_change(CC_LOCK,     _on_off(ui.getSnapMode() != 3))
        # fmt: on

        self._sync_channel_rack_pads()

    def _sync_channel_rack_pads(self) -> None:
        """Syncs the channel rack state with the pad LEDs on the Maschine MK3 device"""

        # NOTE: Need to check range later
        for i in range(127):
            _midi_out_msg_note_on(i, Black0)

        lower_channel = self._channel_page * 16
        channel_count = channels.channelCount()
        selected_channel = channels.selectedChannel()

        # turn on pads for available channels
        for channel in range(lower_channel, channel_count):
            idx = channel - lower_channel
            if idx == 16:
                break
            _midi_out_msg_note_on(idx, _get_channel_color(channel, False))

        # highlight selected channel pad
        if selected_channel in range(lower_channel, channel_count):
            channel = selected_channel - lower_channel
            _midi_out_msg_note_on(channel, _get_channel_color(channel, True))

    @staticmethod
    def _sync_channel_rack_controls() -> None:
        """Syncs the channel rack controls on the Maschine MK3 device with the current FL Studio channel rack state"""

        selected_channel = channels.selectedChannel()

        # fmt: off
        _midi_out_msg_control_change(CC_CHAN_SEL, selected_channel)
        _midi_out_msg_control_change(CC_CHAN_VOL, round(channels.getChannelVolume(selected_channel) * 100))
        _midi_out_msg_control_change(CC_CHAN_PAN, round((channels.getChannelPan(selected_channel) * 50) + 50))
        # fmt: on

    @staticmethod
    def _sync_mixer_controls() -> None:
        """Syncs the mixer (encoders) values on the Maschine MK3 device with the current FL Studio mixer state"""

        track_number = mixer.trackNumber()

        # fmt: off
        _midi_out_msg_control_change(CC_MIX_TRACK, track_number)
        _midi_out_msg_control_change(CC_MIX_VOLUME, round(mixer.getTrackVolume(track_number) * 125))
        _midi_out_msg_control_change(CC_MIX_PAN, round((mixer.getTrackPan(track_number) * 50) + 50))
        _midi_out_msg_control_change(CC_MIX_STEREO, round((mixer.getTrackStereoSep(track_number) + 1) * 50))
        # fmt: on
