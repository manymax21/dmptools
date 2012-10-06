# ============================
#
# maya custom tools for neo
#
# ============================

import os
import sys
import fileinput

import maya.cmds as cmds
import maya.mel as mel

import dmptools.mayaCommands as mayaCommands

def replaceShaderInModel():

    paths = ['s:/assets/environs/sp/air/moon/fragments/',
            's:/assets/props_DS3/Structures/segments/air/moon',        
            ]
    paths = ['s:/assets/environs/sp/air/moon/fragments/alien_building_ext_z01']
    replacement = {'tel_1L_baseWall01_reflection': 'tel_1L_baseWall01_ch10'}

    stuff = ''
    filesList = []
    # check the files in the install path
    for path in paths:
        for root, dirs, files in os.walk(path):
            for f in files:
                # go through python & mel files only
                if f.split('.')[-1] in ['dae',]:
                    filesList.append(root+'\\'+f)
                    for line in fileinput.input(root+'/'+f, inplace=0):
                        # if the key in REPLACEMENTS is in the file then replace the line
                        for rep in replacement.keys():
                            if rep in line:
                                stuff += str(root)+' '+str(f)+' '+str(line)+' -> '+line.replace(rep, replacement[rep])+'\n'
                                line = line.replace(rep, replacement[rep])
                        # write the replaced line in the file
                        # write the file with the new string
                        #sys.stdout.write(line)

def hideCollisions():
    """hide collisions models"""

    global switchCollisions

    mel.eval('source NEO_hideUnhideCollision;')
    mel.eval('NEO_hideCollision;')

    mayaCommands.headsUpDisplayMessage('hidding collisions !')

    switchCollisions = 1

def unhideCollisions():
    """unhide collisions models"""

    global switchCollisions

    mel.eval('source NEO_hideUnhideCollision;')
    mel.eval('NEO_unhideCollision();')

    mayaCommands.headsUpDisplayMessage('showing collisions !')

    switchCollisions = 1

def switchCollisionsVisibility():
    global switchCollisions

    try:
        switchCollisions
    except:
        switchCollisions = 1

    if switchCollisions == 1:
        hideCollisions()
        switchCollisions = 0
    elif switchCollisions == 0:
        unhideCollisions()
        switchCollisions = 1

def hideModels():

    global switchModels

    for node in cmds.ls("Asset_Model"):
        cmds.setAttr(node+".visibility", False)
    for node in cmds.ls("Model"):
        cmds.setAttr(node+".visibility", False)
    for node in cmds.ls("State"):
        cmds.setAttr(node+".visibility", False)

    mayaCommands.headsUpDisplayMessage('hidding models !')

    switchModels = 1

def unhideModels():

    global switchModels

    for node in cmds.ls("Asset_Model"):
        cmds.setAttr(node+".visibility", True)
    for node in cmds.ls("Model"):
        cmds.setAttr(node+".visibility", True)
    for node in cmds.ls("State"):
        cmds.setAttr(node+".visibility", True)

    mayaCommands.headsUpDisplayMessage('showing models !')

    switchModels = 1

def switchModelsVisibility():
    global switchModels

    try:
        switchModels
    except:
        switchModels = 1

    if switchModels == 1:
        hideModels()
        switchModels = 0
    elif switchModels == 0:
        unhideModels()
        switchModels = 1

def assignArtblockShader():
    """select objects with lambert1 and assign the artblock shader"""

    cmds.hyperShade(objects='lambert1')
    if cmds.ls(sl=True):
        cmds.hyperShade(assign='ar_blockworldGrey01')

def fixColladaAttributes():
    """fix dead space collada shader attributes"""
    nodes = cmds.ls(sl=True)
    for node in nodes:
        if not cmds.getAttr(node+'.collada'):
            mat = cmds.getAttr(node+'.forceFragment')
            cmds.setAttr(node+'.collada', mat, type='string')


def createCollisionBox():
    """
        batch create collision bounding box
    """
    collisions = []
    
    sel = cmds.ls(sl=True)
    if sel:
        for node in sel:
            cmds.select(node, r=True)
            # create object aligned collision box
            mel.eval('MODEL_obb_bruteForce(1);')
            cmds.delete(ch=True)
            collisions.append(cmds.ls(sl=True)[0])
        
        cmds.select(collisions, r=True)    
    else:
        cmds.warning('no object found...')

class States(object):
    def __init__(self):
        self.orig = ['Model_Orig_00']
        self.dest = ['Model_Dest_01',
                'Model_Dest_02',
                'Model_Dest_01',
                'Collision_hk_nav_model_Orig_00',
                'Collision_hk_nav_model_Dest_01',
                'Collision_hk_nav_model_Dest_02',
                'Orig_State_00',
                'Dest_State_01',
                'Dest_State_02']
        
    def setOrig(self):
        [cmds.setAttr(node+'.visibility', False) for node in self.dest]
        [cmds.setAttr(node+'.visibility', True) for node in self.orig]

    def setDest(self):
        [cmds.setAttr(node+'.visibility', True) for node in self.dest]
        [cmds.setAttr(node+'.visibility', False) for node in self.orig]

def switchDestructionState():
    states = States()
    global switchDest
    try:
        switchDest
    except:
        switchDest = 1

    if switchDest == 1:
        try:
            states.setOrig()
            switchDest = 0
        except:
            pass
        
    elif switchDest == 0:
        try:
            states.setDest()
            switchDest = 1
        except:
            pass
            
class HideShowNeoStuff(object):

    def __init__(self):
        self.stuffToHide = []
        self.dest1Stuff = []
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

def rotateGenerator():
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
