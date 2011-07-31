# ======================================================
# 
# menu.py
# 
#======================================================

import nuke
import sys

tools_workspace_path = 's:/work/workspace/'
sys.path.append(tools_workspace_path)

import tools.python.nuke.nukeCustomSettings as nc

# toolbar
toolbar = nuke.toolbar("Nodes").addMenu('tools')

toolbar.addCommand('Global Lighting', nc.gl_lighting)