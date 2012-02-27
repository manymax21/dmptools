#=====================================
#
# custom commands and tools for nuke
# michael.havart@gmail.com
#
#=====================================

import nuke
import nukescripts
import re
import os
import commands as cmd
import sys
import time
import re

class PrintPath(nukescripts.PythonPanel):
    """panel the printPath tool"""
    def __init__(self):
        self.reads = nuke.selectedNodes('Read')
        
        if len(self.reads) == 0:
            self.reads = nuke.allNodes('Read')
        nukescripts.PythonPanel.__init__( self, 'PrintPath', 'printpath')
       
        self.textKnob = nuke.Multiline_Eval_String_Knob('Paths:')

        readList = []
        for read in self.reads:
            readList.append(read.name()+": "+read['file'].value())
        readStr = "\n".join(readList)

        self.textKnob.setValue(readStr)
   
        self.refreshButton = nuke.PyScript_Knob('refresh')

        self.addKnob(self.textKnob)
        self.addKnob(self.refreshButton)

    def knobChanged(self, knob):
        if knob == self.refreshButton:
            reads = nuke.selectedNodes('Read')
            if len(reads) == 0:
                reads = nuke.allNodes('Read')
                
            readList = []
            for read in reads:
                readList.append(read.name()+": "+read['file'].value())
            readStr = "\n".join(readList)
            
            self.textKnob.setValue(readStr)
            
def printPath():
    """return a panel with the path of the selected nodes"""
    nukescripts.registerPanel( 'printpath', printPath)
    PrintPath().show()
        
def frameRangeOverrideTab():
    """add an frame override field to a write node"""
    
    node = nuke.thisNode()
    
    envTab = nuke.Tab_Knob("envTab", "dmptools options")
    checkBox = nuke.Boolean_Knob("useOverride","Override frame range")
    checkBox.setValue(True)
    frameRangeKnob = nuke.EvalString_Knob("frameRangeOverride", "frame range", "")
    
    node.addKnob(envTab)
    node.addKnob(checkBox)
    node.addKnob(frameRangeKnob)
    
    node.knob('file').setFlag(True)

def updateWrite():
    # update the write node
    pass

def fetchReadNode():
    # ...
    node = nuke.thisNode()
    print str(node.name())
    read = fetchReadNodeInTree(node)
    if read:
        print str(read.name())
        if os.path.exists(read['file'].getEvaluatedValue()):
            print str(nuke.frame())
            print str(read.name()), 'the file '+str(read['file'].getEvaluatedValue())+' exists ...'
        
def checkDependencies(node):
    #print node.name()
    depNodes = nuke.dependencies(node, nuke.INPUTS | nuke.HIDDEN_INPUTS | nuke.EXPRESSIONS)
    #print depNodes
    nodes = []
    for depNode in depNodes:
        if depNode.Class() == 'Read':
            #print 'found '+depNode.name()
            return depNode
        else:
            nodes.append(depNode)
    #print nodes
    if nodes:
        for dep in nodes:
            result = checkDependencies(dep)
    return result

def fetchReadNodeInTree(node):
    """return read node in the branch"""
    readNode = checkDependencies(node)
    return readNode

def loopnodes(knobs={}):
    """
    will iterate through a selection of nodes and set values on knobs
    loopnodes({<knobname>:<value>})
    ex:
    loopnodes({"samples":10, "shutter":0.5})
    """
    
    for node in nuke.selectedNodes():
        for knob, value in knobs.items():
            try:
                print 'set', node.name(), knob, knobs[knob]
                node[knob].setValue(knobs[knob])
            except:
                print 'FAILED', node.name(), knob, knobs[knob]
                
def unselectAll():
    """selection utils"""
    for node in nuke.allNodes():
        node['selected'].setValue(False)
        if node.Class() == 'Group':
            node.begin()
            for child in nuke.allNodes():
                child['selected'].setValue(False)
            node.end()

def selectReplace(sel):
    """select replace"""
    if type(sel).__name__ == 'str':
        unselectAll()
        sel['selected'].setValue(True)
    if type(sel).__name__ == 'list':
        unselectAll()
        for node in sel:
            node['selected'].setValue(True)
    
def selectAdd(node):
    """add to actual selection"""
    node['selected'].setValue(True)

def closeAllControlPanel():
    """close all node control panel"""
    for node in nuke.allNodes():
        node.hideControlPanel()
        if node.Class() == 'Group':
            node.begin()
            for child in nuke.allNodes():
                child.hideControlPanel()
                child['selected'].setValue(False)
            node.end()

