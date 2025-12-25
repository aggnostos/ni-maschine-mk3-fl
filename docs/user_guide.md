# User Guide

## Controls

- `SHIFT` original **SHIFT** button is reserved by Maschine so we assign it to another CC that is not used - **NOTE REPEAT (Arp)**

### Control Buttons

- `CHANNEL` toggles **Channel Rack** visibility
  - `+SHIFT` focuses **Channel Rack**
- `ARRANGER` toggles **Playlist** visibility
  - `+SHIFT` focuses **Playlist**
- `MIXER` toggles **Mixer** visibility
  - `+SHIFT` focuses **Mixer**
- `BROWSER` toggles **Browser** visibility
  - `+SHIFT` focuses **Browser**
- `PLUG-IN` toggles **Plug-In** window visibility for selected channel
- `FILE` saves current project (behaves same way as pressing `Ctrl+S`)
- `SETTINGS` toggles **Settings** window visibility

### Edit (Encoder) Section

#### Encoder actions

- `PUSH` behaves same way as pressing `Enter` key
- `TURN` performes action depending the selected 4D Encoder mode. If **JOG** (default) mode is selected, performing **next** or **previous** actions.
- `UP` behaves same way as pressing `Up Arrow` key
- `RIGHT` behaves same way as pressing `Right Arrow` key
- `DOWN` behaves same way as pressing `Down Arrow` key
- `LEFT` behaves same way as pressing `Left Arrow` key

#### Encoder modes

- `VOLUME` sets 4D Encoder mode to **VOLUME** allowing you to adjust **Channel** or **Mixer Track** volume depending on what window is focused
- `SWING` sets 4D Encoder mode to **SWING** allowing you to adjust FL Studio's main swing located in the channel rack
- `TEMPO` sets 4D Encoder mode to **TEMPO** allowing you to adjust **Tempo**

### Performance (Touch Strip) Section

- `TOUCH STRIP` allows you to adjust specific parameter depending on what Touch Strip mode You are using. In **TRANSPORT** (default) mode Touch strip is adjusting a current song position.
- `PITCH` changes Touch Strip mode to **PITCH** allowing you to adjust Pitch of selected channel
- `MOD` changes Touch Strip mode to **MOD** (NOT IMPLEMENTED)
- `PERFORM` changes Touch Strip mode to **PERFORM** (NOT IMPLEMENTED)
- `NOTES` changes Touch Strip mode to **NOTES** (NOT IMPLEMENTED)

### Group Section

Groups have different meaning depending on what pad mode you are currently using. Toggling between one of each group (`A-H`) allows you to switch between:

- channel ranges in **PAD** mode (each group contains 16 channels)
- scales in **KEYBOARD** mode
- chord sets in **CHORDS** mode
- sets of gridbits in **STEP** mode

### Transport Section

- `RESTART` stops playback and immediately starts it again from the current song position
  - `+ SHIFT` toggles the **Loop** mode if pressed with
- `ERASE` behaves same way as pressing `Delete` key in Piano Roll
- `TAP` allows you to tap tempo
  - `+ SHIFT` turns the metronome on/off
- `FOLLOW` toggles **Snap (to grid)** mode (**Main** snap setting)
- `PLAY` starts playback from the current playhead position
- `REC` starts or stops recording
  - `+ SHIFT` toggles **Precount** mode if pressed with
- `STOP` stops playback and resets the playhead

### Pad Section

#### Pad Modes

- `FIXED VEL` toggles **Fixed Velocity** mode
- `PAD MODE` enables the **PAD (OMNI)** mode
- `KEYBOARD` enables the **KEYBOARD** mode
- `CHORDS` enables the **CHORDS** mode
- `STEP` enables the **STEP** mode

#### Other

- `PATTERN` allows you to select **Pattern** by pressing on one of the highlighted pads associated with it
- `SELECT` allows you to select **Channel** by pressing on one of the highlighted pads associated with it
- `SOLO` soloes the currently selected **Channel** or **Mixer Track**
- `MUTE` mutes the currently selected **Channel** or **Mixer Track**.
  - By default (whithout `SHIFT`) soloes mixer track, including send tracks that it is routed to, otherwise soloes mixer track, including source tracks routed to it

#### Pads

- `Undo` moves up in the undo history
- `Redo` moves down in the undo history
- `Quantize` performs a quick quantize operation on the channel
- `Quantize 50%` performs a quick quantize operation on the channel only for the start of the note
- `Semitone -` shifts notes triggered by -1 semitone
- `Semitone +` shifts notes triggered by +1 semitone
- `Octave -` shifts notes triggered by -1 octave (-12 semitones)
- `Octave +` shifts notes triggered by +1 octave (+12 semitones)

### Knob Page Section

#### Buttons

- `PRESET -` selects previous **Plug-In** preset in selected channel
- `PRESET +` selects next **Plug-In** preset in selected channel

#### Knobs

- `MIX. TRACK.` selects a mixer track and display the number of the currently selected mixer track on the screen
- `MIX. VOL.` controls the volume for selected mixer track
- `MIX. PAN.` controls the pan for selected mixer track
- `MIX. SS.` controls the stereo separation of the currently selected mixer track
- `CHAN. SEL.` selects a channel from the currently available channels
- `CHAN. VOL.` controls the volume of the currently selected channel
- `CHAN. PAN.` controls the pan for selected channel
- `FIX. VEL.` controls the velocity of notes when **FIXED VELOCITY** mode is turned on

> ## Note
>
> `PRESET+` and `PRESET-` are only compatible with FL Studio stock plugins by now. Compability with external plugins requires custom logic
