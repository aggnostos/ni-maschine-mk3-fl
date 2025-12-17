"""NI Maschine MK3 Controller abstract class"""

import ui
import midi
import mixer
import plugins
import general
import patterns
import channels
import transport
from fl_classes import FlMidiMsg

from enums import *
from consts import *
from colors import *
from controls import *
from utilities import *

__all__ = ["Controller"]


class Controller:
    """Represents the state of the Maschine MK3 controller"""

    _pad_mode: PadMode
    """Current pad mode. See PadMode Enum"""

    _encoder_mode: FourDEncoderMode
    """Current 4D encoder mode. See FourDEncoderMode Enum"""

    _touch_strip_mode: TouchStripMode
    """Current touch strip mode. See TouchStripMode Enum"""

    _selected_group: Group
    """Current selected group (A-H)"""

    _channel_page: int
    """Current channel page (0-15) for channel rack pad display"""

    _step_channel_page: int
    """Current channel page (0-15) for step mode pad display"""

    _fixed_velocity: int
    """Fixed velocity value for pads when fixed velocity mode is enabled"""

    _is_fixed_velocity: bool
    """Indicates whether fixed velocity mode is enabled"""

    _shifting: bool
    """Indicates whether the shift button is currently pressed"""

    _is_plugin_picker_active: bool
    """Indicates whether the plugin picker is currently active"""

    _is_selecting_pattern: bool
    """Indicates whether the user is currently selecting a pattern"""

    def __init__(self):
        self._pad_mode = PadMode.OMNI
        self._encoder_mode = FourDEncoderMode.JOG
        self._touch_strip_mode = TouchStripMode.DISABLED
        self._selected_group = Group.A
        self._channel_page = 0
        self._step_channel_page = 0
        self._fixed_velocity = 100
        self._is_fixed_velocity = False
        self._shifting = False
        self._is_plugin_picker_active = False
        self._is_selecting_pattern = False

    def OnInit(self) -> None:
        self._init_led_states()
        self._sync_led_states()
        self._sync_channel_rack_controls()
        self._sync_mixer_controls()

    def OnDeInit(self) -> None:
        self._deinit_led_states()

    def OnRefresh(self, flags: int) -> None:
        # print(f"flags: {flags}")
        if flags & midi.HW_Dirty_Mixer_Sel:
            print("flags & midi.HW_Dirty_Mixer_Sel")
        if flags & midi.HW_Dirty_Mixer_Display:
            print("midi.HW_Dirty_Mixer_Display")
        if flags & midi.HW_Dirty_Mixer_Controls:
            print("midi.HW_Dirty_Mixer_Controls")
            if not self._is_plugin_picker_active:
                self._sync_mixer_controls()
        if flags & midi.HW_Dirty_FocusedWindow:
            print("midi.HW_Dirty_FocusedWindow")
        if flags & midi.HW_Dirty_Performance:
            print("midi.HW_Dirty_Performance")
        if flags & midi.HW_Dirty_LEDs:
            print("midi.HW_Dirty_LEDs")
            self._sync_led_states()
        if flags & midi.HW_Dirty_Patterns:
            print("midi.HW_Dirty_Patterns")
            if not self._is_selecting_pattern:
                self._sync_channel_rack_pads()
        if flags & midi.HW_Dirty_Tracks:
            print("midi.HW_Dirty_Tracks")
        if flags & midi.HW_Dirty_ControlValues:
            print("midi.HW_Dirty_ControlValues")
            self._sync_touch_strip_value(self._touch_strip_mode)
            if not self._is_plugin_picker_active:
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
            if not self._is_plugin_picker_active:
                self._sync_channel_rack_controls()

    def OnControlChange(self, msg: FlMidiMsg) -> None:
        cc_num, cc_val = msg.controlNum, msg.controlVal
        print(f"CC Num: {cc_num}, CC Val: {cc_val}")
        match cc_num:
            # -------- CONTROL BUTTONS SECTION -------- #
            case CC.CHANNEL:
                if ui.getVisible(midi.widChannelRack):
                    ui.hideWindow(midi.widChannelRack)
                else:
                    ui.showWindow(midi.widChannelRack)

            case CC.PLUGIN:
                channels.showCSForm(channels.selectedChannel(), -1)

            case CC.ARRANGER:
                if ui.getVisible(midi.widPlaylist):
                    ui.hideWindow(midi.widPlaylist)
                else:
                    ui.showWindow(midi.widPlaylist)

            case CC.MIXER:
                if ui.getVisible(midi.widMixer):
                    ui.hideWindow(midi.widMixer)
                else:
                    ui.showWindow(midi.widMixer)

            case CC.BROWSER if self._shifting:  # PLUGIN PICKER
                self._is_plugin_picker_active = not self._is_plugin_picker_active
                transport.globalTransport(midi.FPT_F8, 1)
            case CC.BROWSER:
                if ui.getVisible(midi.widBrowser):
                    ui.hideWindow(midi.widBrowser)
                else:
                    ui.showWindow(midi.widBrowser)

            case CC.FILE_SAVE:
                transport.globalTransport(midi.FPT_Save, 1)

            case CC.SETTINGS:
                transport.globalTransport(midi.FPT_F10, 1)

            # -------- EDIT (ENCODER) SECTION -------- #
            case CC.ENCODER_PUSH:
                ui.enter()

            case CC.ENCODER_TURN:
                is_clockwise = cc_val == 65  # CLOCKWISE
                multiplier = 1 if is_clockwise else -1

                track_number = mixer.trackNumber()
                selected_channel = channels.selectedChannel()

                match self._encoder_mode:
                    case FourDEncoderMode.JOG:
                        ui.jog(1 * multiplier)

                    case FourDEncoderMode.VOLUME:
                        if ui.getFocused(midi.widMixer):
                            target_vol = (
                                mixer.getTrackVolume(track_number)
                                + 0.012125 * multiplier
                            )
                            if 0.0 < target_vol < 1.0:
                                mixer.setTrackVolume(track_number, target_vol)
                        elif ui.getFocused(midi.widChannelRack):
                            channels.setChannelVolume(
                                selected_channel,
                                channels.getChannelVolume(selected_channel)
                                + 0.03125 * multiplier,
                            )

                    case FourDEncoderMode.SWING:
                        pass  # TODO implement swing adjustment

                    case FourDEncoderMode.TEMPO:
                        transport.globalTransport(midi.FPT_TempoJog, 10 * multiplier)

            case CC.ENCODER_UP | CC.ENCODER_RIGHT | CC.ENCODER_DOWN | CC.ENCODER_LEFT:
                match cc_num:
                    case CC.ENCODER_UP:
                        ui.up()
                    case CC.ENCODER_RIGHT:
                        ui.right()
                    case CC.ENCODER_DOWN:
                        ui.down()
                    case CC.ENCODER_LEFT:
                        ui.left()
                    case _:
                        pass

            case CC.ENCODER_VOLUME | CC.ENCODER_SWING | CC.ENCODER_TEMPO:
                self._toggle_encoder_mode(cc_num)

            # -------- TOUCH STRIP SECTION -------- #
            case CC.TOUCH_STRIP:
                selected_channel = channels.selectedChannel()
                match self._touch_strip_mode:
                    case TouchStripMode.PITCH:
                        channels.setChannelPitch(selected_channel, (cc_val / 50) - 1)
                    case TouchStripMode.MOD:
                        pass  # TODO
                    case TouchStripMode.PERFORM:
                        pass  # TODO
                    case TouchStripMode.NOTES:
                        pass  # TODO
                    case TouchStripMode.DISABLED:
                        pass

            # fmt: off
            case CC.TOUCH_STRIP_PITCH | CC.TOUCH_STRIP_MOD | CC.TOUCH_STRIP_PERFORM | CC.TOUCH_STRIP_NOTES:
            # fmt: on
                self._toggle_touch_strip_mode(cc_num)
                self._sync_touch_strip_value(self._touch_strip_mode)

            # -------- GROUP SECTION -------- #
            # fmt: off
            case CC.GROUP_A | CC.GROUP_B | CC.GROUP_C | CC.GROUP_D | CC.GROUP_E | CC.GROUP_F | CC.GROUP_G | CC.GROUP_H:
            # fmt: on
                for cc in GROUPS_RANGE:
                    _midi_out_msg_control_change(cc, White1 if cc == cc_num else Black0)

                page_idx = cc_num - 100

                match self._pad_mode:
                    case PadMode.OMNI:
                        self._channel_page = page_idx
                    case PadMode.STEP:
                        self._step_channel_page = page_idx
                    case _:
                        return
                    
                self._sync_channel_rack_pads()

            # -------- TRASPORT SECTION -------- #
            case CC.RESTART if self._shifting:  # LOOP
                transport.setLoopMode()
            case CC.RESTART:
                transport.stop()
                transport.start()

            case CC.ERASE:
                ui.delete()

            case CC.TAP if self._shifting:  # METRO
                transport.globalTransport(midi.FPT_Metronome, 1)
            case CC.TAP:
                if cc_val:
                    transport.globalTransport(midi.FPT_TapTempo, 1)

            case CC.PLAY:
                transport.start()

            case CC.REC if self._shifting:  # Count-in
                transport.globalTransport(midi.FPT_CountDown, 1)
            case CC.REC:
                transport.record()

            case CC.STOP:
                transport.stop()

            case CC.GRID:
                ui.snapOnOff()

            # -------- PAD SECTION -------- #
            case CC.FIXED_VEL:
                self._is_fixed_velocity = bool(cc_val)

            # TODO PAD MODES
            case CC.PAD_MODE | CC.KEYBOARD_MODE | CC.CHORDS_MODE | CC.STEP_MODE:
                for cc in (CC.PAD_MODE, CC.KEYBOARD_MODE, CC.CHORDS_MODE, CC.STEP_MODE):
                    _midi_out_msg_control_change(cc, 127 if cc == cc_num else 0)

                match cc_num:
                    case CC.PAD_MODE:
                        self._pad_mode = PadMode.OMNI

                    case CC.KEYBOARD_MODE:
                        self._pad_mode = PadMode.KEYBOARD

                    case CC.CHORDS_MODE:
                        self._pad_mode = PadMode.CHORDS

                    case CC.STEP_MODE:
                        self._pad_mode = PadMode.STEP

                    case _:
                        pass

                self._sync_channel_rack_pads()

            case CC.PATTERN:
                for p in range(16):
                    _midi_out_msg_note_on(p, Black0)

                if cc_val:
                    self._is_selecting_pattern = True
                    for pattern in range(patterns.patternCount()):
                        _midi_out_msg_note_on(pattern, Lime1)
                else:
                    self._is_selecting_pattern = False
                    if self._pad_mode in (PadMode.OMNI, PadMode.STEP):
                        self._sync_channel_rack_pads()

            case CC.SOLO:
                if ui.getFocused(midi.widChannelRack):
                    channels.soloChannel(channels.selectedChannel())
                elif ui.getFocused(midi.widMixer):
                    mixer.soloTrack(mixer.trackNumber())

            case CC.MUTE:
                if ui.getFocused(midi.widChannelRack):
                    channels.muteChannel(channels.selectedChannel())
                elif ui.getFocused(midi.widMixer):
                    mixer.muteTrack(mixer.trackNumber())

            # ---- KNOB PAGE SECTION ---- #
            # BUTTONS
            case CC.PRESET_NEXT | CC.PRESET_PREV:
                selected_channel = channels.selectedChannel()
                
                if not plugins.isValid(selected_channel):
                    return
                
                if cc_num == CC.PRESET_NEXT:
                    plugins.nextPreset(selected_channel)
                else:
                    plugins.prevPreset(selected_channel)

            # KNOBS
            case CC.MIX_TRACK:
                mixer.setTrackNumber(cc_val)

            case CC.MIX_VOL:
                mixer.setTrackVolume(mixer.trackNumber(), cc_val / 125)

            case CC.MIX_PAN:
                mixer.setTrackPan(mixer.trackNumber(), (cc_val - 50) / 50)

            case CC.MIX_SS:
                mixer.setTrackStereoSep(mixer.trackNumber(), (cc_val / 50) - 1)

            case CC.CHAN_SEL:
                if cc_val < channels.channelCount():
                    channels.selectOneChannel(cc_val)
                else:
                    _midi_out_msg_control_change(
                        CC.CHAN_SEL, channels.selectedChannel()
                    )

            case CC.CHAN_VOL:
                channels.setChannelVolume(channels.selectedChannel(), cc_val / 100)

            case CC.CHAN_PAN:
                channels.setChannelPan(channels.selectedChannel(), (cc_val - 50) / 50)

            case CC.FIX_VEL:
                self._fixed_velocity = cc_val

            # -------- SHIFT -------- #
            case CC.SHIFT:
                self._shifting = bool(cc_val)

            # -------- DEFAULT -------- #
            case _:
                return

        # We will reach here if a case matched and was handled
        # so we don't have to explicitly set event.handled = True in each case
        # otherwise we would have returned earlier to let FL Studio handle it itself
        msg.handled = True

    def OnNoteOn(self, msg: FlMidiMsg) -> None:
        note_num, note_vel = msg.note, msg.velocity
        # velocity == 0 means note off

        if note_vel:
            if self._shifting:
                if note_num == 0:
                    general.undoUp()
                elif note_num == 1:
                    general.undoDown()
                msg.handled = True
            if self._is_selecting_pattern:
                patterns.jumpToPattern(note_num + 1)
                msg.handled = True

        if msg.handled:
            return

        msg.handled = True

        print(f"Note Num: {note_num}, Note Vel: {note_vel}")

    def _init_led_states(self) -> None:
        self._deinit_led_states()

        # fmt: off
        _midi_out_msg_control_change(CC.TOUCH_STRIP, int(transport.getSongPos() * 127))
        _midi_out_msg_control_change(CC.GROUP_A, White1)
        _midi_out_msg_control_change(CC.PAD_MODE, 127)
        _midi_out_msg_control_change(CC.FIX_VEL, 100)
        # fmt: on

    @staticmethod
    def _deinit_led_states() -> None:
        """De-initializes the LED states on the Maschine MK3 device"""

        for i in range(128):
            _midi_out_msg_control_change(i, Black0)
            _midi_out_msg_note_on(i, Black0)

    def _sync_led_states(self) -> None:
        """Syncs the LED states with the current FL Studio state"""

        # fmt: off
        _midi_out_msg_control_change(CC.RESTART,  _on_off(bool(transport.getLoopMode())))
        _midi_out_msg_control_change(CC.TAP,      _on_off(general.getUseMetronome()))
        _midi_out_msg_control_change(CC.PLAY,     _on_off(transport.isPlaying()))
        _midi_out_msg_control_change(CC.REC,      _on_off(transport.isRecording()))
        _midi_out_msg_control_change(CC.STOP,     _on_off(not transport.isPlaying()))
        _midi_out_msg_control_change(CC.GRID,     _on_off(ui.getSnapMode() != 3))
        _midi_out_msg_control_change(CC.CHANNEL,  _on_off(ui.getVisible(midi.widChannelRack)))
        _midi_out_msg_control_change(CC.ARRANGER, _on_off(ui.getVisible(midi.widPlaylist)))
        _midi_out_msg_control_change(CC.MIXER,    _on_off(ui.getVisible(midi.widMixer)))
        _midi_out_msg_control_change(CC.BROWSER,  _on_off(ui.getVisible(midi.widBrowser)))
        # fmt: on

        self._sync_channel_rack_pads()

    def _sync_channel_rack_pads(self) -> None:
        """Syncs the channel rack state with the pad LEDs on the Maschine MK3 device"""

        # NOTE: Need to check range later
        for i in range(128):
            _midi_out_msg_note_on(i, Black0)

        selected_channel = channels.selectedChannel()

        if self._pad_mode == PadMode.OMNI:
            lower_channel = self._channel_page * 16
            channel_count = channels.channelCount()

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

        if self._pad_mode == PadMode.STEP:
            lower_step = self._step_channel_page * 16

            # turn on pads for step sequencer grid bits
            for gridbit in range(lower_step, lower_step + 16):
                idx = gridbit - lower_step
                if idx == 16:
                    break
                _midi_out_msg_note_on(
                    idx,
                    Lime1 if channels.getGridBit(selected_channel, gridbit) else Black0,
                )

    @staticmethod
    def _sync_channel_rack_controls() -> None:
        """Syncs the channel rack controls on the Maschine MK3 device with the current FL Studio channel rack state"""

        selected_channel = channels.selectedChannel()

        # fmt: off
        _midi_out_msg_control_change(CC.CHAN_SEL, selected_channel)
        _midi_out_msg_control_change(CC.CHAN_VOL, round(channels.getChannelVolume(selected_channel) * 100))
        _midi_out_msg_control_change(CC.CHAN_PAN, round((channels.getChannelPan(selected_channel) * 50) + 50))
        _midi_out_msg_control_change(CC.SOLO, _on_off(channels.isChannelSolo(selected_channel)))
        _midi_out_msg_control_change(CC.MUTE, _on_off(channels.isChannelMuted(selected_channel)))        
        # fmt: on

    @staticmethod
    def _sync_mixer_controls() -> None:
        """Syncs the mixer (encoders) values on the Maschine MK3 device with the current FL Studio mixer state"""

        track_number = mixer.trackNumber()

        # fmt: off
        _midi_out_msg_control_change(CC.MIX_TRACK, track_number)
        _midi_out_msg_control_change(CC.MIX_VOL, round(mixer.getTrackVolume(track_number) * 125))
        _midi_out_msg_control_change(CC.MIX_PAN, round((mixer.getTrackPan(track_number) * 50) + 50))
        _midi_out_msg_control_change(CC.MIX_SS, round((mixer.getTrackStereoSep(track_number) + 1) * 50))
        _midi_out_msg_control_change(CC.SOLO, _on_off(mixer.isTrackSolo(track_number)))
        _midi_out_msg_control_change(CC.MUTE, _on_off(mixer.isTrackMuted(track_number)))
        # fmt: on

    def _toggle_encoder_mode(self, cc: int) -> None:
        """Toggles the 4D encoder mode based on the given control change number"""

        match cc:
            case CC.ENCODER_VOLUME:
                mode = FourDEncoderMode.VOLUME
            case CC.ENCODER_SWING:
                mode = FourDEncoderMode.SWING
            case CC.ENCODER_TEMPO:
                mode = FourDEncoderMode.TEMPO
            case _:
                mode = FourDEncoderMode.JOG

        mode = mode if self._encoder_mode != mode else FourDEncoderMode.JOG

        for cc_num in (CC.ENCODER_VOLUME, CC.ENCODER_SWING, CC.ENCODER_TEMPO):
            _midi_out_msg_control_change(
                cc_num,
                (127 if cc == cc_num and mode != FourDEncoderMode.JOG else 0),
            )

        self._encoder_mode = mode

    def _toggle_touch_strip_mode(self, cc: int) -> None:
        """Toggles the touch strip mode based on the given control change number"""

        match cc:
            case CC.TOUCH_STRIP_PITCH:
                mode = TouchStripMode.PITCH
            case CC.TOUCH_STRIP_MOD:
                mode = TouchStripMode.MOD
            case CC.TOUCH_STRIP_PERFORM:
                mode = TouchStripMode.PERFORM
            case CC.TOUCH_STRIP_NOTES:
                mode = TouchStripMode.NOTES
            case _:
                mode = TouchStripMode.DISABLED

        mode = mode if self._touch_strip_mode != mode else TouchStripMode.DISABLED

        # fmt: off
        for cc_num in (CC.TOUCH_STRIP_PITCH, CC.TOUCH_STRIP_MOD, CC.TOUCH_STRIP_PERFORM, CC.TOUCH_STRIP_NOTES):
        # fmt: on
            _midi_out_msg_control_change(
                cc_num,
                (127 if cc == cc_num and mode != TouchStripMode.DISABLED else 0),
            )

        self._touch_strip_mode = mode

    def _sync_touch_strip_value(self, mode: TouchStripMode) -> None:
        """Syncs the touch strip value on the Maschine MK3 device with the current FL Studio state based on the given mode"""

        match mode:
            case TouchStripMode.PITCH:
                _midi_out_msg_control_change(
                    CC.TOUCH_STRIP,
                    round(channels.getChannelPitch(channels.selectedChannel()) * 50)
                    + 50,
                )
            case TouchStripMode.MOD:
                pass  # TODO
            case TouchStripMode.PERFORM:
                pass  # TODO
            case TouchStripMode.NOTES:
                pass  # TODO
            case TouchStripMode.DISABLED:
                _midi_out_msg_control_change(CC.TOUCH_STRIP, 0)
