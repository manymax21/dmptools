# ============================
#
# maya custom tools for neo
#
# ============================

import maya.cmds as cmds
import maya.mel as mel

class HideShowNeoStuff(object):

    def __init__(self):
        self.stuffToHide = []
        nodes = cmds.ls()
        objFilter = ['Dest', 'Collision_hk', 'Orig_State', 'Dest_State']
        
        for node in nodes:
            for f in objFilter:
                if f in node:
                    self.stuffToHide.append(node)
                    break
     
    def hide(self):
        for node in self.stuffToHide:
            cmds.setAttr(node+'.visibility', False)
    
    def show(self):
        for node in self.stuffToHide:
            cmds.setAttr(node+'.visibility', True)
     
def deleteCollada():
    """ delete collada nodes"""
    colladaNodes = []
    for node in cmds.ls():
        if 'colladaDocuments' in node:
            colladaNodes.append(node)
        
    cmds.delete(colladaNodes)

def rotateScene():
    global switchRotate
    try:
        switchRotate
    except:
        switchRotate = 1

    if switchRotate == 1:
        try:
            cmds.setAttr('|Neo|generator_outpost_01_dm|Asset|Model_Orig_00|scene_grp.ry', 0.0)
            switchRotate = 0
        except:
            pass
        
    elif switchRotate == 0:
        try:
            cmds.setAttr('|Neo|generator_outpost_01_dm|Asset|Model_Orig_00|scene_grp.ry', 45.0)
            switchRotate = 1
        except:
            pass