def clearAnim():
    """clear animation of all the knobs in the selected nodes"""
    for node in nuke.selectedNodes():
        # rotopaint
        if node.Class() == "RotoPaint":
            rotoCurves = node['curves']
            for knob in node.knobs():
                if nuke.Knob.isAnimated(node[knob]):
                    nuke.Knob.clearAnimated(node[knob])            
                    print "clearing animation of: "+node.name()+" "+node[knob].name()
        # other nodes
        if not node.Class() == "RotoPaint":
             for knob in node.knobs():
                if nuke.Knob.isAnimated(node[knob]):
                    nuke.Knob.clearAnimated(node[knob])            
                    print "clearing animation of: "+node.name()+" "+node[knob].name()

def bclone():
    """create a transparent clone to clean the node tree"""
    node = nuke.selectedNodes()
    if len(node)==1:
        clone1 = nuke.createNode("NoOp", inpanel = False)
        clone1.setName("Bclone")
        clone1['label'].setValue(node[0].name()+"\nClone_Parent")
        clone1['tile_color'].setValue(2521651711)
        clone1['note_font_color'].setValue(1583243007)
        clone1xpos = clone1['xpos'].getValue()
        clone1ypos = clone1['ypos'].getValue()
    
        clone2 = nuke.createNode("NoOp", inpanel = False)
        clone2.setName("Bclone")
        clone2['label'].setValue(node[0].name()+"\nClone")
        clone2['hide_input'].setValue(True)
        clone2['tile_color'].setValue(2521651711)
        clone2['note_font_color'].setValue(1583243007)
        clone2['xpos'].setValue(clone1xpos)
        clone2['ypos'].setValue(clone1ypos)

    if len(node)==0:
        clone1 = nuke.createNode("NoOp", inpanel = False)
        clone1.setName("Bclone")
        clone1['label'].setValue("Clone_Parent")
        clone1['tile_color'].setValue(2521651711)
        clone1['note_font_color'].setValue(1583243007)
        clone1xpos = clone1['xpos'].getValue()
        clone1ypos = clone1['ypos'].getValue()
    
        clone2 = nuke.createNode("NoOp", inpanel = False)
        clone2.setName("Bclone")
        clone2['label'].setValue("Clone")
        clone2['hide_input'].setValue(True)
        clone2['tile_color'].setValue(2521651711)
        clone2['note_font_color'].setValue(1583243007)
        clone2['xpos'].setValue(clone1xpos)
        clone2['ypos'].setValue(clone1ypos)
    if len(node)!=0 and len(node)!=1:
        nuke.message('Just select one node to clone !')

def setDisplayWireframe():
    """set all 3d to wireframe mode"""
    for node in nuke.allNodes():
        print node.name()
        goodGeo = ["Group", "ReadGeo","ReadGeo2","Sphere","Cube","Cylinder","Card", "Card2"]
        if node.Class() in goodGeo:
            if node.Class() == "Group":
                node.begin()
                for child in nuke.allNodes():
                    if child.Class() in goodGeo:
                        child['display'].setValue(1)
                node.end()
            else:
                node['display'].setValue(1)
                
def setDisplayShaded():
    """set all 3d to shaded mode"""
    for node in nuke.allNodes():
        print node.name()
        goodGeo = ["Group", "ReadGeo","ReadGeo2","Sphere","Cube","Cylinder","Card", "Card2"]
        if node.Class() in goodGeo:
            if node.Class() == "Group":
                node.begin()
                for child in nuke.allNodes():
                    if child.Class() in goodGeo:
                        child['display'].setValue(2)
                node.end()
            else:
                node['display'].setValue(2)
                
def setDisplayTextured():
    """set all 3d to textured mode"""
    for node in nuke.allNodes():
        print node.name()
        goodGeo = ["Group", "ReadGeo","ReadGeo2","Sphere","Cube","Cylinder","Card", "Card2"]
        if node.Class() in goodGeo:
            if node.Class() == "Group":
                node.begin()
                for child in nuke.allNodes():
                    if child.Class() in goodGeo:
                        child['display'].setValue(4)
                node.end()
            else:
                node['display'].setValue(4)
                
def setDisplayTexturedLines():
    """set all 3d to textured mode"""
    for node in nuke.allNodes():
        print node.name()
        goodGeo = ["Group", "ReadGeo","ReadGeo2","Sphere","Cube","Cylinder","Card", "Card2"]
        if node.Class() in goodGeo:
            if node.Class() == "Group":
                node.begin()
                for child in nuke.allNodes():
                    if child.Class() in goodGeo:
                        child['display'].setValue(5)
                node.end()
            else:
                node['display'].setValue(5)
                
