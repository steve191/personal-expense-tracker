# Building Personal Expense Tracker as an Executable

This guide explains how to compile the Personal Expense Tracker into a standalone Windows executable (.exe) that can run without Python installed.

## Prerequisites

You'll need to do this on a Windows machine (or use a Windows VM) since you're creating a Windows .exe file.

### 1. Install Python
Download and install Python 3.10 or higher from [python.org](https://www.python.org/downloads/)

### 2. Install Required Packages
Open Command Prompt and run:
```bash
pip install ttkbootstrap python-dateutil pandas ofxtools pyinstaller
```

## Building the Executable

### Option 1: Simple Build (Recommended)

Run this command in the project directory:

```bash
pyinstaller --clean --noconsole --onefile --collect-data ttkbootstrap --name "ExpenseTracker" --icon Dollar.ico main.py
```

**What the flags mean:**
- `--clean` - Clean cache before building
- `--noconsole` - Hide the command prompt window (for GUI apps)
- `--onefile` - Create a single .exe file
- `--collect-data ttkbootstrap` - Include ttkbootstrap theme files
- `--name "ExpenseTracker"` - Name of the output file
- `--icon Dollar.ico` - Use the Dollar icon for the app

### Option 2: If You Get Tcl/Tk Errors

If the app crashes with Tcl/Tk errors, you need to include the Tcl/Tk files explicitly. Find your Python installation folder and run:

```bash
pyinstaller --clean --noconsole --onefile ^
    --collect-data ttkbootstrap ^
    --add-data "C:\Python311\tcl\tcl8.6;.\tcl" ^
    --add-data "C:\Python311\tcl\tk8.6;.\tk" ^
    --name "ExpenseTracker" ^
    --icon Dollar.ico ^
    main.py
```

Replace `C:\Python311` with your actual Python installation path.

## Finding Your Executable

After building, you'll find:
- The executable at: `dist/ExpenseTracker.exe`
- Build files at: `build/` (can be deleted)
- Spec file at: `ExpenseTracker.spec` (for future builds)

## Distributing the App

1. Copy `dist/ExpenseTracker.exe` to wherever you want
2. The database file (`database.db`) will be created automatically in the same folder as the .exe when the app runs
3. Users just double-click the .exe to run it - no installation needed

## Troubleshooting

### App won't start
Run from command prompt to see error messages:
```bash
dist\ExpenseTracker.exe
```

### Missing modules error
Add hidden imports to the command:
```bash
pyinstaller --clean --noconsole --onefile ^
    --collect-data ttkbootstrap ^
    --hidden-import=PIL ^
    --hidden-import=pandas ^
    --name "ExpenseTracker" ^
    main.py
```

### Antivirus flags the exe
This is common with PyInstaller. Add an exception in your antivirus or sign the executable with a code signing certificate.

## Build in a Virtual Environment (Best Practice)

```bash
python -m venv build_env
build_env\Scripts\activate
pip install ttkbootstrap python-dateutil pandas ofxtools pyinstaller pillow
pyinstaller --clean --noconsole --onefile --collect-data ttkbootstrap --name "ExpenseTracker" --icon Dollar.ico main.py
```

This ensures only necessary packages are included in the build.
