#========================================================
#
# Generates a Nuke .nk file from Maya (animated) objects cameras and locators 
# michael.havart@gmail.com
#
#=========================================================

import dmptools.mayaToNuke.ui as ui
                    
def main():
    # run the maya to nuke UI
    mayaToNukeUI = ui.MayaToNukeUI()
    mayaToNukeUI.buildUI()

if __name__ == '__main__':
    main()