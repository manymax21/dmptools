import os
import time
import commands
import nuke
import nukescripts
import mpc.jobtools.jobtools as jobtools
import hubUtils

class nukeSequenceManager:	
	def __init__(self):
		
		self.node = nuke.thisNode()
		self.job = jobtools.jobName()
		self.scene = jobtools.sceneName()
		self.shot = jobtools.shotName()
		
		# get some nodes inside the group
		
		self.scene3D = nuke.toNode('scene')
		self.cameraSwitch = nuke.toNode('cameraSwitch')
		
	def refresh(self):
		
		# it's like a second init
		
		scene = self.refreshScenes()[1]
		
		self.node.knob('jobname').setValue("<FONT COLOR=\"#33EE5E\">"+self.job+" "+scene+"<\FONT>")
		self.node.knob('label').setValue("[python os.getenv('JOB')] - [python os.getenv('SCENE')]/[python os.getenv('SHOTNAME')]")
		
		knobChangeCallback()
		

	def refreshScenes(self):
		
		scenes = list(jobtools.scenesList(self.job).columns()['name'])
		scenes.sort()		
		self.node.knob('sceneList').setValues(scenes)
		self.node.knob('sceneList').setValue(self.scene)
		scene = self.node.knob('sceneList').value()
		
		self.refreshShots(scene)
		
		return scenes, scene

	def refreshShots(self, scene):
		
		try:
			shots = list(jobtools.shotsList(self.job, scene).columns()['name'])
			shots.sort()
		
		except:
			shots = ['n/a']
			
		self.node.knob('shotlist').setValues(shots)
		self.node.knob('shotlist').setValue(self.shot)
		
		return shots
		
	def clearSequenceManager(self):

		confirm = nuke.ask('Are you sure ?')
		
		if confirm:
			
			self.node.knob('sceneList').setValues(['n/a'])
			self.node.knob('sceneList').setValue(0)
			self.node.knob('shotlist').setValues(['n/a'])
			self.node.knob('shotlist').setValue(0)
			self.node.knob('jobname').setValue('n/a')
			self.node.knob('label').setValue('')
			#self.node.knob('cameraName').setValue(' ')
			shots = self.node.knob('shotList').values()
			
			self.removeAllShots(shots)
		
	def createShot(self, scene, shot):
		
		# create shot entry if not 'n/a' and doesn't already exists
		if not self.node.knob('grpS_'+shot) and not shot == 'n/a':
			
			#self.deselectAllNodesInGroup()
			
			# get the current properties bin pref
			binVal = int(nuke.toNode("preferences").knob('newPanelsInBin').getValue())
			# set it to 2
			nuke.toNode("preferences").knob('newPanelsInBin').setValue(2)
			
			shots = ' '.join(self.node.knob('shotList').values())
			self.node.knob('shotList').setValues((shots+' '+shot).split(' '))
			timeRange = hubUtils.getShotTimeRangeInfo(shot, scene, hubUtils.HubShotTimeRange.WORKING)['workFrameRange']
			
			#create knobs to add
			hubViewerButton = nuke.PyScript_Knob('hubViewer_'+shot, 'hubViewer')
			hubViewerButton.setFlag(nuke.STARTLINE)
			cmd = "import os\n"
			cmd += "import time\n"
			cmd += "job = nuke.thisNode().knob('jobname').value().split('>')[1].split(' ')[0]\n"
			cmd += "shot = nuke.thisKnob().name()[10:]\n"
			cmd += "scene = shot.split('_')[0]+'_'+shot.split('_')[1]\n"
			cmd += "os.system('firefox -new-window http://hub.mpc.local/FileRoot/software/tools/web/hubViewerSecure/hubViewer.php?job='+job+' &')\n"
			cmd += "time.sleep(2)\n"
			cmd += "os.system('firefox -new-tab http://hub.mpc.local/FileRoot/software/tools/web/hubViewerSecure/2.17/php/hubDailies.php?drawMode=mosaic\&view=server\&scene='+scene+'\&shot='+shot+' &')"
			hubViewerButton.setCommand(cmd)
			
			grpS = nuke.Tab_Knob("grpS_"+shot, shot, nuke.TABBEGINGROUP)
			grpE = nuke.Tab_Knob("grpE_"+shot, shot, nuke.TABENDGROUP)
			text = nuke.Text_Knob('txt_'+shot, '', "handles: <FONT COLOR=\"#7777EE\">"+timeRange+"<\FONT>")
			text.setFlag(nuke.ENDLINE)
			setButton = nuke.PyScript_Knob('set_'+shot, 'set')
			setButton.setFlag(nuke.ENDLINE)
			cmd = "node = nuke.thisNode()\nshot = nuke.thisKnob().name()[4:]\nexecfile('/usr/people/michael-ha/python/env/nukeSequenceManager.py')\nnukeSequenceManager().setShot(shot)"
			setButton.setCommand(cmd)

			delButton = nuke.PyScript_Knob('del_'+shot, 'delete')
			delButton.setFlag(nuke.ENDLINE)
			cmd = "node = nuke.thisNode()\nshot = nuke.thisKnob().name()[4:]\nexecfile('/usr/people/michael-ha/python/env/nukeSequenceManager.py')\nnukeSequenceManager().removeShot(shot)"
			delButton.setCommand(cmd)
			
			# create hubCamera
			if self.node.knob('createCamera').getValue() == 1:
				hubCamera = self.createHubCamera()
				self.setHubCamera(hubCamera, scene, shot)
			
				version = hubCamera.knob('versionHub').value()
				versiontxt = nuke.Text_Knob('version'+shot, '', "cam version: <FONT COLOR=\"#7777EE\">"+version+"<\FONT>")
				versiontxt.setFlag(nuke.ENDLINE)
			
			# add knobs to node
			self.node.addKnob(grpS)
			if self.node.knob('createCamera').getValue() == 1:
				self.node.addKnob(versiontxt)
			self.node.addKnob(text)
			self.node.addKnob(hubViewerButton)
			self.node.addKnob(setButton)
			self.node.addKnob(delButton)
			self.node.addKnob(grpE)

			# set it back to the original value
			nuke.toNode("preferences").knob('newPanelsInBin').setValue(binVal)
			
			if self.node.knob('createCamera').getValue() == 1:			
				self.setShot(shot)			
				
		else:
			nuke.message('the shot '+shot+' already exists')
		
	def createHubCamera(self):
	
		cmd = "import mpc.nuke.hubCamera.hubCameraUtils as mCamUtils; mCamUtils.createHubCamera()"
		exec(cmd)
		camera = nuke.selectedNode()
		self.scene3D.setInput(self.scene3D.inputs()+1, camera)
		camera.knob('selected').setValue(False)
		
		return camera
			
	def setHubCamera(self, hubCamera, scene, shot):
		
		hubCamera.setName(self.job+'_'+shot+'_renderCamera')
		
		for n in hubCamera.knobs():

			if n == 'sceneHub':
				hubCamera.knob('sceneHub').setValue(scene)
				t = nuke.threading.Timer(0.2, self.forceLoad, [hubCamera])
				t.start()
				
			if n == 'shotHub':
				hubCamera.knob('shotHub').setValue(shot)
				t = nuke.threading.Timer(0.2, self.forceLoad, [hubCamera])
				t.start()
				
			if n == 'versionHub':
				
				hubCamera.knob(n).setValue(hubCamera.knob(n).numValues()-1)

				t = nuke.threading.Timer(0.2, self.forceLoad, [hubCamera])
				t.start()

		refreshcmd = "execfile('/usr/people/michael-ha/python/env/nukeSequenceManager.py')\nnukeSequenceManager().refreshLists()"
		#exec(refreshcmd)	

	def forceLoad(self, hubCamera):
		
		#Hack to fore the load on the enum change
		val = not hubCamera.knob('useCache').value()
		nukescripts.utils.executeInMainThreadWithResult(hubCamera.knob('useCache').setValue, val )

	def setShot(self, shot):
		
		try:
			scene = str(shot.split("_")[0])+"_"+str(shot.split("_")[1])
		except:
			scene = 'n/a'
		
		if not shot == 'n/a':
			
			try:
				#cameraGrp = self.node.knob("grpS_"+shot)
				camera = nuke.toNode(self.job+'_'+shot+'_renderCamera')
				#self.node.knob('cameraName').setValue(shot)
			except:
				pass
			try:
				version = camera.knob('versionHub').value()
			except:
				version = 'n/a'
			try:
				self.cameraSwitch.setInput(0, camera)
			except:
				pass
		
		if shot == 'n/a':
			version = 'n/a'
			#self.cameraSwitch.setInput(0)
			
		self.node.knob('shotList').setValue(shot)
		
		#set the timerange
		timeRange = hubUtils.getShotTimeRangeInfo(shot, scene, hubUtils.HubShotTimeRange.WORKING)['workFrameRange']
		
		if timeRange in ['n/a', 'n/a ', 'n/a - n/a', 'n/a-n/a']:
			try:
				camera = nuke.toNode(self.job+'_'+shot+'_renderCamera')
				label = camera.knob('label').value()
				if label:
					timeRange = str(label)
			except:
				pass
		try:
			self.node.knob('actualCamera').setValue("<FONT COLOR=\"#7777EE\"> v"+version+" :   "+timeRange+"<\FONT>")
			self.node.knob('txt_'+shot).setValue("handles: <FONT COLOR=\"#7777EE\">"+timeRange+"<\FONT>")
		except:
			pass
			
		if not timeRange in ['n/a', 'n/a ', 'n/a - n/a', 'n/a-n/a']:

			firstFrame, lastFrame = timeRange.split('-')[0], timeRange.split('-')[1]
			
			if not firstFrame == 'n/a' and not lastFrame == 'n/a':
				
				# set root frame range
				nuke.root().knob('first_frame').setValue(int(firstFrame))
				nuke.root().knob('last_frame').setValue(int(lastFrame))
				# if the current frame is not in the frame range set frame at the begining of the shot
				if nuke.frame() not in range(int(firstFrame), int(lastFrame)):
					nuke.frame(int(firstFrame))
			
	
	def removeShot(self, shot):
		
		# try to delete knobs
		grpS = self.node.knob("grpS_"+shot)
		grpE = self.node.knob("grpE_"+shot)
		txt = self.node.knob("txt_"+shot)
		setButton = self.node.knob('set_'+shot)
		delButton = self.node.knob('del_'+shot)
		versiontxt = self.node.knob('version'+shot)
		shots = self.node.knob('shotList').values()
		hubButton = self.node.knob('hubViewer_'+shot)
		
		try:
			shots.remove(shot)
		except:
			pass

		# try to delete knobs, cam and grps
		try:
			self.removeknob(self.node, grpS)
			self.removeknob(self.node, grpS)
			self.removeknob(self.node, grpE)
			self.removeknob(self.node, txt)
			self.removeknob(self.node, setButton)
			self.removeknob(self.node, delButton)
			self.removeknob(self.node, versiontxt)
			self.removeknob(self.node, hubButton)
			
			try:
				cam = nuke.toNode(self.job+'_'+shot+'_renderCamera')
				nuke.delete(cam)
			except:
				print 'camera '+shot+' not found...'
			
			
			self.node.knob('shotList').setValues(shots)
			
			nuke.callbacks.removeKnobChanged(knobChange, args=(), kwargs={}, nodeClass = 'Group')
		
		except:
			pass
			
	def removeknob(self, node, knob):
		
		try:
			node.removeKnob(knob)
		except:
			print 'knob to remove not found...'
	
	def deselectAllNodesInGroup(self):
		
		for node in nuke.allNodes():
		    node.knob('selected').setValue(0)

	def removeAllShots(self, shots):

		for shot in shots:
			try:
				self.removeShot(shot)
			except:
				continue

		self.node.knob('shotList').setValues(['n/a'])
		self.node.knob('shotList').setValue(0)
		self.node.knob('actualCamera').setValue('n/a')

	def alfredRender(self):
		
		self.node.end()
		
		for node in nuke.allNodes():
			node.knob('selected').setValue(0)
			
		for write in nuke.allNodes('Write'):
			write.knob('disable').setValue(1)
		
		self.node.begin()
		
		writeRender = nuke.toNode('WriteShot')
		writeRender.knob('selected').setValue(1)
		#nuke.show(writeRender)
		
		# alfred render luncher

		currTime = str(time.strftime('%d%m%y_%H%M%S'))
		nuke.scriptSave('')
		nukeScene = nuke.toNode('root').name()
		fileDir = os.path.dirname(nukeScene)+'/'

		panel = nuke.Panel('Alfred batch render')
		panel.addSingleLineInput('frame range', str(int(nuke.root()['first_frame'].getValue()))+','+str(int(nuke.root()['last_frame'].getValue())))
		val = panel.show()
		if val ==1:
			frameRange = panel.value('frame range')
			
			for write in nuke.allNodes('Write'):
				write.knob('disable').setValue(1)
			
			writeRender.knob('disable').setValue(0)

			renderScene = fileDir+'.'+os.path.basename(nukeScene).split('.')[0]+'_alfredrender_'+writeRender.name()+'_'+currTime+'.nk'
			nuke.scriptSaveAs(renderScene, overwrite = 1)
			
			print 'sending '+renderScene+' to Alfred ...'
			#nuke.tcl('exec rnuke "'+renderScene+'" '+frameRange+' &;')
			os.popen('rnuke '+renderScene+' '+frameRange+' &')
			
			for write in nuke.allNodes('Write'):
				write.knob('disable').setValue(0)
			
			nuke.scriptSaveAs(nukeScene, overwrite = 1)
			
		else:
			print 'abort...'
			
		#self.node.end()

# camera callback

def knobChange():
	G = nuke.thisNode()
	K = nuke.thisKnob()
	
	if K.name() == 'shotList':
		try:
			shot = K.value()
			nukeSequenceManager().setShot(shot)
		except:
			pass
			
	if K.name() == 'sceneList':
		try:
			scene = K.value()
			nukeSequenceManager().refreshShots(scene)
			G.knob('jobname').setValue("<FONT COLOR=\"#33EE5E\">"+os.getenv('JOB')+" "+scene+"<\FONT>")
			G.knob('label').setValue("[python os.getenv('JOB')] - [python os.getenv('SCENE')]/[python os.getenv('SHOTNAME')]")
		except:
			pass

def knobChangeCallback():
	nuke.callbacks.addKnobChanged(knobChange, args=(), kwargs={}, nodeClass = 'Group')

if __name__ == "__main__":
	sequenceManager = nukeSequenceManager()