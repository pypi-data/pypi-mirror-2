[Setup]
AppName=Aard Dictionary
AppVerName=Aard Dictionary 0.9.1
DefaultDirName={pf}\Aard Dictionary
DefaultGroupName=Aard Dictionary
Compression=lzma
SolidCompression=yes
OutputDir=..\winsetup
LicenseFile=..\LICENSE
ShowLanguageDialog=auto

[Languages]
Name: "en"; MessagesFile: "compiler:Default.isl"
Name: "ru"; MessagesFile: "compiler:Languages\Russian.isl"

[Files]
Source: "..\dist\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "..\windows\aarddict.org.url"; DestDir: "{app}"
Source: "..\windows\aardtalk.url"; DestDir: "{app}"

[Icons]
Name: "{group}\Aard Dictionary"; Filename: "{app}\run.exe"
Name: "{group}\Aard Site"; Filename: "{app}\aarddict.org.url"
Name: "{group}\Aard Talk"; Filename: "{app}\aardtalk.url"
Name: "{group}\Uninstall Aard Dictionary"; Filename: "{uninstallexe}"