def setFrameRangeFromSel():
    """set the timeline with the handles of the selected node."""
    sel = nuke.selectedNodes()
    if sel:
        nuke.root()['first_frame'].setValue(sel[0]['first'].getValue())
        nuke.root()['last_frame'].setValue(sel[0]['last'].getValue())
    else:
        nuke.message("please select one node.")

def setReadFrameRange():
    """set nuke frame range according to a read node"""
    readNodes = nuke.selectedNodes("Read")
    rawInput = nuke.getInput("StartFrame-EndFrame:",str(int(nuke.root()['first_frame'].getValue()))+"-"+str(int(nuke.root()['last_frame'].getValue())))
    if rawInput:
        try:
            firstFrame = str(rawInput).split("-")[0]
            endFrame = str(rawInput).split("-")[1]
        except:
            nuke.message("Error in the typing...\nTry like this: 1001-1100")

        if readNodes and firstFrame and endFrame:
            for n in readNodes:
                n['first'].setValue(int(firstFrame))
                n['last'].setValue(int(endFrame))
                print "Read node '"+n.name()+"' is set to: "+str(firstFrame)+"-"+str(endFrame)

def setAllReadsFrameRange():
    """same as above ..."""
    p = nuke.Panel("Frame range ")
    p.addSingleLineInput("start", int(nuke.root()['first_frame'].getValue()))
    p.addSingleLineInput("end", int(nuke.root()['last_frame'].getValue()))
    hit = p.show()
    if hit :
        first = int(p.value("start"))
        last = int(p.value("end"))
        for n in nuke.allNodes("Read"):
            n['first'].setValue(first)
            n['last'].setValue(last)
            n['origfirst'].setValue(first)
            n['origlast'].setValue(last)
            print n.name(), "is set to:", firstFrame, "-", endFrame

def initAlignValues(mode):
    """align tool"""
    yMin = -100000000
    yMax = 100000000

    for node in nuke.selectedNodes():
        y = node["ypos"].value(True)
        if y < yMax:
            yMax = y
        if y > yMin:
            yMin = y

    yCenter = (yMin+yMax)/2

    if mode == "center":
        return yCenter
    if mode == "up":
        return yMax
    if mode == "down":
        return yMin

def centerAlignSelectedNodes():
    """align center"""
    yCenter = initAlignValues("center")

    for node in nuke.selectedNodes():
        node["ypos"].setValue(yCenter)

def upAlignSelectedNodes():
    """align up"""
    yMax = initAlignValues("up")

    for node in nuke.selectedNodes():
        node["ypos"].setValue(yMax)

def downAlignSelectedNodes():
    """align down"""
    yMin = initAlignValues("down")

    for node in nuke.selectedNodes():
        node["ypos"].setValue(yMin)

def hideInputs():
    """hide inputs on selection"""
    for node in nuke.selectedNodes():
        node.knob('hide_input').setValue(not node.knob('hide_input').value())
       
def toggleCamGeoDisplay():
    """toggle the display of the 3d cameras and 3d geos"""

    sel = nuke.selectedNodes()

    # on a selection
    good = []
    goodCam = ["Camera2","Camera", "hubCamera"]
    goodGeo = ["ReadGeo","ReadGeo2","Sphere","Cube","Cylinder","Card", "Card2", "Axis", "Axis2"]
    if (int(str(len(sel))))>0:
        nodes = nuke.selectedNodes()
        for node in nodes:
            if node.Class() in goodCam+goodGeo:
                if node['display'].value() == "off" :
                    if node.Class() in goodCam:
                        node['display'].setValue('wireframe')
                    if node.Class() in goodGeo:
                        node['display'].setValue('textured')
                    #node['label'].setValue("")
                    node['note_font_color'].setValue(0)
                    node['tile_color'].setValue(0)
                    print node.name()+" display on"
                else:
                    node['display'].setValue('off')
                    #node['label'].setValue("DISPLAY OFF !!!")
                    node['note_font_color'].setValue(4120346367)
                    node['tile_color'].setValue(573912575)
                    print node.name()+" display off"

            # fill good[] if there is good nodes in the selection

            if node.Class() in goodCam:
                good.append(node.name())
            if node.Class() in goodGeo:
                good.append(node.name())
        if not good:
            nuke.message("there is no camera or readGeo in the selection")

    # on all the readGeos and Cameras

    else:
        nodeL = []
        all = nuke.allNodes()
        for node in all:
            if node.Class() in goodCam+goodGeo:
                nodeL.append(node.name())
        for node in nodeL:
            if nuke.toNode(node)['display'].value() == "off":
                if nuke.toNode(node).Class() in goodCam:
                    nuke.toNode(node)['display'].setValue('wireframe')
                if nuke.toNode(node).Class() in goodGeo:
                    nuke.toNode(node)['display'].setValue('textured')
                nuke.toNode(node)['label'].setValue("")
                nuke.toNode(node)['note_font_color'].setValue(0)
                nuke.toNode(node)['tile_color'].setValue(0)
                print nuke.toNode(node).name()+" display on"
            else:
                nuke.toNode(node)['display'].setValue('off')
                nuke.toNode(node)['label'].setValue("DISPLAY OFF !!!")
                nuke.toNode(node)['note_font_color'].setValue(4120346367)
                nuke.toNode(node)['tile_color'].setValue(573912575)
                print nuke.toNode(node).name()+" display off"
           
        if not nodeL:
            nuke.message("there is no cameras or readGeos in this scene")
   
