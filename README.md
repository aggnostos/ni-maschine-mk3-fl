# NI Maschine MK3 FL Studio MIDI Script

A custom MIDI script that integrates **NI Maschine MK3** with **FL Studio**, providing deep control over channels, mixer, transport, pads, encoder, and touch strip.

This script is designed for users who want a **Maschine-style workflow inside FL Studio**, without running the Maschine software.

## Motivation

When I started looking for Maschine MK3 MIDI scripts for FL Studio, most existing solutions were difficult to read, poorly structured, and hard to extend. Many lacked clear architecture, consistent style, or meaningful documentation.

This project was created to address those issues.

In addition to clean code and solid architecture, special care was taken to map buttons and controls in a way that feels as native as possible to FL Studio, avoiding unnatural or forced behavior.

The goal is to provide a clean, performant, and well-structured MIDI script that works out of the box, while also serving as a solid foundation for anyone who wants to learn or build upon FL Studio MIDI scripting.

## Requirements

Before installing the script, make sure you have the following:
- **FL Studio 24.0.0 or newer**
- **NI Controller Editor**
- **NI Maschine MK3 MIDI controller**

> ⚠️ This script is **not compatible** with Maschine Mikro or Maschine+.

## Installation

### 1. Download the latest release
1. Go to the **Releases** page of this repository.
2. Download the latest release archive named `ni-maschine-mk3-fl-<version>.zip`.
3. Extract the files to a temporary location.

### 2. Load the Maschine MK3 configuration in NI Controller Editor
1. Open **NI Controller Editor**.
2. Connect your **Maschine MK3**.
3. In the menu, select: **"File" → "Open Configuration..."**
4. Open the file `FL Studio.ncc`
5. After loading, select the configuration named **"FL Studio"**
6. Make sure this configuration is **active** on the controller.

### 3. Install the MIDI script in FL Studio
1. Locate the FL Studio MIDI scripts directory:
	- **macOS**: `~/Documents/Image-Line/FL Studio/Settings/Hardware/`
    - **Windows**: `Documents/Image-Line\FL Studio\Settings\Hardware\`
2. Create a **new folder** with any name, for example: `NI_Maschine_MK3`    
3. Copy the file `device_Maschine_MK3.py` into the newly created folder.

The final folder structure should look like this:
```
...
└── Hardware/
	└── NI_Maschine_MK3/
	    └── device_Maschine_MK3.py
```

### 4. Enable the script in FL Studio
1. Open **FL Studio**.
2. Go to: **"Options" → "MIDI Settings"**
3. In the **Input** list, find: "Maschine MK3..."
4. Select it, then:
    - Set **Controller type** to: "NI Maschine MK3"
    - Enable the **Enable** checkbox.
5. Close the MIDI Settings window.

### 5. If nothing happens
If the controller does not respond immediately:
1. Hold **SHIFT** on the Maschine MK3.
2. Press **CHANNEL (MIDI)** on the controller.

## Next steps
- See [User Guide](docs/user_guide.md) for a full control layout and workflow explanation.
- See [Developer Guide](docs/developer_guide.md) if you want to modify or extend the script.