#=================================================
#
# Maya Ratio calculator according to a given Camera node
# michael-ha@moving-picture.com
#
#=================================================

import maya.cmds as cmds
import os

MAYA_PICTURES = '!MAYA_PICTURES!'

class ApertureTool(object):
    def runCamH(self, camh, camv, dmpx, dmpy, cam):
        
        mode = cmds.iconTextRadioButton('hb',  q = True, sl = True)
        
        hap = float(cmds.textField(camh, q = True, tx = True))
        vap =  float(cmds.textField(camv, q = True, tx = True))
        dmpX =  float(cmds.textField(dmpx, q = True, tx = True))
        dmpY =  float(cmds.textField(dmpy, q = True, tx = True))
        
        camRatio = hap/vap
        dmpRatio = dmpX/dmpY
        
        if mode == 0:
            newdmpx = ApertureTool().intRound(dmpY*camRatio)
            cmds.textField(dmpx, e = True, tx = newdmpx)
            
            cmds.setAttr(cam+'.horizontalFilmAperture', hap)
            cmds.setAttr(cam+'.verticalFilmAperture', vap)
            
        if mode == 1:
            newvap = hap/dmpRatio
            cmds.textField(camv, e = True, tx = newvap)
    
            cmds.setAttr(cam+'.horizontalFilmAperture', hap)
            cmds.setAttr(cam+'.verticalFilmAperture', newvap)
    
    def runCamV(self, camh, camv, dmpx, dmpy, cam):
        
        mode = cmds.iconTextRadioButton('hb',  q = True, sl = True)
        
        hap = float(cmds.textField(camh, q = True, tx = True))
        vap =  float(cmds.textField(camv, q = True, tx = True))
        dmpX =  float(cmds.textField(dmpx, q = True, tx = True))
        dmpY =  float(cmds.textField(dmpy, q = True, tx = True))
        
        camRatio = hap/vap
        dmpRatio = dmpX/dmpY
        
        if mode == 0:
            newdmpy = ApertureTool().intRound(dmpX/camRatio)
            cmds.textField(dmpy, e = True, tx = newdmpy)
            
            cmds.setAttr(cam+'.horizontalFilmAperture', hap)
            cmds.setAttr(cam+'.verticalFilmAperture', vap)

        if mode == 1:
            newhap = vap*dmpRatio
            cmds.textField(camh, e = True, tx = newhap)

            cmds.setAttr(cam+'.horizontalFilmAperture', newhap)
            cmds.setAttr(cam+'.verticalFilmAperture', vap)


    def runDmpX(self, camh, camv, dmpx, dmpy, cam):

        mode = cmds.iconTextRadioButton('hb',  q = True, sl = True)

        hap = float(cmds.textField(camh, q = True, tx = True))
        vap =  float(cmds.textField(camv, q = True, tx = True))
        dmpX =  float(cmds.textField(dmpx, q = True, tx = True))
        dmpY =  float(cmds.textField(dmpy, q = True, tx = True))
        
        camRatio = hap/vap
        dmpRatio = dmpX/dmpY
                
        if mode == 0:
            newhap = vap*dmpRatio
            cmds.textField(camh, e = True, tx = newhap)
            
            cmds.setAttr(cam+'.horizontalFilmAperture', newhap)
            cmds.setAttr(cam+'.verticalFilmAperture', vap)
        
        if mode == 1:
            newdmpy = ApertureTool().intRound(dmpX/camRatio)
            cmds.textField(dmpy, e = True, tx = newdmpy)
            
            cmds.setAttr(cam+'.horizontalFilmAperture', hap)
            cmds.setAttr(cam+'.verticalFilmAperture', vap)

    def runDmpY(self, camh, camv, dmpx, dmpy, cam):

        mode = cmds.iconTextRadioButton('hb',  q = True, sl = True)

        hap = float(cmds.textField(camh, q = True, tx = True))
        vap =  float(cmds.textField(camv, q = True, tx = True))
        dmpX =  float(cmds.textField(dmpx, q = True, tx = True))
        dmpY =  float(cmds.textField(dmpy, q = True, tx = True))
        
        camRatio = hap/vap
        dmpRatio = dmpX/dmpY
        
        if mode == 0:
            newvap = hap/(float(dmpX)/float(dmpY))
            cmds.textField(camv, e = True, tx = newvap)
            
            cmds.setAttr(cam+'.horizontalFilmAperture', hap)
            cmds.setAttr(cam+'.verticalFilmAperture', newvap)
        
        if mode == 1:
            newdmpx = ApertureTool().intRound(dmpY*camRatio)
            cmds.textField(dmpx, e = True, tx = newdmpx)
            
            cmds.setAttr(cam+'.horizontalFilmAperture', hap)
            cmds.setAttr(cam+'.verticalFilmAperture', vap)

    def intRound(self, val):
        return int(round(val, 0))

    def getCameraAperture(self, cam):
        return float(cmds.getAttr(cam[1]+".horizontalFilmAperture")), float(cmds.getAttr(cam[1]+".verticalFilmAperture"))
        
    def apertureToolwindow(self, cam):
    
        if cmds.window("apertureToolWindow", exists = True):
            cmds.deleteUI("apertureToolWindow", window = True)
        #if cmds.windowPref("apertureToolWindow", exists = True):
        #    cmds.windowPref("apertureToolWindow", remove = True)
            
        # window
        cmds.window("apertureToolWindow", t = "Ratio Calculator: "+cam[0], w = 300, h = 130)
        #cmds.columnLayout(adj = True)
        form = cmds.formLayout()
        
        separatorTop = cmds.separator()
        separatorBottom = cmds.separator()
        
        camtext = cmds.text(l = 'camera aperture', al = 'left')
        camHtextField = cmds.textField(text = self.getCameraAperture(cam)[0], w = 100)
        camVtextField = cmds.textField(text = self.getCameraAperture(cam)[1], w = 100)
        
        tmpDMPx = 4096
        tmpDMPy = ApertureTool().intRound(4096.0/(self.getCameraAperture(cam)[0]/self.getCameraAperture(cam)[1]))
        
        dmptext = cmds.text(l = 'dmp resolution', al = 'left')
        dmpXtextField = cmds.textField(text = tmpDMPx, w = 100)
        dmpYtextField = cmds.textField(text = tmpDMPy, w = 100)
            
        vbuttons = cmds.iconTextRadioCollection('buttons')
        vbutton = cmds.iconTextRadioButton('vb', st = 'iconOnly', w = 20, onc = 'import maya.cmds as cmds;cmds.text("text", e = True, l = "locked for offset")')
        hbutton = cmds.iconTextRadioButton('hb', st = 'iconOnly', h = 20, onc = 'import maya.cmds as cmds;cmds.text("text", e = True, l = "locked for ratio")')
        
        cmds.iconTextRadioButton('vb', e = True, i = MAYA_PICTURES+'/ratioCalculator_v.tif')
        cmds.iconTextRadioButton('hb', e = True, i = MAYA_PICTURES+'/ratioCalculator_h.tif')
            
        txt = cmds.text('text', l = "locked for ratio", al ='right')
        
        cmds.iconTextRadioButton('hb', e = True, sl = True)
        
        cmds.textField(camHtextField, e = True, cc = 'ratioCalculator.ApertureTool().runCamH("'+camHtextField+'","'+camVtextField+'","'+dmpXtextField+'","'+dmpYtextField+'","'+cam[1]+'")')
        cmds.textField(camVtextField, e = True, cc = 'ratioCalculator.ApertureTool().runCamV("'+camHtextField+'","'+camVtextField+'","'+dmpXtextField+'","'+dmpYtextField+'","'+cam[1]+'")')
        cmds.textField(dmpXtextField, e = True, cc = 'ratioCalculator.ApertureTool().runDmpX("'+camHtextField+'","'+camVtextField+'","'+dmpXtextField+'","'+dmpYtextField+'","'+cam[1]+'")')
        cmds.textField(dmpYtextField, e = True, cc = 'ratioCalculator.ApertureTool().runDmpY("'+camHtextField+'","'+camVtextField+'","'+dmpXtextField+'","'+dmpYtextField+'","'+cam[1]+'")')

        cmds.formLayout(form, e = True, attachForm = [
                                            (camtext, "left", 5),
                                            (camVtextField, "right", 35),
                                            (dmptext, "left", 5),
                                            (dmpYtextField, "right", 35),
                                            (separatorTop, "top", 5),
                                            (separatorTop, "right", 5),
                                            (separatorTop, "left", 5),
                                            (separatorBottom, "right", 5),
                                            (separatorBottom, "left", 5),
                                            (txt, "right", 5),
                                            (txt, "bottom", 5)
                                            ])
        
        cmds.formLayout(form, e = True, attachControl = [
                                            (camtext, "top", 5, separatorTop),
                                            (camHtextField, "top", 5, separatorTop),
                                            (camVtextField, "top", 5, separatorTop),
                                            (dmptext, "top", 10, camtext),
                                            (dmpXtextField, "top", 5, camHtextField),
                                            (dmpYtextField, "top", 5, camVtextField),
                                            (camHtextField, "right", 5, camVtextField),
                                            (dmpXtextField, "right", 5, dmpYtextField),
                                            (hbutton, "top", 2, dmpXtextField),
                                            (vbutton, "left", 2, camVtextField),
                                            (separatorBottom, "bottom", 2, txt)
                                            
                                            ])
        cmds.formLayout(form, e = True, attachOppositeControl = [
                                            (hbutton, "left", 0, dmpXtextField),
                                            (hbutton, "right", 0, camVtextField),
                                            (vbutton, "top", 0, camVtextField),
                                            (vbutton, "bottom", 0, dmpYtextField)
                                            
                                            ])

        # show window
        cmds.showWindow("apertureToolWindow")

    def apertureToolUI(self):
            
        selLen = len(cmds.ls(sl = True))
        cam = cmds.ls(sl = True, dag = True)
        
        if selLen == 1 and cmds.nodeType(cam[1]) == 'camera':
            self.apertureToolwindow(cam)
        else:
            cmds.confirmDialog(t = 'Error !', m = 'please select one camera')
            
            
def main():
    ratioCalculatorLaunch = ApertureTool()
    ratioCalculatorLaunch.apertureToolUI()

if __name__ == '__main__':
    main()
    