def goToFirstFrame():
    """go to first frame a la maya"""
    nuke.frame(int(nuke.root()["first_frame"].getValue()))
    
def nukePlay():
    """play a la maya"""
    nuke.activeViewer().play(1)

def setColorspace():
    """set colorspace to selection"""
    availableColorspace = 'none(raw) linear Cineon sRGB'
    panelColor = nuke.Panel('Select colorspace')
    panelColor.addEnumerationPulldown("Colorspaces", availableColorspace)

    val = panelColor.show()
    if val:
        if panelColor.value("Colorspaces") == 'none(raw)':
            for node in nuke.selectedNodes():
                try:
                    node['raw'].setValue(1)
                except:
                    print node.name(), "doesn't have colorspace..."
        else:
            for node in nuke.selectedNodes():
                try:
                    node['raw'].setValue(0)
                    node['colorspace'].setValue(panelColor.value("Colorspaces"))
                except:
                    print node.name(), "doesn't have colorspace..."

def copySpecial():
    """copy selection, paste and reconnect (just one node)"""
    depNode = nuke.dependencies(nuke.selectedNode())
    dependNode = nuke.dependentNodes(nuke.INPUTS or nuke.HIDDEN_INPUTS or nuke.EXPRESSIONS, [nuke.selectedNode()])
    i = 0
    if dependNode[0].Class() in ['Scene', 'MergeGeo']:
        i = nuke.inputs(dependNode[0])+1

    nuke.nodeCopy(nukescripts.cut_paste_file())

    for node in nuke.allNodes():
        node['selected'].setValue(0)

    nuke.nodePaste(nukescripts.cut_paste_file())

    newNode = nuke.selectedNode()
    newNode.setInput(0, depNode[0])
    dependNode[0].setInput(i+1, newNode)

def replaceStringInFile():
    """replace string in file knob"""
    sel = nuke.selectedNodes()
    pane = nuke.Panel('replace string in file knob')
    pane.addSingleLineInput('replace this', '')
    pane.addSingleLineInput('by this', '')
    val = pane.show()

    if val and sel:
        for node in sel:
            if node.Class() in ['Read', 'Write, ReadGeo2']:
                try:
                    str1 = pane.value('replace this')
                    str2 = pane.value('by this')
                    file = str(node['file'].value())
                    newfile = file.replace(str1, str2)
                    node['file'].setValue(newfile)
                except:
                    print 'failed'

def importScript():
    """import exported nuke script from maya"""
    crosswalkFile = 'mayaToNuke.info'
    if os.path.exists(crosswalkFile):
        fileInfo = open(crosswalkFile, 'r')
        text = fileInfo.readlines()
        dic = eval(text[-1])
        nkFile = dic.get('file')
        if os.path.exists(nkFile):
            print 'importing: '+nkFile
            nuke.nodePaste(nkFile)
    else:
        print 'nuke script not found...'

def replaceStereoStr(node, view):
    """used for openTerminal"""
    inputPath = node['file'].value()
    strToRemove = '%V'
    strToReplace = view
    outputPath = re.sub(strToRemove, strToReplace, inputPath)
    return outputPath

