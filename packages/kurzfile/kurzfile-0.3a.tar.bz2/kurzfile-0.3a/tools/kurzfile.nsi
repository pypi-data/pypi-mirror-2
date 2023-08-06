#!define VERSION "0.3a"

# define installer name
Name "kurzfile"

outFile "..\dist\kurzfile-${VERSION}-setup.exe"

# set desktop as install directory
InstallDir "$PROGRAMFILES\kurzfile-${VERSION}"

Page directory
Page instfiles

# default section start
Section ""

# define output path
SetOutPath $INSTDIR

# specify file to go in output path
File ..\dist\k2list.exe

# define uninstaller name
WriteUninstaller $INSTDIR\uninstaller.exe

# default section end
SectionEnd

# create a section to define what the uninstaller does.
# the section will always be named "Uninstall"
Section "Uninstall"

# Always delete uninstaller first
Delete $INSTDIR\uninstaller.exe

# now delete installed file
Delete $INSTDIR\k2list.exe

SectionEnd
