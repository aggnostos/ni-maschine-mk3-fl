# Developer guide

## Design Goals

- explicit state management instead of implicit behavior
- clear separation of responsibilities
- readable, self-documenting code that's easy to understand

The project is intentionally structured as a reference-quality implementation rather than a black box, making it suitable both for daily use and as a learning base for developers interested in FL Studio MIDI scripting.

## Requirements

- **python** >=3.11
- **poetry** >=2.1.3

## Setup

```sh
 poetry install
```

## Build

- MacOS:

 ```sh
 ./build
 ```

- Win:

 ```powershell
 ./build.cmd
 ```

## Format

```sh
 poetry run black ./
```

## Project structure

`src/`:

- `main.py` contains integration layer between FL Studio and the controller logic
- `consts.py` contains global constants used across the script. This file centralizes constants so they are easy to update.
- `controller.py` the central controller class where all MIDI events are handled
- `controls.py` defines CC mappings for the device
- `enums.py` contains enumerations used globally
- `notes.py` defines MIDI note constants
- `utilities.py` helper functions used by the script

`dist/`:

- `device_Maschine_MK3.py` file produced by `build` script

`controller_editor/`:

- `FL_Studio.ncm3` template file for **Controller Editor**

`scripts/`:

- `build` is an utility script used for building all the source files into one inside the `dist/` folder (used for building a release version)
