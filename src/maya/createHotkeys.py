#==========================================================================
#
# createHotkeys.py
# michael.havart@gmail.com
#
# create Maya hotkeys instead of typing them in the maya hotkey menu.
#
#==========================================================================

import maya.cmds as cmds
import os

import dmptools.hotkeys as hotkeys

# hotkeys files path
CMD_FILE = '!MAYA_GLOBAL!/prefs/userRunTimeCommands.mel'
HOTKEY_FILE = '!MAYA_GLOBAL!/prefs/userHotkeys.mel'
COMMAND_NAME_FILE = '!MAYA_GLOBAL!/prefs/userNamedCommands.mel'
HOTKEYS = hotkeys.HOTKEYS

def setHotkey(hotkey):
    
    # get hotkey dict data
    name = hotkey['name']
    key = hotkey['key']
    alt = hotkey['alt']
    ctl = hotkey['ctrl']
    release = hotkey['release']
    command = hotkey['command']
    if release:
        releaseName = name+"Release"
        releaseCommand = hotkey['releaseCommand']
    
    #create hotkey command
    cmds.nameCommand(name, sourceType="mel", annotation=name, command=command)
    if release:
        cmds.nameCommand(releaseName, sourceType="mel", annotation=releaseName, command=releaseCommand)
    
    # set hotkey
    cmds.hotkey(k=key, alt=alt, ctl=ctl, name=name)    
    #print 'set hotkey:', name, key, alt, ctrl, command

    if release:
        cmds.hotkey(k=key, alt=alt, ctl=ctl, releaseName=releaseName)
        #print 'set hotkey release:', releaseName, key, alt, ctrl, releaseCommand

def showHotkeysList():
    """shows the current user hotkeys mapping and its name"""
    reload(hotkeys)
    lines = []
    for key in hotkeys.HOTKEYS:
        lines.append('key:  '+str(key['key'])+'  ctrl:  '+str(key['ctrl'])+'  alt:  '+str(key['alt'])+'  '+str(key['name']))

    window = cmds.window('hotkeysWindow')
    cmds.paneLayout()
    cmds.textScrollList(numberOfRows=8,
                        allowMultiSelection=True,
                        append=lines,)
    cmds.showWindow()

def main():
    """
        delete the old maya hotkey files
        and install the new ones from the HOTKEYS list
    """
    print 'creating hotkeys...'
    # delete old hotkeys
    if os.path.exists(CMD_FILE):
        os.remove(CMD_FILE)
    if os.path.exists(HOTKEY_FILE):
        os.remove(HOTKEY_FILE)
    if os.path.exists(COMMAND_NAME_FILE):
        os.remove(COMMAND_NAME_FILE)
    # create hotkeys
    for hotKey in HOTKEYS:
            setHotkey(hotKey)
    print '> done.'

if __name__ == '__main__':
    main()
