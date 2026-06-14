# Installation Guide

You can run **Focus Primer** on Windows using either the packaged release options or by running directly from the source repository.

## Option 1: Standalone Portable Executable
1. Download `FocusPrimer.exe` from the latest release page.
2. Double click `FocusPrimer.exe` to run.

## Option 2: Setup Installer (Recommended)
1. Download `FocusPrimerSetup.exe` from the latest release page.
2. Run the setup installer and proceed with the wizard.
3. This creates Start Menu and Desktop shortcuts for quick launching.

## Developer Source Build Instructions
Ensure you have Python 3.10+ installed.

1. Clone repository:
   ```bash
   git clone https://github.com/[your-username]/focus-primer.git
   cd focus-primer
   ```
2. Install PyWebview dependencies:
   ```bash
   pip install pywebview pyinstaller
   ```
3. Run the application:
   ```bash
   python src/main.py
   ```
4. Package the application locally:
   ```bash
   pyinstaller --onefile --windowed --add-data "src/index.html;." --icon "assets/app-icon.ico" --name "FocusPrimer" src/main.py
   ```
