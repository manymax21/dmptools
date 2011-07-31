'''
custom commands and tools for nuke
michael-ha@moving-picture.com
'''

import nuke
import nukescripts
import re
import os
import commands as cmd
import sys
import time

def setShotFrameRange():

	shot = os.environ['SHOT']
	scene = os.environ['SCENE']
	frameRange = hubUtils.getShotTimeRangeInfo(shot, scene, hubUtils.HubShotTimeRange.WORKING)['workFrameRange']
	try:
		nuke.toNode('root')['first_frame'].setValue(frameRange[0])
		nuke.toNode('root')['last_frame'].setValue(frameRange[1])
	except:
		print 'failed to get a correct frame range:\n'+shot+' : '+frameRange
		nuke.message('failed to get a correct frame range:\n'+shot+' : '+frameRange)

def nukeToFramecycler():									# run framecycler from a read or write. can do a comparision of two nodes.
    
    nodes = nuke.selectedNodes()
    
    if len(nodes) == 1:
        if nodes[0].Class() != "Read" and nodes[0].Class() != "Write":
            nuke.message("Your selection ("+nodes[0].name()+" : "+nodes[0].Class()+") is not a read or a write node.")
        else:
            sequence1 = nodes[0]['file'].value()
            sequence1 = re.sub('%0[0-9i]d', '#' , sequence1)
    
            #build and run the system command                            
            fcCommand = "framecycler " +sequence1+" &"
            os.system(fcCommand)

    if len(nodes) == 2:
        if nodes[0].Class() != "Read" and nodes[0].Class() != "Write" or nodes[1].Class() != "Read" and nodes[1].Class() != "Write":
            nuke.message("One of the nodes ("+nodes[0].name()+" : "+nodes[0].Class()+" or "+nodes[1].name()+" : "+nodes[1].Class()+") you have selected is not a read or a write node")
        else:
            sequence1 = nodes[0]['file'].value()
            sequence1 = re.sub('%0[0-9i]d', '#' , sequence1)
        
            sequence2 = nodes[1]['file'].value()
            sequence2 = re.sub('%0[0-9i]d', '#' , sequence2)
            
            #build and run the system command                            
            fcCommand = "framecycler A[ "+sequence1+" ]A B[ "+sequence2+" ]B &"
            os.system(fcCommand)

    if len(nodes) != 1 and len(nodes) != 2:
        nuke.message("You need to select one or two read or write node...")

def clearAnim():											# clear animation of all the knobs in the selected nodes

    for node in nuke.selectedNodes():
        #----------- ROTOPAINT SPECIAL---------------------#
        if node.Class() == "RotoPaint":
            rotoCurves = node['curves']
            for knob in node.knobs():
                if nuke.Knob.isAnimated(node[knob]):
                    nuke.Knob.clearAnimated(node[knob])            
                    print "clearing animation of: "+node.name()+" "+node[knob].name()
        #---------------OTHER NODES------------------#
        else:
             for knob in node.knobs():
                if nuke.Knob.isAnimated(node[knob]):
                    nuke.Knob.clearAnimated(node[knob])            
                    print "clearing animation of: "+node.name()+" "+node[knob].name()

def bclone():												# create a transparent clone to clean the node tree
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


def connectSel():											# connect 1 source ->  multiple target
    sel = nuke.selectedNodes()
    sel1 = sel[-1]
    sel.remove(sel1)
    for node in sel:
        node.setInput(0,sel1)

def setDisplayWireframe():								# set all 3d to wireframe mode
	for node in nuke.allNodes():
		goodGeo = ["ReadGeo","ReadGeo2","Sphere","Cube","Cylinder","Card", "Card2"]
		if node.Class() in goodGeo:
			node['display'].setValue(1)

def setDisplayShaded():									# set all 3d to shaded mode
	for node in nuke.allNodes():
		goodGeo = ["ReadGeo","ReadGeo2","Sphere","Cube","Cylinder","Card", "Card2"]
		if node.Class() in goodGeo:
				node['display'].setValue(2)
				
def setDisplayTextured():									# set all 3d to textured mode
	for node in nuke.allNodes():
		goodGeo = ["ReadGeo","ReadGeo2","Sphere","Cube","Cylinder","Card", "Card2"]
		if node.Class() in goodGeo:
				node['display'].setValue(4)

def setDisplayTexturedLines():								# set all 3d to textured mode
	for node in nuke.allNodes():
		goodGeo = ["ReadGeo","ReadGeo2","Sphere","Cube","Cylinder","Card", "Card2"]
		if node.Class() in goodGeo:
				node['display'].setValue(5)

def setFrameRangeFromSel():								# set the ti;meline with the handles of the selected node.
	sel = nuke.selectedNodes()
	if sel:
		nuke.root()['first_frame'].setValue(sel[0]['first'].getValue())
		nuke.root()['last_frame'].setValue(sel[0]['last'].getValue())
	else:
		nuke.message("please select one node.")

