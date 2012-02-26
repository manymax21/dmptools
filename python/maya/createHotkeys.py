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

# hotkeys files path
CMD_FILE = '!MAYA_GLOBAL!/prefs/userRunTimeCommands.mel'
HOTKEY_FILE = '!MAYA_GLOBAL!/prefs/userHotkeys.mel'
COMMAND_NAME_FILE = '!MAYA_GLOBAL!/prefs/userNamedCommands.mel'

# hotkeys list
HOTKEYS = [
        {
            'name':'bufMove',
            'key':'q',
            'alt':False,
            'ctl':False,
            'release':True,
            'command':'python("import dmptools.mayaCommands as mayaCommands;\
                reload(mayaCommands);mayaCommands.bufMove()");',
            'releaseCommand':'python("import dmptools.mayaCommands as mayaCommands;\
                reload(mayaCommands);mayaCommands.bufMoveRelease()");'
        },
        {
            'name':'hideSelectionSwitch',
            'key':'h',
            'alt':False,
            'ctl':False,
            'release':False,
            'command':'python("import dmptools.mayaCommands as mayaCommands;\
                reload(mayaCommands);mayaCommands.hideSelSwitch()");'
        },
        {
            'name':'isolateSelection',
            'key':'H',
            'alt':True,
            'ctl':False,
            'release':True,
            'command':'python("import dmptools.mayaCommands as mayaCommands;\
                reload(mayaCommands);mayaCommands.isolateSelection()");',
            'releaseCommand':'python("import dmptools.mayaCommands as mayaCommands;\
                reload(mayaCommands);mayaCommands.isolateSelectionRelease()");'
        },
        {
            'name':'toggleNormals',
            'key':'n',
            'alt':True,
            'ctl':False,
            'release':False,
            'command':'python("import dmptools.mayaCommands as mayaCommands;\
                reload(mayaCommands);mayaCommands.toggleNormals()");',
        },
        {
            'name':'setWireframe',
            'key':'w',
            'alt':True,
            'ctl':False,
            'release':False,
            'command':'python("import dmptools.mayaCommands as mayaCommands;\
                reload(mayaCommands);mayaCommands.setWireframe()");',
        },
        {
            'name':'setBackfaceCulling',
            'key':'B',
            'alt':True,
            'ctl':False,
            'release':False,
            'command':'python("import dmptools.mayaCommands as mayaCommands;\
                reload(mayaCommands);mayaCommands.setBackfaceCulling()");',},
        {
            'name':'setDefaultMaterial',
            'key':'d',
            'alt':True,
            'ctl':False,
            'release':False,
            'command':'python("import dmptools.mayaCommands as mayaCommands;\
                reload(mayaCommands);mayaCommands.setDefaultMaterial()");',
        },
        {
            'name':'cameraPanTool',
            'key':'z',
            'alt':True,
            'ctl':False,
            'release':False,
            'command':'python("import dmptools.mayaCommands as mayaCommands;\
                reload(mayaCommands);mayaCommands.cameraPanTool()");',
        },
        {
            'name':'cameraZoomTool',
            'key':'Z',
            'alt':True,
            'ctl':False,
            'release':False,
            'command':'python("import dmptools.mayaCommands as mayaCommands;\
                reload(mayaCommands);mayaCommands.cameraZoomTool()");',
        },
        {
            'name':'resetPanZoom',
            'key':'Z',
            'alt':True,
            'ctl':True,
            'release':False,
            'command':'python("import dmptools.mayaCommands as mayaCommands;\
                reload(mayaCommands);mayaCommands.resetPanZoom()");',
        },
        {
            'name':'selectNgones',
            'key':'q',
            'alt':True,
            'ctl':False,
            'release':False,
            'command':'python("import dmptools.mayaCommands as mayaCommands;\
                reload(mayaCommands);mayaCommands.switchSelectNgones()");',
        },
        {
            'name':'selectTriangles',
            'key':'p',
            'alt':True,
            'ctl':False,
            'release':False,
            'command':'python("import dmptools.mayaCommands as mayaCommands;\
                reload(mayaCommands);mayaCommands.switchSelectTriangles()");',
        },
        {
            'name':'switchLight',
            'key':'l',
            'alt':True,
            'ctl':False,
            'release':False,
            'command':'python("import dmptools.mayaCommands as mayaCommands;\
                reload(mayaCommands);mayaCommands.switchLight()");'
        },
        {
            'name':'switchHighlightedSelection',
            'key':'f',
            'alt':True,
            'ctl':False,'release':False,
            'command':'python("import dmptools.mayaCommands as mayaCommands;\
                reload(mayaCommands);mayaCommands.switchHighlightedSelection()");'
        },
        {
            'name':'askFlushUndo',
            'key':'f',
            'alt':False,
            'ctl':True,
            'release':False,
            'command':'python("import dmptools.mayaCommands as mayaCommands;\
                reload(mayaCommands);mayaCommands.askFlushUndo()");'
        },
        {
            'name':'saveAs',
            'key':'S',
            'alt':False,
            'ctl':True,
            'release':False,
            'command':'SaveSceneAs;'
        },
        {
            'name':'freezeHistory',
            'key':'F',
            'alt':True,
            'ctl':False,
            'release':False,
            'command':'delete -ch;makeIdentity -apply true -t 1 -r 1 -s 1 -n 0;'
        },
        {
            'name':'freezeHistoryCenterPivot',
            'key':'F',
            'alt':True,
            'ctl':True,
            'release':False,
            'command':'delete -ch;xform -cp;makeIdentity -apply true -t 1 -r 1 -s 1 -n 0;'
        },
        {
            'name':'setDefaultRenderer',
            'key':'1',
            'alt':True,
            'ctl':False,
            'release':False,
            'command':'python("import dmptools.mayaCommands as mayaCommands;\
                reload(mayaCommands);mayaCommands.setDefaultRenderer()");'
        },
        {
            'name':'setHardwareRenderer',
            'key':'2',
            'alt':True,
            'ctl':False,
            'release':False,
            'command':'python("import dmptools.mayaCommands as mayaCommands;\
                reload(mayaCommands);mayaCommands.setHardwareRenderer()");'
        },
        {
            'name':'setViewport2Renderer',
            'key':'3',
            'alt':True,
            'ctl':False,
            'release':False,
            'command':'python("import dmptools.mayaCommands as mayaCommands;\
                reload(mayaCommands);mayaCommands.setViewport2Renderer()");'
        },
    ]
   
def setHotkey(hotkey):
    
    # get hotkey dict data
    name = hotkey['name']
    key = hotkey['key']
    alt = hotkey['alt']
    ctl = hotkey['ctl']
    release = hotkey['release']
    command = hotkey['command']
    if release:
        releaseName = name+"Release"
        releaseCommand = hotkey['releaseCommand']
    
    #create hotkey command
    cmds.nameCommand(name, sourceType = "mel", annotation = name, command = command)
    if release:
        cmds.nameCommand(releaseName, sourceType = "mel", annotation = releaseName, command = releaseCommand)
    
    # set hotkey
    cmds.hotkey(k = key, alt=alt, ctl = ctl, name = name)    
    print 'set hotkey:', name, key, alt, ctl, command

    if release:
        cmds.hotkey(k = key, alt=alt, ctl = ctl, releaseName = releaseName)
        print 'set hotkey release:', releaseName, key, alt, ctl, releaseCommand

def main():
    """
        delete the old maya hotkey files
        and install the new ones from the HOTKEYS list
    """
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

if __name__ == '__main__':
    main()
