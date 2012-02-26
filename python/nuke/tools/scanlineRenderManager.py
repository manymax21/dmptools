#====================================================
#
# create a scanline render manager dockable panel
# 
# it drives the common attributes of all the scanline render nodes in the script
#
#====================================================

import nuke
import nukescripts
from threading import Thread

class ScanlineRenderManager(nukescripts.PythonPanel, Thread):
    def __init__(self):
        
        nukescripts.PythonPanel.__init__( self, 'ScanlineRenderManager', 'ScanlineRenderManager')
        Thread.__init__(self)

        knobs = []
    
        #scanlineRenderTab = nuke.Tab_Knob("ScanlineRender Manager")
        self.header = nuke.Text_Knob('header', '', "Override all the scanline render nodes in this script.")
        # scanlineRender createknobs
        self.scanlineRenderGRP_start = nuke.Tab_Knob("ScanlineRender_start", "ScanlineRender",  nuke.TABBEGINGROUP)
        self.transparencyKnob = nuke.Boolean_Knob('transparency', 'transparency', 1)
        self.ZbufferKnob = nuke.Boolean_Knob('Z-buffer', 'Z-buffer', 1)
        self.filterKnob = nuke.Enumeration_Knob('filter', 'filter', ['Impulse', 'Cubic', 'Keys', 'Simon', 'Rifman', 'Mitchell', 'Parzen', 'Notch'])
        self.filterKnob.setValue('Cubic')
        self.antialiasingKnob =  nuke.Enumeration_Knob('antialiasing', 'antialiasing', ['none', 'low', 'medium', 'high'])
        self.overscanKnob = nuke.WH_Knob('overscan', 'overscan')
        self.scanlineRenderGRP_end = nuke.Tab_Knob("ScanlineRender_end", "ScanlineRender",  nuke.TABENDGROUP)

        # multisamples createknobs
        self.multisamplesGRP_start = nuke.Tab_Knob("Multisamples_start", "Multisamples",  nuke.TABBEGINGROUP)
        self.samplesKnob = nuke.Int_Knob('samples', 'samples')
        self.samplesKnob.setValue(1)
        self.shutterKnob = nuke.Double_Knob('shutter', 'shutter')
        self.shutterKnob.setValue(0.5)
        self.multisamplesGRP_end = nuke.Tab_Knob("Multisamples_end", "Multisamples",  nuke.TABENDGROUP)

        # shader createknobs
        #shaderGRP_start = nuke.Tab_Knob("Shader", "Shader",  nuke.TABBEGINGROUP)

        knobs.append(self.header)
        knobs.append(self.scanlineRenderGRP_start)
        knobs.append(self.transparencyKnob)
        knobs.append(self.ZbufferKnob)
        knobs.append(self.filterKnob)
        knobs.append(self.antialiasingKnob)
        knobs.append(self.overscanKnob)
        knobs.append(self.scanlineRenderGRP_end)
        knobs.append(self.multisamplesGRP_start)
        knobs.append(self.samplesKnob)
        knobs.append(self.shutterKnob)
        knobs.append(self.multisamplesGRP_end)

        for knob in knobs:
            self.addKnob(knob)
        
    def knobChanged(self, knob):

        scanlineRenders = nuke.allNodes('ScanlineRender')
        
        if scanlineRenders:
            for node in scanlineRenders:
                if knob == self.transparencyKnob:
                    transparency = self.transparencyKnob.value()
                    node.knob('transparency').setValue(transparency)
                if knob == self.ZbufferKnob:
                    Zbuffer = self.ZbufferKnob.value()
                    node.knob('ztest_enabled').setValue(Zbuffer)
                if knob == self.filterKnob:
                    filter = self.filterKnob.value()
                    node.knob('filter').setValue(filter)
                if knob == self.antialiasingKnob:
                    antialiasing = self.antialiasingKnob.value()
                    node.knob('antialiasing').setValue(antialiasing)
                if knob == self.overscanKnob:
                    overscan = self.overscanKnob.value()
                    node.knob('overscan').setValue(overscan)
                if knob == self.samplesKnob:
                    samples = self.samplesKnob.value()
                    node.knob('samples').setValue(samples)
                if knob == self.shutterKnob:
                    shutter = self.shutterKnob.value()
                    node.knob('shutter').setValue(shutter)