def setReadFrameRange():								# set frame range according to a read node (2def)
    sel = nuke.selectedNodes("Read")
    rawInput = nuke.getInput("StartFrame-EndFrame:",str(int(nuke.root()['first_frame'].getValue()))+"-"+str(int(nuke.root()['last_frame'].getValue())))
    if rawInput:
        try:
            firstFrame = str(rawInput).split("-")[0]
            endFrame = str(rawInput).split("-")[1]
        except:
            nuke.message("Error in the typing...\nTry like this: 1001-1100")

        if sel and firstFrame and endFrame:
            for n in sel:
                n['first'].setValue(int(firstFrame))
                n['last'].setValue(int(endFrame))
                print "Read node '"+n.name()+"' is set to: "+str(firstFrame)+"-"+str(endFrame)
        else:
            for n in nuke.allNodes("Read"):
                n['first'].setValue(int(firstFrame))
                n['last'].setValue(int(endFrame))
            print "All Read Nodes are set to: "+str(firstFrame)+"-"+str(endFrame)


def setAllReadsFrameRange():
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
        print "All Read Nodes are set to: "+str(firstFrame)+"-"+str(endFrame)

def initAlignValues(mode):									# align tool (4def)
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
	yCenter = initAlignValues("center")
	
	for node in nuke.selectedNodes():
		node["ypos"].setValue(yCenter)


def upAlignSelectedNodes():
	yMax = initAlignValues("up")
	
	for node in nuke.selectedNodes():
		node["ypos"].setValue(yMax)

def downAlignSelectedNodes():
	yMin = initAlignValues("down")
	
	for node in nuke.selectedNodes():
		node["ypos"].setValue(yMin)

def renameLabel():										# rename label according to the dependance node
    sel=nuke.selectedNodes()
    if sel:
        for node in sel:
            try:
                if not nuke.dependencies(node)[0]['label'].value():
                    node['label'].setValue(nuke.dependencies(node)[0].name())
                else:
                    node['label'].setValue(nuke.dependencies(node)[0]['label'].value())

                if node.Class() == "Dot":
                    parentColor = int(nuke.dependencies(node)[0]['tile_color'].getValue())
                    node['tile_color'].setValue(parentColor)
                    node['note_font_size'].setValue(15)
                    node['note_font_color'].setValue(parentColor)
            except:
                print "Needs connected Nodes !"
def listKnobs():											# prints all available knobs in the selected node. print also its actual value 

    sel = nuke.selectedNodes()

    if (int(str(len(sel))))==1:
        for knob in sel[0].knobs():
        	print '*************************', ' ', knob.upper(), ' KNOB', '*************************', '\n'
        	print "Knob Name: ", knob
        	print "Knob Value: ", sel[0].knob(knob).value()

    else:
        nuke.message("please select one node")
def hideInputs():											# hide inputs on selection
    for node in nuke.selectedNodes():
       node.knob('hide_input').setValue(not node.knob('hide_input').value())
       
def toggleCamGeoDisplay():								#toggle the display of the 3d cameras and 3d geos

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
   
def goToFirstFrame():										# go to first frame
	nuke.frame(int(nuke.root()["first_frame"].getValue()))
def nukePlay():											# play
	nuke.activeViewer().play(1)
	
def setColorspace():										# set colorspace to selection
	
	availableColorspace = 'none(raw) linear Cineon sRGB MPC_Cineon'
	panelColor = nuke.Panel('Select colorspace')
	panelColor.addEnumerationPulldown("Colorspaces", availableColorspace)
	
	val = panelColor.show()
	if val:
		if panelColor.value("Colorspaces") == 'none(raw)':
			for node in nuke.selectedNodes():
				node['raw'].setValue(1)
		else:
			for node in nuke.selectedNodes():
				node['raw'].setValue(0)
				node['colorspace'].setValue(panelColor.value("Colorspaces"))
				
def copySpecial():										# copy selection, paste and reconnect (just one node)
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

def switchCrop():											# switch the viewerInput crop
	try:
		job = os.environ['JOB']
	except:
		job = None
	
	jobs = ['ia', 'et1', 'et2', 'p4']
	
	if job in jobs:
		viewer = nuke.ViewerProcess.node()
		crops = ['1.66','1.78','1.85','2.35','Off']
		s = viewer['viewerCrop'].value()
		cropIndex = crops.index(s)
		try:
			viewer['viewerCrop'].setValue(crops[cropIndex+1])
			cropIndex +=1

		except:
			viewer['viewerCrop'].setValue(crops[0])    
			cropIndex +=1
	else:
		print "this script don't have the crop option. abort..."

def switchUV_PROJ():										# switch all the switch nodes from 0 to 1
	for node in nuke.allNodes('Switch'):
		if node.name().split('_')[-1] == 'uvproj':
			if int(node['which'].value()) == 0:
				node['which'].setValue(1)
				#node['label'].setValue('PROJ !')
				node['tile_color'].setValue(713403391)
				#print 'set all the switch named *_uvproj to PROJ'
			else:
				node['which'].setValue(0)
				#node['label'].setValue('UV !')
				node['tile_color'].setValue(2878620927)
				#print 'set all the switch named *_uvproj to UV'

