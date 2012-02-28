#========================================================
#
# Generates a Nuke .nk file from Maya (animated) objects cameras and locators 
# michael.havart@gmail.com
#
#=========================================================

import maya.cmds as cmds
import os
import time
import commands as cmd

import dmptools.mayaToNuke.ui as ui
import dmptools.mayaToNuke.utils as utils
                    
def main():
    # run the maya to nuke UI
    mayaToNukeUI = ui.MayaToNukeUI()
    mayaToNukeUI.buildUI()

if __name__ == '__main__':
    main()