#======================================
#
# michael.havart@gmail.com
# create dmptools shelf
#
#======================================

import maya.cmds as cmds
import maya.mel as mel
import os

import dmptools.shelfButtons as shelfButtons

# globals
CONFIGPATH = '!MAYA_SHELF!'
VERSION = '!VERSION!'
ICONSPATH = '!MAYA_SHELF!'
BUTTONS = shelfButtons.BUTTONS

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
    # select the last created shelf 
    i = cmds.shelfTabLayout(shelfParent, numberOfChildren=True, q=True)
    cmds.shelfTabLayout(shelfParent, selectTabIndex=i, e=True)

def addButton(button):
    # create dmptools shelf button
    b = cmds.shelfButton(button['name'],
                    enableCommandRepeat=True,
                    enable=True,
                    width=34,
                    height=34,
                    manage=True,
                    visible=True,
                    image1=ICONSPATH+'/'+button['icon'],
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