def openTerminal():
    """open a gnome-terminal with the correct job set.
     if there a read or a write node selected, it will go to the file directory"""
    sel = nuke.selectedNodes()
    job = os.environ['JOB']
    shot = os.environ['SHOT']
    discipline = os.environ['DISCIPLINE']
    jobCmd = 'source some stuff'
    if sel:
        for node in sel:
            if node.Class() in ['Read', 'Write']:
                try:
                    views = node['views'].value()
                except:
                    views = '(mono)'
                if not views in ['(mono)', 'main']:
                    panel = nuke.Panel('select view')
                    panel.addEnumerationPulldown("views", 'left right')
                    value = panel.show()
                    if value:
                        view = panel.value('views')
                        outputpath = replaceStereoStr(node, view)
                        filename = os.path.basename(outputpath)
                        path = os.path.dirname(outputpath)
                        title = path.split('/')[-1]+'/'+filename
                        os.system('gnome-terminal --title '+title+' -x csh -c "'+jobCmd+';cd '+path+';csh"&')
                        
                else:
                    filename = os.path.basename(node['file'].value())
                    path = os.path.dirname(node['file'].value())
                    title = path.split('/')[-1]+'/'+filename
                    os.system('gnome-terminal --title '+title+' -x tcsh -c "'+jobCmd+';cd '+path+';tcsh"&')
    else:
        os.system('gnome-terminal --title '+job+'--'+shot+' -x tcsh -c "'+jobCmd+';tcsh"&')

def getLatestAutosave():
    """returns the latest autosave nuke script"""
    nukeAutoSavePath = nuke.toNode("preferences").knob('AutoSaveName').evaluate()
    if os.exists(nukeAutoSavePath):
        latestAutosave = cmd.getstatusoutput('ls -1tr '+nukeAutoSavePath+' | tail -1')[1]
        latestAutosavePy = latestAutosave.split('.')[0]+'.nk'
        cmd.getstatusoutput('cp '+nukeAutoSavePath+latestAutosave+' '+nukeAutoSavePath+latestAutosavePy)
        return nukeAutoSavePath+latestAutosavePy
    else:
        pass

def showModules():
    """this is a simple function to print all the modules available in nuke"""
    keys, values = sys.modules.keys(), sys.modules.values()
    keys.sort()
    modulesList = ''
    for key in keys:
        modulesList += key+' '

    panel = nuke.Panel('python modules list')
    panel.addEnumerationPulldown('available modules', modulesList)
    val = panel.show()
    if val == 1:
        moduleToLoad = panel.value('available modules')
        panelA = nuke.Panel('module selected')
        panelA.addNotepad('module:', str(sys.modules[moduleToLoad]))
        panelA.addBooleanCheckBox('load/reload the module', 0)
        val = panelA.show()
        if val == 1:
            if panelA.value('load/reload the module') == 1:				
                print 'loading module '+moduleToLoad
                exec('import '+moduleToLoad)
                exec('reload('+moduleToLoad+')')

def reloadReadNodes():
    """hit the reload button if possible"""
    for node in nuke.selectedNodes():
        try:
            node['reload'].execute()
        except:
            pass

def togglePostageStamps():
    """toggle the poststamps on the read nodes"""
    for node in nuke.allNodes('Read'):
        node['selected'].setValue(True)
        nukescripts.toggle("postage_stamp")
        node['selected'].setValue(False)

def flipViewer():
    """input process to flip the viewer"""
    allV = nuke.allNodes('Viewer')
    pV = allV[0]
    List = nuke.selectedNodes()
    nuke.selectAll()
    nuke.invertSelection()
    try:
        n = nuke.toNode('VIEWER_INPUT')
        if n.Class() == 'Mirror':
            n['Horizontal'].setValue(not n['Horizontal'].value())
            for i in allV:
                i['input_process'].setValue(not n['Vertical'].value() + n['Horizontal'].value() == 0)
            if n['Vertical'].value() + n['Horizontal'].value() == 0:
                nuke.delete(n)
            nuke.selectAll()
            nuke.invertSelection()
        else:
            nuke.message("Another Viewer Input already exists.\nAborting to avoid conflict")
        for i in List:
            i['selected'].setValue(True)
        
    except:
        n = nuke.Node('Mirror', inpanel=False)
        n['xpos'].setValue(pV.xpos()+150)
        n['ypos'].setValue(pV.ypos())
        n['name'].setValue('VIEWER_INPUT')
        n['hide_input'].setValue(1)
        n['Horizontal'].setValue(not n['Horizontal'].value())
        nuke.selectAll()
        nuke.invertSelection()
        for i in List:
            i['selected'].setValue(True)