def createReadFromWrite():								# create read from write

	writeNodes = nuke.selectedNodes('Write')

	def readFromWrite(node):
		file = node['file'].value()
		name = node.name()
		colorSpace = node['colorspace'].value()
		read = nuke.createNode('Read', inpanel = False)
		
		read['file'].setValue(file)
		read['name'].setValue('read_'+name)
		read['colorspace'].setValue(colorSpace)


	for node in writeNodes:
		readFromWrite(node)
		

def replaceStringInFile():									# replace string in file knob
	
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
					actualVal = str(node['file'].value())
					node['file'].setValue(actualVal.replace(str1, str2, 1))
				except:
					print 'failed'

def setSelWriteActive():
	sel = nuke.selectedNode()

	for node in nuke.allNodes('Write'):
		node['disable'].setValue(1)

	sel['disable'].setValue(0)


def setAllReadToRaw():
	for node in nuke.allNodes('Read'):
		if node['colorspace'].value() == 'sRGB' and node['raw'].value() == False:
			node['raw'].setValue(1)
		else:
			node['raw'].setValue(0)
def importScript():
	crosswalkFile = '/tmp/mayaToNuke.info'
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

def openTerminal():										# open a gnome-terminal with the correct job set. if there a read or a write node selected, it will go to the file directory
	sel = nuke.selectedNodes()
	job = os.environ['JOB']
	shot = os.environ['SHOT']
	discipline = os.environ['DISCIPLINE']
	jobCmd = 'source /usr/people/$USER/.cshrc;source /usr/people/$USER/.tcshrc;source $TOOLS/scripts/job.csh; job -d '+discipline+' '+job+' '+shot
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

def replaceStereoStr(node, view):
	inputPath = node['file'].value()
	strToRemove = '%V'
	strToReplace = view
	outputPath = re.sub(strToRemove, strToReplace, inputPath)
	return outputPath

def graffiti():
	'launch the graffiti in nuke'
	
	os.system('graffiti&')
	
def getLatestAutosave():

	nukeautosavePath = '/disk1/nuke/'+os.environ['USERNAME']+'/autosave/'
	latestAutosave = cmd.getstatusoutput('ls -1tr '+nukeautosavePath+' | tail -1')[1]
	latestAutosavePy = latestAutosave.split('.')[0]+'.nk'
	cmd.getstatusoutput('cp '+nukeautosavePath+latestAutosave+' '+nukeautosavePath+latestAutosavePy)
	return nukeautosavePath+latestAutosavePy

def getLatestUserSave():
	
	os.environ['USER'], 
	user, job, shot, scene = os.environ['USER'], os.environ['JOB'], os.environ['SHOT'], os.environ['SCENE']
	nukeUserPath = '/jobs/'+job+'/'+shot+'/nuke/scenes/'+user+'/'
	latestNukeScript = cmd.getstatusoutput('ls -1tr '+nukeUserPath+' | tail -1')[1]
	return nukeautosavePath+latestAutosavePy


def showModules():

	'this is a simple function to print all the modules available in nuke'

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
	
	for node in nuke.selectedNodes():
		if node.Class() in ['Read', 'ReadGeo', 'ReadGeo2']:
			node['reload'].execute()
		
def reloadAllReadNodes():
	
	for node in nuke.allNodes('Read'):
		node['reload'].execute()

def togglePostageStamps():
	for node in nuke.allNodes('Read'):
		node['selected'].setValue(True)
		nukescripts.toggle("postage_stamp")
		node['selected'].setValue(False)
		
def flipViewer():
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
	
	for viewer in nuke.allNodes('Viewer'):
		val = int(viewer.knob('gl_lighting').getValue())
		viewer.knob('gl_lighting').setValue(not val)

def openHubViewer():

	job = os.environ['JOB']
	shot = os.environ['SHOTNAME']
	scene = os.environ['SCENE']

	panel = nuke.Panel('Open hubViewer:')
	panel.addSingleLineInput('Shot:', shot)
	val = panel.show()
	if val:
		
		shot = panel.value('Shot:')
		scene = shot.split('_')[0]+'_'+shot.split('_')[1]
		os.system('firefox -new-window http://hub.mpc.local/FileRoot/software/tools/web/hubViewerSecure/hubViewer.php?job='+job+' &')
		time.sleep(2)
		os.system('firefox -new-tab http://hub.mpc.local/FileRoot/software/tools/web/hubViewerSecure/2.17/php/hubDailies.php?drawMode=mosaic\&view=server\&scene='+scene+'\&shot='+shot+' &')

'''
# ratio calculator

camera = nuke.selectedNodes()[1]
image = nuke.selectedNodes()[0]
goodCam = ['Camera', 'Camera2', 'hubCamera']
good2D = ['Read']
if camera.Class() in goodCam and image.Class() in good2D:
    x, y = image.width(), image.height()
    imageratio = float(x)/float(y)
    h,v = camera.knob('haperture').getValue(), camera.knob('vaperture').getValue()
    cameraratio = h/v
    if not round(imageratio) == round(cameraratio):
        print imageratio, cameraratio
        print h/imageratio
    else:
        print 'the ratio are the same'
'''