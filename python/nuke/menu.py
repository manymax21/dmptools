#==============================================================================
#
# script by michael-ha - michael.havart@gmail.com
# 3dmp nuke toolbar
# 
# 13 jul 2011
#
#==============================================================================

import nuke
import nukescripts
import sys

VERSION = '!VERSION!'
NUKE_SHARE = '!NUKE_SHARE!'

# import macros that are loaded at nuke startup
import dmptools.macros.nukeCommands as nukeCommands
from dmptools.tools.scanlineRenderManager import ScanlineRenderManager

#============================
#   DEFAULT STARTUP TOOLS 
#============================

# add a frame range override on write node creation for the alfredRender tool
nukeCommands.addFrameRangeOverride()

# auto check alpha on write node creation 
nukeCommands.autoCheckAlpha()

# auto check gl_light on viewers 
nukeCommands.viewerSettings()

# add a latestAutosave menu item 
nuke.menu("Nuke").addCommand('File/Recent Files/Latest autosave', 'import dmptools.macros.nukeCommands as nukeCommands ; nuke.scriptOpen(nukeCommands.getLatestAutosave())')

#========================
#   BUILD THE TOOLBAR 
#========================

# create 3ddmp toolbar
toolbar = nuke.toolbar("Nodes").addMenu('tools v'+VERSION, icon = NUKE_SHARE+'/toolbar.png')

# toolbar menus
toolbar.addMenu('Tools', icon = NUKE_SHARE+'/tools.png')
toolbar.addMenu('Nodes', icon = NUKE_SHARE+'/nodes.png')
toolbar.addMenu('Nodes/2d')
toolbar.addMenu('Nodes/3d')
toolbar.addMenu('Macros', icon = NUKE_SHARE+'/macros.png')
toolbar.addMenu('Macros/2d')
toolbar.addMenu('Macros/3d')

#===================
#    TOOLS MENU
#===================

#export nuke to maya
toolbar.addCommand('Tools/Nuke to Maya...', 'import dmptools.tools.exportNukeToMaya as exportNukeToMaya ; exportNukeToMaya.exportToMayaUI()', icon = NUKE_SHARE+'/nukeToMaya.png')
# psd to nuke 
toolbar.addCommand('Tools/Psd to Nuke...', 'import dmptools.tools.psdToNuke as psdToNuke ; psdToNuke.psdToNuke()', icon = NUKE_SHARE+'/psdToNuke.png')
# ratio calculator
toolbar.addCommand('Tools/Ratio calculator...', 'import dmptools.tools.nukeRatioCalculator as nukeRatioCalculator ; nukeRatioCalculator.ratioCalculator()', icon = NUKE_SHARE+'/ratioCalculator.png')
# bake camera projections into uv textures
toolbar.addCommand('Tools/Bake projection to UV...', 'import dmptools.tools.bakeProjToUV as bakeProjToUV ; bakeProjToUV.bakeItUI()', icon = NUKE_SHARE+'/bake.png')
# scanline render manager
sc = ScanlineRenderManager()
pane = nuke.menu("Pane")
pane.addCommand( "scanlineRenderManager", sc.addToPane)
nukescripts.registerPanel('ScanlineRenderManager', sc.addToPane)
toolbar.addCommand('Tools/Scanline Render Manager', sc.show, icon = NUKE_SHARE+'/scanline.png')

#===================
#    NODES MENU
#===================

#2D
# coverage map
toolbar.addCommand('Nodes/2d/Coverage Map', 'nuke.createNode("coverageMap")')
# apply lut
toolbar.addCommand('Nodes/2d/Apply Lut', 'nuke.createNode("ApplyLUT")')

# 3D
# create projection camera from render camera
toolbar.addCommand('Nodes/3d/Bake-Create Camera', 'import dmptools.nodes.bakeCamera as bakeCamera ; bakeCamera.BakeCamera()')
# 3d image plane
toolbar.addCommand('Nodes/3d/Image plane', 'nuke.createNode("imagePlane")')
# populate geo on 3d selection
toolbar.addCommand('Nodes/3d/Populate 3d Geo ...', 'import dmptools.tools.nukePopulate as nukePopulate ; nukePopulate.main()')
# sequence manager (dev)
toolbar.addCommand('Nodes/3d/Sequence Manager', 'nuke.createNode("sequenceManager")')