def flopViewer():
    """input process to flop the viewer"""
    allV = nuke.allNodes('Viewer')
    pV = allV[0]
    List = nuke.selectedNodes()
    nuke.selectAll()
    nuke.invertSelection()
    try:
        n = nuke.toNode('VIEWER_INPUT')
        if n.Class() == 'Mirror':
            n['Vertical'].setValue(not n['Vertical'].value())
            for i in allV:
                i['input_process'].setValue(not n['Vertical'].value() + n['Horizontal'].value() == 0)
            if n['Vertical'].value() + n['Horizontal'].value() == 0:
                nuke.delete(n)
            nuke.selectAll()
            nuke.invertSelection()
        else:
            nuke.message("Another Viewer Input already exists.\nAborting to avoid conflict")
        
    except:
        n = nuke.Node('Mirror',inpanel=False)
        n['xpos'].setValue(pV.xpos()+150)
        n['ypos'].setValue(pV.ypos())
        n['name'].setValue('VIEWER_INPUT')
        n['hide_input'].setValue(1)
        n['Vertical'].setValue(not n['Vertical'].value())
        nuke.selectAll()
        nuke.invertSelection()
        for i in List:
            i['selected'].setValue(True)
    for i in List:
        i['selected'].setValue(True)
    
def gl_lighting():
    """switch the global lighting on a 3d viewer"""
    for viewer in nuke.allNodes('Viewer'):
        val = int(viewer.knob('gl_lighting').getValue())
        viewer.knob('gl_lighting').setValue(not val)
        
def viewerSettings():
    """set some default values on the viewer"""
    node = nuke.thisNode()
    print "set default value on", node.name()
    node.knob('near').setValue(100)
    node.knob('far').setValue(500000)
    node.knob('grid_display').setValue(False)
    node.knob('gl_lighting').setValue(1)

def nukeExecute():
    """try to execute (reload, render) the selected nodes"""
    if nuke.selectedNodes():
        for node in nuke.selectedNodes():
            try:
                node.knob('Render').execute()
            except:
                pass
            try:
                node.knob('reload').execute()
            except:
                pass

def checkAlpha():
    """check the alpha channel"""
    node = nuke.thisNode()
    file_type = node.knob('file_type').value()
    channels = node.knob('channels').value()
    renderFormat = node.knob('renderFormat')
    if renderFormat:
        if file_type == 'dpx':
            node.knob('channels').setValue('rgb')
        if not renderFormat.value() == 'dpx' and not file_type == 'dpx' and not channels == 'all':
            node.knob('channels').setValue('rgba')
    else:
        if file_type == 'dpx':
            node.knob('channels').setValue('rgb')
        if not file_type == 'dpx' and not channels == 'all':
            node.knob('channels').setValue('rgba')
            
def createViewerInput():
    """create the color check node"""
    if 'VIEWER_INPUT' not in [node.name() for node in nuke.allNodes()]:
        for node in nuke.allNodes():
            node['selected'].setValue(False)
        nuke.createNode("dmpViewerInput")
        node = nuke.toNode('VIEWER_INPUT')
        node.showControlPanel()
        node['selected'].setValue(False)
    else:
        nuke.toNode('VIEWER_INPUT').showControlPanel()
        #nuke.delete(nuke.toNode('VIEWER_INPUT'))

def printNodeKnobsExpressions():
    """return nodes that have expression and the expression"""
    nodes = {}
    for node in nuke.allNodes():
        nodes[node] = {}
        for knob in node.knobs():
            if node[knob].hasExpression():
                nodes[node][knob] = node[knob].animation(0).expression()
                print node[knob].name(), node.name(), True, node[knob].toScript(), node[knob].animation(0).expression()
    return nodes
    
# ======================
# CALLBACKS
# ======================

def viewerSettings():#
    """set default values at the creation of a viewer node"""
    nuke.callbacks.addOnCreate(viewerSettings, args=(), kwargs={}, nodeClass='Viewer')
    
def autoCheckAlpha():
    """auto check the alpha channel at the creation of write nodes"""
    nuke.callbacks.addOnUserCreate(checkAlpha, args=(), kwargs={}, nodeClass='Write')
    
def addFrameRangeOverride():
    """auto add the frame range override tab on write nodes"""
    nuke.callbacks.addOnUserCreate(frameRangeOverrideTab, args=(), kwargs={}, nodeClass='Write')

# end
