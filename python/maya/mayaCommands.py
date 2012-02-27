# =====================
#
# maya custom tools
#
# =====================

import maya.cmds as cmds
import maya.mel as mel
import os
import time
import subprocess

from dmptools.presets import PresetsManager

def launchSublimeText():

    # get the sublime text path preset if exists
    presets = PresetsManager()
    sublimeTextPath = presets.getPreset('sublime_text_path')
    if sublimeTextPath and os.path.exists(sublimeTextPath[0]):
        # launch sublime text
        subprocess.Popen(sublimeTextPath[0])
    else:
        # ask for the sublime text exe path
        filedialog = cmds.fileDialog2(cap='Please give me the path of Sublime Text.exe !',
                        fm=1,
                        dir='C:\\Program Files\\',
                        ff='*.exe')
        if filedialog:
            sublimeTextPath = str(filedialog[0])
            if os.path.exists(sublimeTextPath):
                # setting preset
                presets.addPreset('sublime_text_path', sublimeTextPath)
                # launch sublime text
                subprocess.Popen(sublimeTextPath)
        else:
            raise UserWarning('No exe found !')

def launchNuke():

    # get the sublime text path preset if exists
    presets = PresetsManager()
    nukePath = presets.getPreset('nuke_path')
    if nukePath:
        if os.path.exists(nukePath[0]):
            # launch sublime text
            subprocess.Popen(nukePath[0]+" --nukex")
        else:
            raise UserWarning('No exe found !')
    else:
        # ask for the sublime text exe path
        filedialog = cmds.fileDialog2(cap='Please give me the path of Nuke.exe !',
                        fm=1,
                        dir='C:\\Program Files\\',
                        ff='*.exe')
        if filedialog:
            nukePath = str(filedialog[0])
            if os.path.exists(nukePath):
                # setting preset
                presets.addPreset('nuke_path', nukePath)
                # launch sublime text
                subprocess.Popen(nukePath+" --nukex")
            else:
                raise UserWarning('No exe found !')
        else:
            raise UserWarning('No exe found !')

def setDefaultRenderer():
    panel = cmds.getPanel(wf=True)
    cmds.modelEditor(panel, shadows=False, displayLights='all', e=True)
    cmds.modelEditor(panel, rnm='base_OpenGL_Renderer', e=True)

def setHardwareRenderer():
    panel = cmds.getPanel(wf=True)
    cmds.modelEditor(panel, shadows=True, displayLights='all', e=True)
    cmds.modelEditor(panel, rnm='hwRender_OpenGL_Renderer', e=True)

def setViewport2Renderer():
    panel = cmds.getPanel(wf=True)
    cmds.modelEditor(panel, shadows=True, displayLights='all', e=True)
    cmds.modelEditor(panel, rnm='ogsRenderer', e=True)

def assignSurfaceShader(name="", values=(0,0,0)):

    selection = cmds.ls(sl = True)
    print name, selection, values[0], values[1], values[2]
    
    if selection:
        # if the shader already exists
        if name in cmds.ls("*", type = "surfaceShader") and name+"SG" in cmds.ls("*", type = "shadingEngine"):
            for node in selection:
                try:
                    cmds.select(node, r = True)
                    cmds.sets(node, e = True, forceElement = name+"SG")
                except:
                    pass
                    
        # otherwise create the shader
        else:
            shader = cmds.shadingNode('surfaceShader', asShader = True, name = name)
            shadingGroup = cmds.sets(shader, renderable = True, noSurfaceShader = True, empty = True, name = name+"SG")
            cmds.connectAttr(shader+".outColor", shadingGroup+".surfaceShader", force = True)
            cmds.setAttr(shader+".outColor", values[0], values[1], values[2], type = "double3")
        
            for node in selection:
                try:
                    cmds.sets(node, e = True, forceElement = name+"SG")
                except:
                    pass
            
        cmds.select(selection, r = True)

def askFlushUndo():
    confirm = cmds.confirmDialog(t = "flushUndo", m = 'Are you sure ?', ma = "center", b = ['Yes','No'], db = 'Yes', cb = 'No', ds = 'No' )
    if confirm == "Yes":
        print "flushUndo..."
        cmds.flushUndo()
    else:
        print "abort..."

def undoQueue(undos=100):
    # set the undo queue 
    cmds.undoInfo(state = True, infinity = False, length = undos)
    
def switchHighlightedSelection():
    panel = cmds.getPanel(wf = True)
    cmds.modelEditor(panel, edit = True, sel = not cmds.modelEditor(panel, query = True, sel = True))
    
