; Inno Setup Script for IMS Import Management System
; Compiles dist/IMS.exe into a professional Windows Installer Setup wizard

[Setup]
AppName=IMS Import Management System
AppVersion=1.1.0
AppPublisher=Baraa Solutions
AppPublisherURL=https://shipping.baraa-solutions.com
DefaultDirName={autopf}\IMS_ImportSystem
DefaultGroupName=IMS Import Management System
OutputDir=installer_output
OutputBaseFilename=Setup_IMS_v1.1.0
Compression=lzma2/max
SolidCompression=yes
SetupIconFile=src\assets\app_icon.ico
UninstallDisplayIcon={app}\IMS.exe
WizardStyle=modern

[Languages]
Name: "arabic"; MessagesFile: "compiler:Languages\Arabic.isl"
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: checked

[Files]
Source: "dist\IMS.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\IMS Import Management System"; Filename: "{app}\IMS.exe"
Name: "{group}\{cm:UninstallProgram,IMS Import System}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\IMS Import Management System"; Filename: "{app}\IMS.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\IMS.exe"; Description: "{cm:LaunchProgram,IMS Import System}"; Flags: nowait postinstall skipifsilent
