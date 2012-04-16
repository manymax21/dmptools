import nuke
import math

class BakeCamera():
    
    def __init__(self):
        
        try:
            basecamera = nuke.selectedNode()
        except:
            basecamera = None
            
        frame = nuke.frame()
        
        if basecamera and basecamera.Class() in ['Camera', 'Camera2', 'hubCamera']:
            
            basecamera.knob('selected').setValue(0)
            knobs = self.getCameraKnobs(basecamera, frame)
            xform = self.getWorldMatrix(basecamera, frame)
            
            projCamera = self.createProjectionCamera(basecamera, frame, knobs, xform)
            
        else:
            nuke.message("please select a render camera ('Camera', 'Camera2', 'hubCamera')")
        
    def getCameraKnobs(self, basecamera, frame):

        trOrder, rotOrder = basecamera.knob('xform_order').value(), basecamera.knob('rot_order').value()        
        focal, hap, vap = float(basecamera.knob('focal').getValueAt(frame)), float(basecamera.knob('haperture').getValueAt(frame)), float(basecamera.knob('vaperture').getValueAt(frame))
        near, far = float(basecamera.knob('near').getValueAt(frame)), float(basecamera.knob('far').getValueAt(frame))
    
        return {'trOrder':trOrder, 'rotOrder':rotOrder, 'focal':focal, 'hap':hap, 'vap':vap, 'near':near, 'far':far}
        
    def getWorldMatrix(self, node, frame):

        worldMatrix = node['world_matrix']
        worldMatrixAt = node['world_matrix'].getValueAt(frame)
        
        matrix = nuke.math.Matrix4()

        worldMatrix = node['world_matrix']
        matrix = nuke.math.Matrix4()
        for y in range(worldMatrix.height()):
            for x in range(worldMatrix.width()):
                matrix[x+(y*worldMatrix.width())] = worldMatrixAt[y + worldMatrix.width()*x]

        transM =nuke.math.Matrix4(matrix)
        transM.translationOnly()
        rotM = nuke.math.Matrix4(matrix)
        rotM.rotationOnly()
        scaleM = nuke.math.Matrix4(matrix)
        scaleM.scaleOnly()
        
        scale = (scaleM.xAxis().x, scaleM.yAxis().y, scaleM.zAxis().z)
        rot = rotM.rotationsZXY()
        rotate = (math.degrees(rot[0]), math.degrees(rot[1]), math.degrees(rot[2]))
        translate = (transM[12], transM[13], transM[14])
        
        return {'tr':translate, 'rot':rotate, 'sc':scale}
        
    def createProjectionCamera(self, basecamera, frame, knobs, xform):
    
        camera = nuke.createNode('Camera2', inpanel =  False)
        camera.setName(basecamera.name()+'_projCamera')
        camera.knob('label').setValue(str(frame))
        
        camera.knob('translate').setValue(xform['tr'])
        camera.knob('rotate').setValue(xform['rot'])
        camera.knob('scaling').setValue(xform['sc'])        
        camera.knob('focal').setValue(knobs['focal'])
        camera.knob('haperture').setValue(knobs['hap'])
        camera.knob('vaperture').setValue(knobs['vap'])
        camera.knob('near').setValue(knobs['near'])
        camera.knob('far').setValue(knobs['far'])
        camera.knob('xform_order').setValue(knobs['trOrder'])
        camera.knob('rot_order').setValue(knobs['rotOrder'])
        
        camera.knob('xpos').setValue(basecamera.knob('xpos').value()+100)
        camera.knob('ypos').setValue(basecamera.knob('ypos').value())
        
        return camera
        