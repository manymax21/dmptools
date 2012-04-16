# Nuke Ratio calculator according to a given Camera node
# michael-ha@moving-picture.com
#

import nuke
import nukescripts

class RatioCalculator(nukescripts.PythonPanel):
    def __init__(self, camera):
        
        nukescripts.PythonPanel.__init__( self, 'Ratio calculator', 'ratioCalculator')
        
        self.camera = camera
        
        self.dmp = ''
        self.dmpX = 4096
        self.dmpY = None

        # create knobs
        self.cameratext = nuke.Text_Knob('camera', 'Camera:')
        self.cameratext.setValue(self.camera.name())
        self.cameraRatio = float(self.camera['haperture'].getValue())/float(self.camera['vaperture'].getValue())
            
        self.camh = nuke.IArray_Knob('haperture', 'Haperture')
        self.camv = nuke.IArray_Knob('vaperture', 'Vaperture')
        self.camh.setValue(self.camera['haperture'].getValue())
        self.camv.setValue(self.camera['vaperture'].getValue())

        self.dmpx = nuke.Int_Knob('dmpResolution', 'Xresolution')
        self.dmpy = nuke.Int_Knob('dmpResolution', 'Yresolution')
        self.dmpx.setValue(self.dmpX)
        self.dmpy.setValue(float(self.dmpx.getValue())/self.cameraRatio)
        
        self.ratiotxt = nuke.Text_Knob('ratioText', 'ratio:', str(self.cameraRatio))
        #self.ratiotxt.setFlag(4096)
        
        self.mode = nuke.Boolean_Knob('mode', 'Mode', False)
        self.mode.setFlag(4096)

        self.text = nuke.Text_Knob('modeText', '', 'locked for ratio')
        self.mode.setFlag(8192)
        
        # add knobs
        self.addKnob(self.cameratext)
        self.addKnob(self.camh)
        self.addKnob(self.camv)
        self.addKnob(self.dmpx)
        self.addKnob(self.dmpy)
        self.addKnob(self.ratiotxt)
        self.addKnob(self.mode)
        self.addKnob(self.text)

    def knobChanged(self, knob):

        if knob == self.mode:
            if self.mode.getValue() == 0:
                self.text.setValue('locked for ratio')
            if self.mode.getValue() == 1:
                self.text.setValue('locked for offset')
        
        # camera changed
        if knob == self.camh:
            mode = self.mode.getValue()
            if mode == 0:
                ratio = float(float(self.dmpx.getValue())/float(self.dmpy.getValue()))
                self.camv.setValue(float(self.camh.getValue())/ratio)
                self.camera['haperture'].setValue(float(self.camh.getValue()))
                self.camera['vaperture'].setValue(float(self.camh.getValue())/ratio)
                self.ratiotxt.setValue(str(ratio))
                
            if mode == 1:
                camRatio = float(float(self.camh.getValue())/float(self.camv.getValue()))
                self.dmpx.setValue(self.intRound(float(self.dmpy.getValue())*camRatio))
                self.camera['haperture'].setValue(float(self.camh.getValue()))
                self.ratiotxt.setValue(str(camRatio))
                
        if knob == self.camv:
            mode = self.mode.getValue()
            if mode == 0:
                ratio = float(float(self.dmpx.getValue())/float(self.dmpy.getValue()))
                self.camh.setValue(float(self.camv.getValue())*ratio)
                self.camera['haperture'].setValue(float(self.camv.getValue())*ratio)
                self.camera['vaperture'].setValue(float(self.camv.getValue))
                self.ratiotxt.setValue(str(ratio))
                
            if mode == 1:
                camRatio = float(float(self.camh.getValue())/float(self.camv.getValue()))
                self.dmpy.setValue(int(float(self.dmpx.getValue())/camRatio))
                self.camera['vaperture'].setValue(float(self.camv.getValue))
                self.ratiotxt.setValue(str(camRatio))
                
        # dmp changed
        if knob == self.dmpx:
            mode = self.mode.getValue()
            if mode == 0:
                ratio = float(float(self.camh.getValue())/float(self.camv.getValue()))
                self.dmpy.setValue(self.intRound(float(self.dmpx.getValue())/ratio))
                self.ratiotxt.setValue(str(ratio))
                
            if mode == 1:
                dmpRatio = float(self.dmpx.getValue())/float(self.dmpy.getValue())
                self.camh.setValue(float(self.camv.getValue())*dmpRatio)
                self.camera['haperture'].setValue(float(self.camv.getValue())*dmpRatio)
                self.ratiotxt.setValue(str(dmpRatio))
                
        if knob == self.dmpy:
            mode = self.mode.getValue()
            if mode == 0:
                ratio = float(float(self.camh.getValue())/float(self.camv.getValue()))
                self.dmpx.setValue(self.intRound(float(self.dmpy.getValue())*ratio))
                self.ratiotxt.setValue(str(ratio))
                
            if mode == 1:
                dmpRatio = float(self.dmpx.getValue())/float(self.dmpy.getValue())
                self.camv.setValue(float(self.camh.getValue())/dmpRatio)
                self.camera['vaperture'].setValue(float(self.camh.getValue())/dmpRatio)
                self.ratiotxt.setValue(str(dmpRatio))
                
    def intRound(self, value):
        return int(round(value, 0))
    
def ratioCalculator():
    nodes = nuke.selectedNodes()

    if len(nodes) == 2:
        camera = [node for node in nodes if node.Class() in ('Camera', 'Camera2')][0]
        
        RatioCalculator(camera, dmp).show()
            
    if len(nodes) == 1:
        camera = [node for node in nodes if node.Class() in ('Camera', 'Camera2')][0]
        dmp = None
        
        RatioCalculator(camera).show()
        
    if len(nodes) == 0 or len(nodes) >= 2:
        nuke.message('please select a Camera node')
        
    nukescripts.registerPanel( 'ratioCalculator', ratioCalculator)
