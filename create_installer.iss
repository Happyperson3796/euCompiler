[Setup]
AppName=EuCompiler
AppVersion=1.0
DefaultDirName={autopf}\EuCompiler
OutputBaseFilename=EuCompiler-setup
PrivilegesRequired=admin

[Files]
Source: "EuCompiler.dist\*"; DestDir: "{app}"; Flags: recursesubdirs createallsubdirs

[Icons]
Name: "{group}\Eu5 Compiler"; Filename: "{app}\EuCompiler.exe"

[Registry]
Root: HKCR; Subkey: ".euc"; ValueType: string; ValueName: ""; ValueData: "EuCompiler.File"; Flags: uninsdeletekey

Root: HKCR; Subkey: "EuCompiler.File"; ValueType: string; ValueName: ""; ValueData: "Hearts of Iron Compiler File"; Flags: uninsdeletekey

Root: HKCR; Subkey: "EuCompiler.File\shell\open\command"; ValueType: string; ValueName: ""; ValueData: """{app}\EuCompiler.exe"" ""%1"""

Root: HKCR; Subkey: "EuCompiler.File\DefaultIcon"; ValueType: string; ValueName: ""; ValueData: "{app}\EuCompiler.exe,0"