# Developer guide

## Motivation & Design Goals

As was said this project was created in response to the state of existing Maschine MK3 MIDI scripts for FL Studio, which often suffer from:

- tightly coupled logic
- unclear control flow
- lack of separation between input handling, state, and UI sync
- minimal or nonexistent documentation
- code that is difficult to modify without breaking behavior

Rather than patching an existing solutions, this script was implemented from scratch with a focus on architecture, maintainability, and performance.

In addition, significant effort was made to ensure that all buttons, encoders, and controls are mapped in a way that feels native to FL Studio’s workflow. Wherever possible, controls mirror FL Studio’s own shortcuts and interaction patterns instead of introducing arbitrary or controller-centric abstractions.

Key design goals:

- explicit state management instead of implicit behavior
- clear separation of responsibilities
- predictable event handling for FL Studio callbacks
- readable, self-documenting code that's easy to understand

The project is intentionally structured as a reference-quality implementation rather than a black box, making it suitable both for daily use and as a learning base for developers interested in FL Studio MIDI scripting.

## Project structure

`src/`:

- `main.py` contains integration layer between FL Studio and the controller logic
- `consts.py` contains global constants used across the script. This file centralizes constants so they are easy to update.
- `controller.py` the central controller class where all MIDI events are handled
- `controls.py` defines CC mappings for the device
- `enums.py` contains enumerations used globally
- `notes.py` defines MIDI note constants
- `utilities.py` helper functions used by the script

`scripts/`:

- `build.py` is an utility script used for building all the source files into one inside the `dist/` folder (used for building a release version)

`dist/`:

- `device_Maschine_MK3.py` file produced by `build.py` script

`controller_editor/`:

- `FL_Studio.ncc` configuration file for **Controller Editor**
