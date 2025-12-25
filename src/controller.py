import ui
import midi
import mixer
import plugins
import general
import patterns
import channels
import transport
from fl_classes import FlMidiMsg

from pads import *
from enums import *
from notes import *
from consts import *
from controls import *
from utilities import *

__all__ = ["Controller"]


class Controller:
    """Represents the state of the Maschine MK3 controller"""

    _pad_mode: PadMode
    """Current pad mode. See PadMode Enum"""

    _pad_mode_color: PadModeColor
    """Current pad mode color. See PadModeColor Enum"""

    _encoder_mode: FourDEncoderMode
    """Current 4D encoder mode. See FourDEncoderMode Enum"""

    _touch_strip_mode: TouchStripMode
    """Current touch strip mode. See TouchStripMode Enum"""

    _active_group: PadGroup
    """Current selected group (A-H)"""

    _selected_channel: int
    """Currently selected channel index"""

    _channel_page: int
    """Current channel page (0-15) for OMNI mode pad display"""

    _step_page: int
    """Current step sequence page (0-15) for STEP mode pad display"""

    _semi_offset: int
    """Current semitone offset"""

    _scale_index: int
    """Current scale index for keyboard mode (0-7)"""

    _chordset_index: int
    """Current chord set index for chords mode (0-7)"""

    _fixed_velocity: int
    """Fixed velocity value for pads when fixed velocity mode is enabled"""

    _is_fixed_velocity: bool
    """Indicates whether fixed velocity mode is enabled"""

    _shifting: bool
    """Indicates whether the shift button is currently pressed"""

    _is_selecting_pattern: bool
    """Indicates whether the user is currently selecting a pattern"""

    _is_selecting_channel: bool
    """Indicates whether the user is currently selecting a channel"""

    def __init__(self):
        self._pad_mode = PadMode.OMNI
        self._pad_mode_color = PadModeColor.OMNI
        self._encoder_mode = FourDEncoderMode.JOG
        self._touch_strip_mode = TouchStripMode.TRANSPORT
        self._active_group = PadGroup.A
        self._selected_channel = 0
        self._channel_page = 0
        self._step_page = 0
        self._semi_offset = 0
        self._scale_index = 0
        self._chordset_index = 0
        self._fixed_velocity = 100
        self._is_fixed_velocity = False
        self._shifting = False
        self._is_selecting_pattern = False
        self._is_selecting_channel = False

    def on_init(self) -> None:
        self._init_led_states()
        self._sync_cc_led_states()
        self._sync_selected_channel()
        self._sync_channel_pads()
        self._sync_channel_controls()
        self._sync_mixer_controls()
        self._sync_song_position()

    def on_de_init(self) -> None:
        self._deinit_led_states()

    def on_refresh(self, flags: int) -> None:
        # `flags` is a bitmask — a single integer where each bit represents a different type of state change,
        # allowing multiple updates to be signaled at once.

        channel_event = flags & midi.HW_ChannelEvent
        pattern_event = flags & midi.HW_Dirty_Patterns
        control_values_event = flags & midi.HW_Dirty_ControlValues
        mixer_sel_event = flags & midi.HW_Dirty_Mixer_Sel
        mixer_display_event = flags & midi.HW_Dirty_Mixer_Display
        mixer_controls_event = flags & midi.HW_Dirty_Mixer_Controls
        leds_event = flags & midi.HW_Dirty_LEDs

        # This `elif` block is needed because `leds_event` is triggered alongside other events
        # so we only want to run the full leds sync logic when no other events are present.
        # e.g. `leds_event` is triggered alongside `channel_event`, so we only want to sync leds
        # that are related to `channel_event` in that case.
        if channel_event:
            self._sync_selected_channel()
            self._sync_channel_controls()
            self._sync_channel_pads()
        elif mixer_sel_event or mixer_display_event or mixer_controls_event:
            self._sync_mixer_controls()
        elif leds_event:
            self._sync_cc_led_states()
            if self._touch_strip_mode == TouchStripMode.TRANSPORT:
                self._sync_song_position()
            if not self._is_selecting_pattern:
                self._sync_channel_pads()

        # for some reason turning record on/off triggers `mixer_controls_event` alongside `leds_event`,
        # so we need to handle it separately
        if mixer_controls_event and leds_event:
            _midi_out_msg_control_change(CC.REC, _on_off(transport.isRecording()))

        if pattern_event:
            self._sync_channel_pads()

        if control_values_event:
            if self._touch_strip_mode == TouchStripMode.PITCH:
                self._sync_touch_strip_value(self._touch_strip_mode)
            self._sync_channel_controls()

        # # Debugging output for refresh flags
        # if flags & midi.HW_Dirty_Mixer_Sel:
        #     print("midi.HW_Dirty_Mixer_Sel")
        # if flags & midi.HW_Dirty_Mixer_Display:
        #     print("midi.HW_Dirty_Mixer_Display")
        # if flags & midi.HW_Dirty_Mixer_Controls:
        #     print("midi.HW_Dirty_Mixer_Controls")
        # if flags & midi.HW_Dirty_FocusedWindow:
        #     print("midi.HW_Dirty_FocusedWindow")
        # if flags & midi.HW_Dirty_Performance:
        #     print("midi.HW_Dirty_Performance")
        # if flags & midi.HW_Dirty_LEDs:
        #     print("midi.HW_Dirty_LEDs")
        # if flags & midi.HW_Dirty_Patterns:
        #     print("midi.HW_Dirty_Patterns")
        # if flags & midi.HW_Dirty_Tracks:
        #     print("midi.HW_Dirty_Tracks")
        # if flags & midi.HW_Dirty_ControlValues:
        #     print("midi.HW_Dirty_ControlValues")
        # if flags & midi.HW_Dirty_Colors:
        #     print("midi.HW_Dirty_Colors")
        # if flags & midi.HW_Dirty_Names:
        #     print("midi.HW_Dirty_Names")
        # if flags & midi.HW_Dirty_ChannelRackGroup:
        #     print("midi.HW_Dirty_ChannelRackGroup")
        # if flags & midi.HW_ChannelEvent:
        #     print("midi.HW_ChannelEvent")

    def on_control_change(self, msg: FlMidiMsg) -> None:
        cc_num, cc_val = msg.controlNum, msg.controlVal

        match cc_num:
            # -------- CONTROL BUTTONS SECTION -------- #
            case CC.CHANNEL | CC.ARRANGER | CC.MIXER | CC.BROWSER:
                match cc_num:
                    case CC.CHANNEL:
                        wid = midi.widChannelRack
                    case CC.ARRANGER:
                        wid = midi.widPlaylist
                    case CC.MIXER:
                        wid = midi.widMixer
                    case CC.BROWSER:
                        wid = midi.widBrowser
                    case _:
                        return

                is_visible = ui.getVisible(wid)

                if self._shifting:
                    if not is_visible:
                        ui.showWindow(wid)
                    ui.setFocused(wid)
                else:
                    if is_visible:
                        ui.hideWindow(wid)
                    else:
                        ui.showWindow(wid)

                is_visible = ui.getVisible(wid)

                _midi_out_msg_control_change(cc_num, _on_off(is_visible))

            case CC.PLUGIN:
                channels.showCSForm(self._selected_channel, -1)

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

                match self._encoder_mode:
                    case FourDEncoderMode.JOG:
                        ui.jog(1 * multiplier)

                    case FourDEncoderMode.VOLUME:
                        if ui.getFocused(midi.widMixer):
                            target_vol = (
                                mixer.getTrackVolume(track_number)
                                + MIXER_TRACK_VOL_STEP * multiplier
                            )
                            if 0.0 < target_vol < 1.0:
                                mixer.setTrackVolume(track_number, target_vol)
                        elif ui.getFocused(midi.widChannelRack):
                            channels.setChannelVolume(
                                self._selected_channel,
                                channels.getChannelVolume(self._selected_channel)
                                + CHANNEL_VOL_STEP * multiplier,
                            )

                    case FourDEncoderMode.SWING:
                        swing = general.processRECEvent(
                            midi.REC_MainShuffle, 0, midi.REC_GetValue
                        )
                        target_swing = swing + (SWING_STEP * multiplier)
                        if 0 <= target_swing <= 128:
                            general.processRECEvent(
                                midi.REC_MainShuffle,
                                target_swing,
                                midi.REC_UpdateControl | midi.REC_Control,
                            )

                    case FourDEncoderMode.TEMPO:
                        transport.globalTransport(midi.FPT_TempoJog, 10 * multiplier)

            case CC.ENCODER_UP:
                ui.up()

            case CC.ENCODER_RIGHT:
                ui.right()

            case CC.ENCODER_DOWN:
                ui.down()

            case CC.ENCODER_LEFT:
                ui.left()

            case CC.ENCODER_VOLUME | CC.ENCODER_SWING | CC.ENCODER_TEMPO:
                self._toggle_encoder_mode(cc_num)

            # -------- TOUCH STRIP SECTION -------- #
            case CC.TOUCH_STRIP:
                match self._touch_strip_mode:
                    case TouchStripMode.TRANSPORT:
                        transport.setSongPos(cc_val / 100)
                        _midi_out_msg_control_change(CC.TOUCH_STRIP, cc_val)
                    case TouchStripMode.PITCH:
                        channels.setChannelPitch(
                            self._selected_channel,
                            _percent_to_bipolar(cc_val),
                        )
                    case TouchStripMode.MOD:
                        pass  # TODO
                    case TouchStripMode.PERFORM:
                        pass  # TODO
                    case TouchStripMode.NOTES:
                        pass  # TODO

            case (
                CC.TOUCH_STRIP_PITCH
                | CC.TOUCH_STRIP_MOD
                | CC.TOUCH_STRIP_PERFORM
                | CC.TOUCH_STRIP_NOTES
            ):
                self._toggle_touch_strip_mode(cc_num)
                self._sync_touch_strip_value(self._touch_strip_mode)

            # -------- GROUP SECTION -------- #
            case (
                CC.GROUP_A
                | CC.GROUP_B
                | CC.GROUP_C
                | CC.GROUP_D
                | CC.GROUP_E
                | CC.GROUP_F
                | CC.GROUP_G
                | CC.GROUP_H
            ):
                page_idx = cc_num - 100

                match self._pad_mode:
                    case PadMode.OMNI:
                        self._channel_page = page_idx
                    case PadMode.KEYBOARD:
                        self._scale_index = page_idx
                    case PadMode.CHORDS:
                        self._chordset_index = page_idx
                    case PadMode.STEP:
                        self._step_page = page_idx
                    case _:
                        return

                self._active_group = PadGroup(cc_num)
                self._change_group_colors()

                self._sync_channel_pads()

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
                transport.globalTransport(midi.FPT_TapTempo, 1)

            case CC.GRID:
                ui.snapOnOff()

            case CC.PLAY:
                transport.start()

            case CC.STOP:
                transport.stop()

            case CC.REC if self._shifting:  # Count-in
                transport.globalTransport(midi.FPT_CountDown, 1)
            case CC.REC:
                transport.record()

            # -------- PAD SECTION -------- #
            case CC.FIXED_VEL:
                self._is_fixed_velocity = bool(cc_val)

            case CC.PAD_MODE | CC.KEYBOARD_MODE | CC.CHORDS_MODE | CC.STEP_MODE:
                for cc in (CC.PAD_MODE, CC.KEYBOARD_MODE, CC.CHORDS_MODE, CC.STEP_MODE):
                    _midi_out_msg_control_change(cc, 127 if cc == cc_num else 0)

                active_group = PadGroup.A
                match cc_num:
                    case CC.PAD_MODE:
                        self._pad_mode = PadMode.OMNI
                        self._pad_mode_color = PadModeColor.OMNI
                        active_group += self._channel_page

                    case CC.KEYBOARD_MODE:
                        self._pad_mode = PadMode.KEYBOARD
                        self._pad_mode_color = PadModeColor.KEYBOARD
                        active_group += self._scale_index

                    case CC.CHORDS_MODE:
                        self._pad_mode = PadMode.CHORDS
                        self._pad_mode_color = PadModeColor.CHORDS
                        active_group += self._chordset_index

                    case CC.STEP_MODE:
                        self._pad_mode = PadMode.STEP
                        self._pad_mode_color = PadModeColor.STEP
                        active_group += self._step_page

                    case _:
                        pass

                self._active_group = PadGroup(active_group)
                self._change_group_colors()

                self._sync_channel_pads()

            case CC.PATTERN:
                self._is_selecting_pattern = bool(cc_val)
                self._sync_channel_pads()

            case CC.SELECT:
                self._is_selecting_channel = bool(cc_val)
                self._sync_channel_pads()

            case CC.SOLO:
                if ui.getFocused(midi.widChannelRack):
                    channels.soloChannel(self._selected_channel)
                elif ui.getFocused(midi.widMixer):
                    if self._shifting:
                        mixer.soloTrack(
                            mixer.trackNumber(), -1, midi.fxSoloModeWithSourceTracks
                        )
                    else:
                        mixer.soloTrack(
                            mixer.trackNumber(), -1, midi.fxSoloModeWithDestTracks
                        )

            case CC.MUTE:
                if ui.getFocused(midi.widChannelRack):
                    channels.muteChannel(self._selected_channel)
                elif ui.getFocused(midi.widMixer):
                    mixer.muteTrack(mixer.trackNumber())

            # ---- KNOB PAGE SECTION ---- #
            # BUTTONS
            case CC.PRESET_PREV | CC.PRESET_NEXT if cc_val:  # TODO: add mixer logic
                if not plugins.isValid(self._selected_channel):
                    return

                if cc_num == CC.PRESET_NEXT:
                    plugins.nextPreset(self._selected_channel)
                else:
                    plugins.prevPreset(self._selected_channel)

            # KNOBS
            case CC.MIX_TRACK:
                mixer.setTrackNumber(cc_val)

            case CC.MIX_VOL:
                mixer.setTrackVolume(mixer.trackNumber(), cc_val / 125)

            case CC.MIX_PAN:
                mixer.setTrackPan(mixer.trackNumber(), _percent_to_bipolar(cc_val))

            case CC.MIX_SS:
                mixer.setTrackStereoSep(
                    mixer.trackNumber(), _percent_to_bipolar(cc_val)
                )

            case CC.CHAN_SEL:
                if cc_val < channels.channelCount():
                    channels.selectOneChannel(cc_val)
                else:
                    _midi_out_msg_control_change(CC.CHAN_SEL, self._selected_channel)

            case CC.CHAN_VOL:
                channels.setChannelVolume(self._selected_channel, cc_val / 100)
            case CC.CHAN_PAN:
                channels.setChannelPan(
                    self._selected_channel, _percent_to_bipolar(cc_val)
                )

            case CC.FIX_VEL:
                self._fixed_velocity = cc_val

            # -------- SHIFT -------- #
            case CC.SHIFT:
                self._shifting = bool(cc_val)
                self._sync_channel_pads()

            # -------- DEFAULT -------- #
            case _:
                return

        msg.handled = True

    def on_note_on(self, msg: FlMidiMsg) -> None:
        note_num, note_vel = msg.note, msg.velocity
        # velocity == 0 means note off

        if note_vel:
            if self._shifting:
                self._handle_shift_note_on(note_num)

            if self._is_selecting_pattern:
                patterns.jumpToPattern(note_num + 1)
                self._sync_channel_pads()

            if self._is_selecting_channel:
                chan_idx = note_num + self._channel_page * NOTES_COUNT
                if chan_idx < channels.channelCount():
                    channels.selectOneChannel(chan_idx)

        if self._shifting or self._is_selecting_pattern or self._is_selecting_channel:
            msg.handled = True
            return

        self._handle_note_on(note_num, note_vel)

        msg.handled = True

    def _handle_shift_note_on(self, note_num: int) -> None:
        """Handles note on events when the shift button is pressed"""

        self._sync_channel_pads()

        match note_num:
            case Pad.UNDO:
                general.undoUp()
            case Pad.REDO:
                general.undoDown()
            case Pad.QUANTIZE:
                channels.quickQuantize(self._selected_channel)
            case Pad.QUANTIZE_HALF:
                channels.quickQuantize(self._selected_channel, 1)
            case Pad.SEMI_DOWN if self._semi_offset > MIN_SEMI_OFFSET:
                self._semi_offset -= 1
            case Pad.SEMI_UP if self._semi_offset < MAX_SEMI_OFFSET:
                self._semi_offset += 1
            case Pad.OCTAVE_DOWN if self._semi_offset > MIN_SEMI_OFFSET:
                self._semi_offset -= 12
            case Pad.OCTAVE_UP if self._semi_offset < MAX_SEMI_OFFSET:
                self._semi_offset += 12
            case _:
                pass

    def _handle_note_on(self, note_num: int, note_vel: int) -> None:
        match self._pad_mode:
            case PadMode.OMNI:
                real_note = ROOT_NOTE + self._get_semi_offset()
                chan_idx = note_num + self._channel_page * NOTES_COUNT
                if chan_idx >= channels.channelCount():
                    return
                if note_vel:
                    channels.midiNoteOn(
                        chan_idx,
                        real_note,
                        self._fixed_velocity if self._is_fixed_velocity else note_vel,
                    )
                else:
                    channels.midiNoteOn(chan_idx, real_note, 0)
                _midi_out_msg_note_on(
                    note_num, _get_channel_color(chan_idx, bool(note_vel))
                )

            case PadMode.KEYBOARD:
                real_note = (
                    SCALES[self._scale_index][note_num] + self._get_semi_offset()
                )
                if note_vel:
                    channels.midiNoteOn(
                        self._selected_channel,
                        real_note,
                        self._fixed_velocity if self._is_fixed_velocity else note_vel,
                    )
                    _midi_out_msg_note_on(note_num, PadModeColor.KEYBOARD)
                else:
                    channels.midiNoteOn(self._selected_channel, real_note, 0)
                    _midi_out_msg_note_on(note_num, ControllerColor.BLACK_0)

            case PadMode.CHORDS:
                chord_notes = CHORD_SETS[self._chordset_index][note_num]
                for note in chord_notes:
                    real_note = note + self._get_semi_offset()
                    if note_vel:
                        channels.midiNoteOn(
                            self._selected_channel,
                            real_note,
                            (
                                self._fixed_velocity
                                if self._is_fixed_velocity
                                else note_vel
                            ),
                        )
                        _midi_out_msg_note_on(note_num, PadModeColor.CHORDS)
                    else:
                        channels.midiNoteOn(self._selected_channel, real_note, 0)
                        _midi_out_msg_note_on(note_num, ControllerColor.BLACK_0)

            case PadMode.STEP if note_vel:
                chan_idx = note_num + self._step_page * NOTES_COUNT
                selected_channel = self._selected_channel
                channels.setGridBit(
                    selected_channel,
                    chan_idx,
                    not channels.getGridBit(selected_channel, chan_idx),
                )

            case _:
                pass

    def _init_led_states(self) -> None:
        self._deinit_led_states()

        # fmt: off
        _midi_out_msg_control_change(CC.GROUP_A, self._pad_mode_color)
        _midi_out_msg_control_change(CC.PAD_MODE, 127)
        _midi_out_msg_control_change(CC.FIX_VEL, 100)
        # fmt: on

    @staticmethod
    def _deinit_led_states() -> None:
        """De-initializes the LED states on the Maschine MK3 device"""

        for cc in range(CC_COUNT):
            _midi_out_msg_control_change(cc, ControllerColor.BLACK_0)

        for note in range(NOTES_COUNT):
            _midi_out_msg_note_on(note, ControllerColor.BLACK_0)

    def _sync_cc_led_states(self) -> None:
        """Syncs the CC LED states with the current FL Studio state"""

        # fmt: off
        _midi_out_msg_control_change(CC.CHANNEL,  _on_off(ui.getVisible(midi.widChannelRack)))
        _midi_out_msg_control_change(CC.ARRANGER, _on_off(ui.getVisible(midi.widPlaylist)))
        _midi_out_msg_control_change(CC.MIXER,    _on_off(ui.getVisible(midi.widMixer)))
        _midi_out_msg_control_change(CC.RESTART,  _on_off(bool(transport.getLoopMode())))
        _midi_out_msg_control_change(CC.BROWSER,  _on_off(ui.getVisible(midi.widBrowser)))
        _midi_out_msg_control_change(CC.TAP,      _on_off(general.getUseMetronome()))
        _midi_out_msg_control_change(CC.PLAY,     _on_off(transport.isPlaying()))
        _midi_out_msg_control_change(CC.REC,      _on_off(transport.isRecording()))
        _midi_out_msg_control_change(CC.STOP,     _on_off(not transport.isPlaying()))
        _midi_out_msg_control_change(CC.GRID,     _on_off(ui.getSnapMode() != 3))
        # fmt: on

    def _sync_selected_channel(self) -> None:
        """Syncs the selected channel index with the current FL Studio selected channel"""

        self._selected_channel = channels.selectedChannel()

    def _toggle_selected_channel_highlight(self) -> None:
        """Highlights the selected channel pad on the Maschine MK3 device"""

        _midi_out_msg_note_on(
            self._selected_channel - self._channel_page * NOTES_COUNT,
            _get_channel_color(self._selected_channel, self._is_selecting_channel),
        )

    def _sync_channel_pads(self) -> None:
        """Syncs the channel rack state with the pad LEDs on the Maschine MK3 device"""

        for note in range(NOTES_COUNT):
            _midi_out_msg_note_on(note, ControllerColor.BLACK_0)

        if self._shifting:
            for note in range(NOTES_COUNT):
                if _is_enum_value(Pad, note):
                    _midi_out_msg_note_on(note, ControllerColor.WHITE_0)
        elif self._is_selecting_pattern:
            for pattern in range(patterns.patternCount()):
                _midi_out_msg_note_on(
                    pattern,
                    (
                        ControllerColor.ORANGE_2
                        if patterns.isPatternSelected(pattern + 1)
                        else ControllerColor.ORANGE_0
                    ),
                )
        elif self._pad_mode == PadMode.OMNI or self._is_selecting_channel:
            lower_channel = self._channel_page * NOTES_COUNT
            channel_count = channels.channelCount()

            # turn on pads for available channels
            for channel in range(lower_channel, channel_count):
                idx = channel - lower_channel
                if idx == NOTES_COUNT:
                    break
                _midi_out_msg_note_on(idx, _get_channel_color(channel, False))

            self._toggle_selected_channel_highlight()
        elif self._pad_mode == PadMode.STEP:
            lower_step = self._step_page * NOTES_COUNT

            # turn on pads for step sequencer grid bits
            for gridbit in range(lower_step, lower_step + NOTES_COUNT):
                idx = gridbit - lower_step
                _midi_out_msg_note_on(
                    idx,
                    (
                        PadModeColor.STEP
                        if channels.getGridBit(self._selected_channel, gridbit)
                        else ControllerColor.BLACK_0
                    ),
                )

    def _sync_channel_controls(self) -> None:
        """Syncs the channel rack controls on the Maschine MK3 device with the current FL Studio channel rack state"""

        # fmt: off
        _midi_out_msg_control_change(CC.CHAN_SEL, self._selected_channel)
        _midi_out_msg_control_change(CC.CHAN_VOL, round(channels.getChannelVolume(self._selected_channel) * 100))
        _midi_out_msg_control_change(CC.CHAN_PAN, _bipolar_to_percent(channels.getChannelPan(self._selected_channel)))
        _midi_out_msg_control_change(CC.SOLO, _on_off(channels.isChannelSolo(self._selected_channel)))
        _midi_out_msg_control_change(CC.MUTE, _on_off(channels.isChannelMuted(self._selected_channel)))        
        # fmt: on

    @staticmethod
    def _sync_mixer_controls() -> None:
        """Syncs the mixer (encoders) values on the Maschine MK3 device with the current FL Studio mixer state"""

        track_number = mixer.trackNumber()

        # fmt: off
        _midi_out_msg_control_change(CC.MIX_TRACK, track_number)
        _midi_out_msg_control_change(CC.MIX_VOL, round(mixer.getTrackVolume(track_number) * 125))
        _midi_out_msg_control_change(CC.MIX_PAN, _bipolar_to_percent(mixer.getTrackPan(track_number)))
        _midi_out_msg_control_change(CC.MIX_SS, _bipolar_to_percent(mixer.getTrackStereoSep(track_number)))
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
                mode = TouchStripMode.TRANSPORT

        mode = mode if self._touch_strip_mode != mode else TouchStripMode.TRANSPORT

        for cc_num in (
            CC.TOUCH_STRIP_PITCH,
            CC.TOUCH_STRIP_MOD,
            CC.TOUCH_STRIP_PERFORM,
            CC.TOUCH_STRIP_NOTES,
        ):
            _midi_out_msg_control_change(
                cc_num,
                (127 if cc == cc_num and mode != TouchStripMode.TRANSPORT else 0),
            )

        self._touch_strip_mode = mode

    def _sync_touch_strip_value(self, mode: TouchStripMode) -> None:
        """Syncs the touch strip value on the Maschine MK3 device with the current FL Studio state based on the given mode"""

        match mode:
            case TouchStripMode.TRANSPORT:
                self._sync_song_position()
            case TouchStripMode.PITCH:
                _midi_out_msg_control_change(
                    CC.TOUCH_STRIP,
                    _bipolar_to_percent(
                        channels.getChannelPitch(self._selected_channel)
                    ),
                )
            case TouchStripMode.MOD:
                pass  # TODO
            case TouchStripMode.PERFORM:
                pass  # TODO
            case TouchStripMode.NOTES:
                pass  # TODO

    def _sync_song_position(self) -> None:
        """Syncs the touch strip song position value on the Maschine MK3 device"""

        _midi_out_msg_control_change(CC.TOUCH_STRIP, int(transport.getSongPos() * 100))

    def _change_group_colors(self) -> None:
        """Updates the group button colors based on the current pad mode"""

        for cc in range(CC.GROUP_A, CC.GROUP_H + 1):
            _midi_out_msg_control_change(
                cc,
                (
                    self._pad_mode_color
                    if cc == self._active_group
                    else ControllerColor.BLACK_0
                ),
            )

    def _get_semi_offset(self) -> int:
        """Returns the current semitone offset"""
        return self._semi_offset + SEMITONES_IN_OCTAVE
