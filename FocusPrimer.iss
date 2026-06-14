[Setup]
AppName=Focus Primer
AppVersion=1.0.0
DefaultDirName={autopf}\Focus Primer
DefaultGroupName=Focus Primer
UninstallDisplayIcon={app}\FocusPrimer.exe
Compression=lzma2
SolidCompression=yes
OutputDir=releases\v1.0.0
OutputBaseFilename=FocusPrimerSetup
SetupIconFile=assets\app-icon.ico
WizardSmallImageFile=assets\app-icon.ico

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"

[Files]
Source: "releases\v1.0.0\FocusPrimer.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\Focus Primer"; Filename: "{app}\FocusPrimer.exe"
Name: "{autodesktop}\Focus Primer"; Filename: "{app}\FocusPrimer.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\FocusPrimer.exe"; Description: "{cm:LaunchProgram,Focus Primer}"; Flags: nowait postinstall skipifsilent