def transferVertices(meshes=[], preserveUVs=True):
    
    dateStart = str(time.strftime('%d/%m/%y at %H:%M:%S'))
    
    if len(meshes) == 2:
        verticesRange1 = int(cmds.ls(meshes[0]+".vtx[*]")[0].split(":")[-1][:-1])
        verticesRange2 = int(cmds.ls(meshes[1]+".vtx[*]")[0].split(":")[-1][:-1])
        if verticesRange1 == verticesRange2:
            for vertex in range(verticesRange1+1):
                vertexName1 = meshes[0]+".vtx["+str(vertex)+"]"
                vertexName2 = meshes[1]+".vtx["+str(vertex)+"]"
                xform1 = cmds.xform(vertexName1, q = True, ws = True, t = True)
                xform2 = cmds.xform(vertexName2, q = True, ws = True, t = True)
                #print " > moving", meshes[0], "vtx", vertex, "to", xform2
                cmds.select(vertexName1, r = True)
                cmds.move(xform2[0], xform2[1], xform2[2], ws = True, puv = preserveUVs)
        
        else:
            cmds.warning("The selection doesn't have the same vertex count !")
    else:
        cmds.warning("Please select 2 objects !")
        
    dateEnd = str(time.strftime('%d/%m/%y at %H:%M:%S'))
    print " > Process started at", dateStart, "and ended at", dateEnd

def toggleNormals():
    #toggle normals
    cmds.polyOptions(r = True, f = True, dn = not cmds.polyOptions(q = True, dn = True))
    
def unselectAll():
    # unselect all
    cmds.select(clear = True)
    
def setWireframe():
    panel = cmds.getPanel(wf = True)
    cmds.modelEditor(panel, edit = True, wireframeOnShaded = not cmds.modelEditor(panel, query = True, wireframeOnShaded = True))
    
def setBackfaceCulling():
    panel = cmds.getPanel(wf = True)
    cmds.modelEditor(panel, edit = True, backfaceCulling = not cmds.modelEditor(panel, query = True, backfaceCulling = True))
    
def setDefaultMaterial():
    panel = cmds.getPanel(wf = True)
    cmds.modelEditor(panel, edit = True, useDefaultMaterial = not cmds.modelEditor(panel, query = True, useDefaultMaterial = True))

def bufMove():
    'enter the Buf move vertex mode'
    sel = cmds.ls(sl = True)
    if cmds.nodeType(sel) == 'transform':
        if cmds.nodeType(cmds.listRelatives(sel)) == 'mesh':
            mode = 'mesh'
        if cmds.nodeType(cmds.listRelatives(sel)) == 'nurbsCurve':
            mode = 'nurbs'
    if cmds.nodeType(sel) == 'mesh':
        mode = 'mesh'
    if cmds.nodeType(sel) == 'nurbsCurve':
        mode = 'nurbs'
    
    try:    
        if mode == 'mesh':
            cmds.selectMode(component = True)
            panel = cmds.getPanel(withFocus = True)
            cmds.modelEditor(panel, e = True, manipulators = False)
            cmds.setToolTo('moveSuperContext')
            cmds.selectType(alc = 0)
            cmds.selectType(v = 1)
            cmds.selectPref(clickDrag = True)
        if mode == 'nurbs':
            cmds.selectMode(component = True)
            panel = cmds.getPanel(withFocus = True)
            cmds.modelEditor(panel, e = True, manipulators = False)
            cmds.setToolTo('moveSuperContext')
            cmds.selectType(alc = 0)
            cmds.selectType(cv = 1)
            cmds.selectPref(clickDrag = True)
    except:
        pass
    #cmds.selectPref(useDepth = True)
    
def bufMoveRelease():
    
    cmds.selectMode(object = True)
    panel = cmds.getPanel(withFocus = True)
    cmds.modelEditor(panel, e = True, manipulators = True)
    cmds.setToolTo('moveSuperContext')
    cmds.selectPref(clickDrag = False)
    #cmds.selectPref(useDepth = False)

def importScene():
    'import scene exported from nuke'
    
    crosswalkFile = 'nukeToMaya.info'
    if os.path.exists(crosswalkFile):
        fileInfo = open(crosswalkFile, 'r')
        mayaFile = fileInfo.readlines()[-1].split('=')[-1][:-1]
        if os.path.exists(mayaFile):
            cmds.file(mayaFile, i = True, type = 'mayaAscii', ra = True)
        else:
            print mayaFile
            mel.eval('warning "File '+mayaFile+' not found !"')

def isolateSelection():
    'isolate selection'
    
    activePanel = cmds.getPanel(wf = True)
    cmds.isolateSelect(activePanel, state = not cmds.isolateSelect(activePanel, q = True, state = True))
    #cmds.isolateSelect(activePanel, as = True)
    
def isolateSelectionRelease():
    
    activePanel = cmds.getPanel(wf = True)
    cmds.isolateSelect(activePanel, state = not cmds.isolateSelect(activePanel, q = True, state = True))
    #cmds.isolateSelect(activePanel, as = True)

def hideSel():
    
    sel = cmds.ls(sl = True)
    for node in sel:
        cmds.setAttr(node+'.visibility', 0)
        
def hideSelSwitch():
    
    sel = cmds.ls(sl = True)
    for node in sel:
        cmds.setAttr(node+'.visibility', not cmds.getAttr(node+'.visibility'))

def hideSelRelease():
    
    sel = cmds.ls(sl = True, dag = True)
    for node in sel:
        cmds.setAttr(node+'.visibility', 1)

