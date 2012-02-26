#======================================
#
# michael.havart@gmail.com
# create dmptools shelf
#
#======================================

import maya.cmds as cmds
import maya.mel as mel
import os

# globals
CONFIGPATH = '!MAYA_SHELF!'
VERSION = '!VERSION!'
ICONSPATH = '!MAYA_SHELF!'
BUTTONS = [
            {
                'name' : 'SublimeText',
                'command' : 'import dmptools.mayaCommands as mayaCommands;mayaCommands.launchSublimeText()',
                'icon' : ICONSPATH+'/SublimeText.xpm',
                'annotation' : 'Launch the Sublime Text editor.'
            },
            {
                'name' : 'Nuke',
                'command' : 'import dmptools.mayaCommands as mayaCommands;mayaCommands.launchNuke()',
                'icon' : ICONSPATH+'/Nuke.xpm',
                'annotation' : 'Launch Nuke.'
            },
            {
                'name' : 'mayaToNuke',
                'command' : 'import dmptools.mayaToNuke as mayaToNuke;mayaToNuke.mayaToNuke()',
                'icon' : ICONSPATH+'/MayaToNuke.xpm',
                'annotation' : 'Maya to Nuke Exporter.'
            },
            {
                'name' : 'ratioCalculator',
                'command' : 'import dmptools.ratioCalculator as ratioCalculator;ratioCalculator.main()',
                'icon' : ICONSPATH+'/RatioCalculator.xpm',
                'annotation' : 'Camera-Image ratio calculator.'
            },
          ]

def createShelf():
    # delete the shelf is already exists
    if cmds.shelfLayout('dmptools', ex=True):
        fullname = cmds.shelfLayout('dmptools', fpn=True, q=True)
        cmds.deleteUI(fullname)
    # create the shelf
    shelfParent = cmds.shelfTabLayout('ShelfLayout', fpn=True, q=True)
    cmds.shelfLayout('dmptools', p=shelfParent)
    # create shelf buttons
    for button in BUTTONS:
        b = addButton(button)

def addButton(button):
    # create dmptools shelf button
    b = cmds.shelfButton(button['name'],
                    enableCommandRepeat=True,
                    enable=True,
                    width=34,
                    height=34,
                    manage=True,
                    visible=True,
                    image1=button['icon'],
                    label=button['name'],
                    style='iconOnly',
                    annotation=button['annotation'],
                    command=button['command'],
                    sourceType='python',
                    )
    return cmds.shelfButton(b, fpn=True, q=True)

def main():
    createShelf()

if __name__ == '__main__':
    main()