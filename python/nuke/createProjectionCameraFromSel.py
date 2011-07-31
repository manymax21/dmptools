import nuke

class renderCamToProj():
	
	def __init__(self):
		
		try:
			self.basecamera = nuke.selectedNode()
		except:
			self.basecamera = None
			
		self.frame = nuke.frame()
		
		if self.basecamera and self.basecamera.Class() in ['Camera', 'Camera2', 'hubCamera']:
			
			self.basecamera.knob('selected').setValue(0)
			trOrder, rotOrder, trX, trY, trZ, rX, rY, rZ, focal, hap, vap, near, far= self.getHubCameraKnobs(self.basecamera, self.frame)
			projCamera = self.createProjectionCamera(self.basecamera, self.frame, trOrder, rotOrder, trX, trY, trZ, rX, rY, rZ, focal, hap, vap, near, far)
			
		else:
			nuke.message("please select a render camera ('Camera', 'Camera2', 'hubCamera')")
		
	def getHubCameraKnobs(self, basecamera, frame):

		trOrder, rotOrder = basecamera.knob('xform_order').value(), basecamera.knob('rot_order').value()

		trX, trY, trZ = float(basecamera.knob('translate').getValueAt(frame)[0]), float(basecamera.knob('translate').getValueAt(frame)[1]), float(basecamera.knob('translate').getValueAt(frame)[2])
		rX, rY, rZ = float(basecamera.knob('rotate').getValueAt(frame)[0]), float(basecamera.knob('rotate').getValueAt(frame)[1]), float(basecamera.knob('rotate').getValueAt(frame)[2])
		
		focal, hap, vap = float(basecamera.knob('focal').getValueAt(frame)), float(basecamera.knob('haperture').getValueAt(frame)), float(basecamera.knob('vaperture').getValueAt(frame))
		near, far = float(basecamera.knob('near').getValueAt(frame)), float(basecamera.knob('far').getValueAt(frame))
	
		print trOrder, rotOrder, trX, trY, trZ, rX, rY, rZ, focal, hap, vap, near, far
		
		return trOrder, rotOrder, trX, trY, trZ, rX, rY, rZ, focal, hap, vap, near, far
		
	def createProjectionCamera(self, basecamera, frame, trOrder, rotOrder, trX, trY, trZ, rX, rY, rZ, focal, hap, vap, near, far):
	
		camera = nuke.createNode('Camera2', inpanel =  False)
		camera.setName(basecamera.name()+'_projCamera')
		camera.knob('label').setValue(str(frame))
		
		camera.knob('translate').setValue([trX, trY, trZ])
		camera.knob('rotate').setValue([rX, rY, rZ])
		camera.knob('focal').setValue(focal)
		camera.knob('haperture').setValue(hap)
		camera.knob('vaperture').setValue(vap)
		camera.knob('near').setValue(near)
		camera.knob('far').setValue(far)
		camera.knob('xform_order').setValue(trOrder)
		camera.knob('rot_order').setValue(rotOrder)
		
		camera.knob('xpos').setValue(basecamera.knob('xpos').value()+100)
		camera.knob('ypos').setValue(basecamera.knob('ypos').value())
		
		return camera