#===================
#   MACROS MENU
#===================

# 2D
# set the colorspace of the selected read nodes
toolbar.addCommand('Macros/2d/Set colorspace...', 'import dmptools.macros.nukeCommands as nukeCommands ; nukeCommands.setColorspace()')
# try to reload the selected nodes
toolbar.addCommand('Macros/2d/Reload selected nodes', 'import dmptools.macros.nukeCommands as nukeCommands ; nukeCommands.reloadReadNodes()', "Shift+Alt+R")
# flip the viewer
toolbar.addCommand('Macros/2d/Flip', 'import dmptools.macros.nukeCommands as nukeCommands ; nukeCommands.flipViewer()', "`")
# flop the viewer
toolbar.addCommand('Macros/2d/Flop', 'import dmptools.macros.nukeCommands as nukeCommands ; nukeCommands.flopViewer()', "Alt+`")
# align nodes in the nodegraph
toolbar.addCommand('Macros/2d/Align Up', 'import dmptools.macros.nukeCommands as nukeCommands ; nukeCommands.upAlignSelectedNodes()')
toolbar.addCommand('Macros/2d/Align Center', 'import dmptools.macros.nukeCommands as nukeCommands ; nukeCommands.centerAlignSelectedNodes()')
toolbar.addCommand('Macros/2d/Align Down', 'import dmptools.macros.nukeCommands as nukeCommands ; nukeCommands.downAlignSelectedNodes()')
# search and replace string in file knob
toolbar.addCommand('Macros/2d/Search and replace string in file knob...', 'import dmptools.macros.nukeCommands as nukeCommands ; nukeCommands.replaceStringInFile()')
# show the path of all or selected read nodes
toolbar.addCommand('Macros/2d/Show paths of all or selected Read nodes...', 'import dmptools.macros.nukeCommands as nukeCommands ; nukeCommands.printPath()')
# unselect and close all nodes control panel
toolbar.addCommand('Macros/2d/Close all the nodes control panel', 'import dmptools.macros.nukeCommands as nukeCommands ; nukeCommands.closeAllControlPanel()')
# create viewerinput node check
toolbar.addCommand('Macros/2d/Viewerinput Check node', 'import dmptools.macros.nukeCommands as nukeCommands ; nukeCommands.createViewerInput()', "CTRL+ALT+X")

# 3D
# toggle visibility of 3d nodes
toolbar.addCommand('Macros/3d/toggle camera and geo display', 'import dmptools.macros.nukeCommands as nukeCommands ; nukeCommands.toggleCamGeoDisplay()',"Ctrl+Alt+Shift+C")
# go through wireframe, shaded, textured and textured+wireframe
toolbar.addCommand('Macros/3d/Wireframe', 'import dmptools.macros.nukeCommands as nukeCommands ; nukeCommands.setDisplayWireframe()', "Ctrl+Alt+4")
toolbar.addCommand('Macros/3d/Shaded', 'import dmptools.macros.nukeCommands as nukeCommands ; nukeCommands.setDisplayShaded()', "Ctrl+Alt+5")
toolbar.addCommand('Macros/3d/Textured', 'import dmptools.macros.nukeCommands as nukeCommands ; nukeCommands.setDisplayTextured()', "Ctrl+Alt+6")
toolbar.addCommand('Macros/3d/Textured+Lines', 'import dmptools.macros.nukeCommands as nukeCommands ; nukeCommands.setDisplayTexturedLines()', "Ctrl+Alt+7")
toolbar.addCommand('Macros/3d/Enable-Disable gl lighting', 'import dmptools.macros.nukeCommands as nukeCommands ; nukeCommands.gl_lighting()', "Ctrl+Alt+0")

# intranet help
toolbar.addCommand('Help !', '', icon = NUKE_SHARE+'/help.png')
