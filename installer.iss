#define MyAppName "Asha Nurse App"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "Asha Nurse"
#define MyAppExeName "AshaNurseApp.exe"

[Setup]
AppId={{A7B4E8D2-6F1C-4B92-91C5-ASHANURSE2026}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}

SetupIconFile=AshaNurseApp.ico

DefaultDirName={localappdata}\Programs\AshaNurseApp
DefaultGroupName={#MyAppName}

OutputDir=installer
OutputBaseFilename=AshaNurseApp_Setup

Compression=lzma
SolidCompression=yes

PrivilegesRequired=lowest
Uninstallable=yes

[Files]
Source: "dist\AshaNurseApp\*"; DestDir: "{app}"; Flags: recursesubdirs createallsubdirs ignoreversion

[Icons]
Name: "{autodesktop}\Asha Nurse App"; Filename: "{app}\AshaNurseApp.exe"
Name: "{group}\Asha Nurse App"; Filename: "{app}\AshaNurseApp.exe"

[Run]
Filename: "{app}\AshaNurseApp.exe"; Description: "Launch Asha Nurse App"; Flags: nowait postinstall skipifsilent