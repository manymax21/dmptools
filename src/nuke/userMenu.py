import nuke
import os
import random
import dmptools.tf2classes as tf2

NUKE_SHARE = '!NUKE_SHARE!'
TF2CLASSES = tf2.CLASSES
    
# randomly get toolbar icon
iconPrefix = TF2CLASSES.keys()[random.randint(0,len(TF2CLASSES)-1)]
iconTooltip = TF2CLASSES[iconPrefix][random.randint(0,len(TF2CLASSES[iconPrefix])-1)]
iconPath = NUKE_SHARE+'/tf2avatars/'+iconPrefix+'.jpg'

print iconTooltip

m = nuke.toolbar("Nodes").addMenu('dmptools/Misc', tooltip = iconTooltip, icon = iconPath)

# 3D
m.addCommand('3d/Shadow Generator', 'nuke.createNode("shadow_generator")')

# 2D
m.addCommand('2d/Nuke Image Converter...', 'execfile("/usr/people/michael-ha/python/env/nukeImageConverter.py");makeProxyUI()')
m.addCommand('2d/Buf Clone', 'import dmptools.macros.nukeCommands as nukeCommands;nukeCommands.bclone()')
m.addCommand('2d/Connect Selection ', 'import dmptools.macros.nukeCommands as nukeCommands;nukeCommands.connectSel()', "CTRL+Shift+Y")
m.addCommand('2d/Clear Animation', 'import dmptools.macros.nukeCommands as nukeCommands;nukeCommands.clearAnim()')
m.addCommand('2d/Show-Hide inputs', 'import dmptools.macros.nukeCommands as nukeCommands;nukeCommands.hideInputs()',"Alt+T")
m.addCommand('2d/Set Selected or All Read Frame Range...', 'import dmptools.macros.nukeCommands as nukeCommands;nukeCommands.setReadFrameRange()')
m.addCommand('2d/Set frame range from selection', 'import dmptools.macros.nukeCommands as nukeCommands;nukeCommands.setFrameRangeFromSel()', "Ctrl+Shift+R")
m.addCommand('2d/Rename label according the dependance node', 'import dmptools.macros.nukeCommands as nukeCommands;nukeCommands.renameLabel()', "Ctrl+Alt+Shift+R")
m.addCommand('2d/Switch crop format', 'import dmptools.macros.nukeCommands as nukeCommands;nukeCommands.switchCrop()', "Ctrl+Alt+Shift+O")
m.addCommand('2d/Switch 0 - 1', 'import dmptools.macros.nukeCommands as nukeCommands;nukeCommands.switchUV_PROJ()', "Ctrl+Alt+Shift+S")
m.addCommand('2d/Create read from write', 'import dmptools.macros.nukeCommands as nukeCommands;nukeCommands.createReadFromWrite()', "Ctrl+Alt+Shift+R")
m.addCommand('2d/Toggle postage stamp on read nodes', 'import dmptools.macros.nukeCommands as nukeCommands;nukeCommands.togglePostageStamps()', "Ctrl+Alt+P")
m.addCommand('2d/Bezier', 'import dmptools.macros.nukeCommands as nukeCommands;nukeCommands.switchNode()', "Ctrl+Alt+Shift+S")
m.addCommand('2d/Switch node', 'nuke.tcl("Bezier")', "Shift+B")

# other
m.addCommand('Other/Centralize script...', 'execfile("/usr/people/michael-ha/python/centralizeNukeScript.py");makeLocalUI()')
m.addCommand('Other/Archive script...', 'execfile("/usr/people/michael-ha/python/archive_v1.0.py");ai.interface()')
m.addCommand('Other/Copy special', 'import dmptools.macros.nukeCommands as nukeCommands;nukeCommands.copySpecial()', "CTRL+SHIFT+C")
m.addCommand('Other/list knobs', 'import dmptools.macros.nukeCommands as nukeCommands;nukeCommands.listKnobs()',"Ctrl+Alt+Shift+I")
m.addCommand('Other/Play', 'import dmptools.macros.nukeCommands as nukeCommands;nukeCommands.nukePlay()', "Alt+V")
m.addCommand('Other/Goto first frame', 'import dmptools.macros.nukeCommands as nukeCommands;nukeCommands.goToFirstFrame()', "Alt+Shift+V")
m.addCommand('Other/Replace string in file knob...', 'import dmptools.macros.nukeCommands as nukeCommands;nukeCommands.replaceStringInFile()')
m.addCommand('Other/Set selected Write the only active write', 'import dmptools.macros.nukeCommands as nukeCommands;nukeCommands.setSelWriteActive()')
m.addCommand('Other/How many nodes', 'nuke.message(str(len(nuke.allNodes()))+" nodes in comp.")', "Ctrl+Shift+Alt+A")
m.addCommand('Other/Expression arrows', '_internal_expression_arrow_cmd()', "Alt+Shift+E")
m.addCommand('Other/Unselect All', 'import dmptools.macros.nukeCommands as nukeCommands ; nukeCommands.unselectAll();nukeCommands.closeAllControlPanel()', "Ctrl+Space")

#root
m.addCommand('Execute', 'import dmptools.macros.nukeCommands as nukeCommands;nukeCommands.nukeExecute()', "Alt+E")
m.addCommand('Import exported file', 'import dmptools.macros.nukeCommands as nukeCommands;nukeCommands.importScript()', "Ctrl+Shift+I")
m.addCommand('Open terminal from selection', 'import dmptools.macros.nukeCommands as nukeCommands;nukeCommands.openTerminal()', "Alt+X")
m.addCommand('Start server', 'execfile("/usr/people/michael-ha/python/nukeserver.py");threaded_server()')
m.addCommand('Set Shot FrameRange', 'import dmptools.macros.nukeCommands as nukeCommands;nukeCommands.setShotFrameRange()')
m.addCommand('Show modules...', 'import dmptools.macros.nukeCommands as nukeCommands;nukeCommands.showModules()')
