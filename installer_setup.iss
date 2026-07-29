; Inno Setup Script for Enterprise Import Management System
; Compiles dist/ImportManagementSystem into a professional Windows Installer Setup wizard

[Setup]
AppName=Enterprise Import Management System
AppVersion=1.0.0
AppPublisher=Egyptian Import ERP Co.
AppPublisherURL=https://your-domain.com
DefaultDirName={autopf}\ImportManagementSystem
DefaultGroupName=Enterprise Import Management System
OutputDir=installer_output
OutputBaseFilename=Setup_ImportManagementSystem_v1.0.0
Compression=lzma2/max
SolidCompression=yes
SetupIconFile=src\assets\app_icon.ico
UninstallDisplayIcon={app}\ImportManagementSystem.exe
WizardStyle=modern

[Languages]
Name: "arabic"; MessagesFile: "compiler:Languages\Arabic.isl"
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "dist\ImportManagementSystem\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\Enterprise Import System"; Filename: "{app}\ImportManagementSystem.exe"; IconFilename: "{app}\src\assets\app_icon.ico"
Name: "{group}\{cm:UninstallProgram,Enterprise Import System}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\Enterprise Import System"; Filename: "{app}\ImportManagementSystem.exe"; IconFilename: "{app}\src\assets\app_icon.ico"; Tasks: desktopicon

[Run]
Filename: "{app}\ImportManagementSystem.exe"; Description: "{cm:LaunchProgram,Enterprise Import System}"; Flags: nowait postinstall skipifsilent
