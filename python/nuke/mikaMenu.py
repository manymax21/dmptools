import nuke
import os
import random
import dmptools

NUKE_SHARE = '!NUKE_SHARE!'
TF2CLASSES = {
    'red_scout':'Eat my dust!',
    'red_pyro':'OUUUMMMPHHHH MMMPPFFHHH MPFHH!',
    'red_medic':'Did the Frauleins have their Mittelschmerz?',
    'red_heavy':'Entire team is babies!',
    'red_sniper':'Thanks for standin\' still, wanker!',
    'red_demoman':'KA-BOOOOOOOM!',
    'red_engineer':'Spy sappin\' my sentry!',
    'red_spy':'Gentlemen.',
    'red_soldier':'Maggots!',
    }
    
# randomly get toolbar icon
iconPrefix = TF2CLASSES.keys()[random.randint(0,len(TF2CLASSES)-1)]
iconPath = NUKE_SHARE+'/tf2avatars/'+iconPrefix+'.jpg'
print TF2CLASSES[iconPrefix]

m = nuke.toolbar("Nodes").addMenu(TF2CLASSES[iconPrefix], icon = iconPath)

# 3D
m.addCommand('3d/Shadow Generator', 'nuke.createNode("shadow_generator")')

# 2D
m.addCommand('2d/Nuke Image Converter...', 'execfile("/usr/people/michael-ha/python/env/nukeImageConverter.py");makeProxyUI()')
m.addCommand('2d/Buf Clone', 'execfile("/usr/people/michael-ha/python/env/nukeCustomSettings.py");bclone()')
m.addCommand('2d/Connect Selection ', 'execfile("/usr/people/michael-ha/python/env/nukeCustomSettings.py");connectSel()', "CTRL+Shift+Y")
m.addCommand('2d/Clear Animation', 'execfile("/usr/people/michael-ha/python/env/nukeCustomSettings.py");clearAnim()')
m.addCommand('2d/Show-Hide inputs', 'execfile("/usr/people/michael-ha/python/env/nukeCustomSettings.py");hideInputs()',"Alt+T")
m.addCommand('2d/Set Selected or All Read Frame Range...', 'execfile("/usr/people/michael-ha/python/env/nukeCustomSettings.py");setReadFrameRange()')
m.addCommand('2d/Set frame range from selection', 'execfile("/usr/people/michael-ha/python/env/nukeCustomSettings.py");setFrameRangeFromSel()', "Ctrl+Shift+R")
m.addCommand('2d/Rename label according the dependance node', 'execfile("/usr/people/michael-ha/python/env/nukeCustomSettings.py");renameLabel()', "Ctrl+Alt+Shift+R")
m.addCommand('2d/Switch crop format', 'execfile("/usr/people/michael-ha/python/env/nukeCustomSettings.py");switchCrop()', "Ctrl+Alt+Shift+O")
m.addCommand('2d/Switch 0 - 1', 'execfile("/usr/people/michael-ha/python/env/nukeCustomSettings.py");switchUV_PROJ()', "Ctrl+Alt+Shift+S")
m.addCommand('2d/Create read from write', 'execfile("/usr/people/michael-ha/python/env/nukeCustomSettings.py");createReadFromWrite()', "Ctrl+Alt+Shift+R")
m.addCommand('2d/Toggle postage stamp on read nodes', 'execfile("/usr/people/michael-ha/python/env/nukeCustomSettings.py");togglePostageStamps()', "Ctrl+Alt+P")
m.addCommand('2d/Bezier', 'execfile("/usr/people/michael-ha/python/env/nukeCustomSettings.py");switchNode()', "Ctrl+Alt+Shift+S")
m.addCommand('2d/Switch node', 'nuke.tcl("Bezier")', "Shift+B")

# other
m.addCommand('Other/Centralize script...', 'execfile("/usr/people/michael-ha/python/centralizeNukeScript.py");makeLocalUI()')
m.addCommand('Other/Archive script...', 'execfile("/usr/people/michael-ha/python/archive_v1.0.py");ai.interface()')
m.addCommand('Other/Copy special', 'execfile("/usr/people/michael-ha/python/env/nukeCustomSettings.py");copySpecial()', "CTRL+SHIFT+C")
m.addCommand('Other/list knobs', 'execfile("/usr/people/michael-ha/python/env/nukeCustomSettings.py");listKnobs()',"Ctrl+Alt+Shift+I")
m.addCommand('Other/Play', 'execfile("/usr/people/michael-ha/python/env/nukeCustomSettings.py");nukePlay()', "Alt+V")
m.addCommand('Other/Goto first frame', 'execfile("/usr/people/michael-ha/python/env/nukeCustomSettings.py");goToFirstFrame()', "Alt+Shift+V")
m.addCommand('Other/Replace string in file knob...', 'execfile("/usr/people/michael-ha/python/env/nukeCustomSettings.py");replaceStringInFile()')
m.addCommand('Other/Set selected Write the only active write', 'execfile("/usr/people/michael-ha/python/env/nukeCustomSettings.py");setSelWriteActive()')
m.addCommand('Other/How many nodes', 'nuke.message(str(len(nuke.allNodes()))+" nodes in comp.")', "Ctrl+Shift+Alt+A")
m.addCommand('Other/Expression arrows', '_internal_expression_arrow_cmd()', "Alt+Shift+E")
m.addCommand('Other/Unselect All', 'import dmptools.macros.nukeCommands as nukeCommands ; nukeCommands.unselectAll();\
                import dmptools.macros.nukeCommands as nukeCommands ; nukeCommands.closeAllControlPanel()', "Ctrl+Space")

#root
m.addCommand('Execute', 'execfile("/usr/people/michael-ha/python/env/nukeCustomSettings.py");nukeExecute()', "Alt+E")
m.addCommand('Import exported file', 'execfile("/usr/people/michael-ha/python/env/nukeCustomSettings.py");importScript()', "Ctrl+Shift+I")
m.addCommand('Open terminal from selection', 'execfile("/usr/people/michael-ha/python/env/nukeCustomSettings.py");openTerminal()', "Alt+X")
m.addCommand('Start server', 'execfile("/usr/people/michael-ha/python/nukeserver.py");threaded_server()')
m.addCommand('Set Shot FrameRange', 'execfile("/usr/people/michael-ha/python/env/nukeCustomSettings.py");setShotFrameRange()')
m.addCommand('Show modules...', 'execfile("/usr/people/michael-ha/python/env/nukeCustomSettings.py");showModules()')