def openTerminal():
    
    job = os.environ['JOB']
    shot = os.environ['SHOT']
    discipline = os.environ['DISCIPLINE']
    jobCmd = 'job -d '+discipline+' '+job+' '+shot
    #os.system('gnome-terminal --title '+job+'--'+shot+' -x tcsh -c "'+jobCmd+';tcsh"&')
    os.system('mpxterm -e "'+jobCmd+';tcsh"&')

def assignBlackShader():

    global switch
    activeModel = cmds.getPanel(wf = True)
    cmds.modelEditor(activeModel, e = True, udm = 1)
    cmds.displayRGBColor( 'background', 0, 0, 0 )
    cmds.setAttr('lambert1.color', 0, 0, 0, type = "double3")
    cmds.setAttr('lambert1.diffuse', 0)
    cmds.displayRGBColor('userDefined1', 1 ,1 ,1 )

    for node in cmds.ls(sl = True):
        cmds.color(ud = 1) # assign white wireframes
    switch = 1

def assignDefaultShader():

    global switch
    activeModel = cmds.getPanel(wf = True)
    cmds.modelEditor(activeModel, e = True, udm = 0)
    cmds.displayRGBColor( 'background', 0.61, 0.61, 0.61 )
    cmds.setAttr('lambert1.color', 0.5, 0.5, 0.5, type = "double3")
    cmds.setAttr('lambert1.diffuse', 0.5)
    for node in cmds.ls(sl = True):
        cmds.color() # assign default wireframes
    switch = 1

def switchShaders():

    global switchshader
    try:
        switchshader
    except:
        switchshader = 1

    if switchshader == 1:
        assignBlackShader()
        switchshader = 0
    elif switchshader == 0:
        assignDefaultShader()
        switchshader = 1

def getCam():

    sel = cmds.ls(sl = True)
    if sel:
        camShape = cmds.listRelatives(sel[0])[0]
        if cmds.nodeType(camShape) == 'camera':
            setRenderCamera(sel[0], camShape)

def cameraPanTool():
    panContext = cmds.panZoomCtx(panMode = True)
    cmds.setToolTo(panContext)
    
def cameraZoomTool():
    zoomContext = cmds.panZoomCtx(zoomMode = True)
    cmds.setToolTo(zoomContext)

def resetPanZoom():
    panel = cmds.getPanel(wf = True)
    cameraNode = cmds.modelPanel(panel, q = True, camera = True)

    cmds.setAttr(cameraNode+".zoom", 1)
    cmds.setAttr(cameraNode+".horizontalPan", 0)
    cmds.setAttr(cameraNode+".verticalPan", 0)

def polySplitTool():
    polysplit = cmds.polySplitCtx()
    cmds.setToolTo(polysplit)

def selectNgones():
    panel = cmds.getPanel(withFocus = True)
    cmds.modelEditor(panel, e = True, manipulators = False)
    cmds.selectMode(component = True)
    cmds.selectType(fc = 1)
    cmds.polySelectConstraint(m = 3, t = 8, sz = 3)
    
def selectNgonesRelease():
    panel = cmds.getPanel(withFocus = True)
    cmds.modelEditor(panel, e = True, manipulators = True)
    cmds.select(clear = True)
    cmds.selectMode(object = True)
    cmds.polySelectConstraint(m = 0)

def switchSelectNgones():
    global switchselectngones
    try:
        switchselectngones
    except:
        switchselectngones = 1

    if switchselectngones == 1:
        selectNgones()
        switchselectngones = 0
    elif switchselectngones == 0:
        selectNgonesRelease()
        switchselectngones = 1

def selectTriangles():
    panel = cmds.getPanel(withFocus = True)
    cmds.modelEditor(panel, e = True, manipulators = False)
    cmds.selectMode(component = True)
    cmds.selectType(fc = 1)
    cmds.polySelectConstraint(m = 3, t = 8, sz = 1)

def selectTrianglesRelease():
    panel = cmds.getPanel(withFocus = True)
    cmds.modelEditor(panel, e = True, manipulators = True)
    cmds.select(clear = True)
    cmds.selectMode(object = True)
    cmds.polySelectConstraint(m = 0)

def switchSelectTriangles():
    global switchselecttriangles
    try:
        switchselecttriangles
    except:
        switchselecttriangles = 1

    if switchselecttriangles == 1:
        selectTriangles()
        switchselecttriangles = 0
    elif switchselecttriangles == 0:
        selectTrianglesRelease()
        switchselecttriangles = 1

def setDefaultLight():
    activePanel = cmds.getPanel(wf = True)
    cmds.modelEditor(activePanel, e = True, dl = "default")

def setAllLight():
    activePanel = cmds.getPanel(wf = True)
    cmds.modelEditor(activePanel, edit = True, displayLights = 'all')

def switchLight():
    global switchlight
    try:
        switchlight
    except:
        switchlight = 1

    if switchlight == 1:
        setDefaultLight()
        switchlight = 0
    elif switchlight == 0:
        setAllLight()
        switchlight = 1
   
def lockPickNodes(lock=True):
    for node in cmds.ls(sl = True):
        try:
            cmds.lockNode(node, lock=lock)
        except:
            cmds.warning("cannot lockPick this node: "+str(node))
            
# this is a silly place