# Mouse Logger
Logs mouse movements and stores it in a file.

## Description
This program tracks:
- the mouse's location once every 0.5 seconds
- mouse clicks
- if *any* mouse button was pressed
- total seconds since program began

All logs are stored in a folder called `Mouse Logs`.

## Getting Started
### Requirements
- 15 MB RAM
- 0.3 MB/s read and write speed
- 100KB of storage for every 30 minutes of testing
- 1920x1080 screen resolution

Note, this program must be run on a single-monitor setup. Data may get messed up if you are using it on a multi-monitor setup.

### Download
1. [Click here to download program](https://github.com/EthicallyPython/Mouse-Logger/raw/main/mouse_tracker.exe).
2. Disable antivirus warnings (if needed).
3. When the test begins, launch the program and click `Start Tracking`. **Please do not turn off until the test is over**.
5. When the test ends, click `Stop Tracking`
6. Close program.

## Developers
If you are concerned about security, you can always look at `mouse_tracker.py` for the original source code. This program was packaged into an exe using [Auto PY to EXE](https://github.com/brentvollebregt/auto-py-to-exe).

If you do not want to downoad `mouse_tracker.exe`:
1. Download `mouse_tracker.py`
2. Run Auto PY to EXE
3. Use Auto PY to EXE to convert `mouse_tracker.py` into an EXE file.

## Author
Kevin Duong
