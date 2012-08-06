import maya.cmds as cmds
import time
import os
import subprocess

from dmptools.mayaToNuke.utils import Utils
UTILS = Utils()

class Exporter(object):
    """
        generate a nuke script (.nk) from a selection.
    """
    def __init__(self, items={}, outputFile='', framerange={}):
        # get the stuff to export and the outputFile
        self.items = items
        self.outputFile = outputFile
        # get the framerange info
        self.currentFrame = framerange['current']
        self.firstFrame = framerange['first']
        self.lastFrame = framerange['last']
        # get time
        timeInfo = UTILS.getTime()
        self.currTime = timeInfo['current']
        self.timeStr = timeInfo['str']
        # get the nuke.exe path
        self.nukeexe = UTILS.nukeexe

    def startExport(self):
        """
            write the python file which will be used
            to generate the nuke script.
        """
        print "----------------| start |----------------"

        pyFile = "c:/tmp/"+self.outputFile.split('/')[-1].split('.')[-2]+"_"+self.currTime+".py"
        generateNukeScript = '"'+self.nukeexe+'" -t '+pyFile+''

        # writing header of the python file
        self.filePy = open(pyFile, "a")
        
        self.filePy.write("# this python file is generated automatically by the mayaToNuke.py tool.\n")
        self.filePy.write("# it will be processed by mayapy and will create a .nk file.\n\n")
        self.filePy.write("# name of the python file: "+pyFile+"\n")
        self.filePy.write("# name of the maya file: "+self.outputFile+"\n")
        self.filePy.write("# generated the : "+self.timeStr+"\n\n")
        self.filePy.write('import nuke\n\n')
        self.filePy.write('nuke.root().knob("first_frame").setValue('+str(self.firstFrame)+')\n')
        self.filePy.write('nuke.root().knob("last_frame").setValue('+str(self.lastFrame)+')\n\n')
        
        # get the items
        objects = self.items['meshes']
        cameras = self.items['cameras']
        locators = self.items['locators']
        lights = self.items['lights']

        if objects:
            print "-exporting "+str(len(objects))+" objects:"
            self.writeObjectsToPyFile(objects, self.filePy)
        
        if cameras:
            print "-exporting "+str(len(cameras))+" cameras:"
            self.writeCamerasToPyFile(cameras, self.filePy)

        if locators:
            print "-exporting "+str(len(locators))+" locators:"
            self.writeLocatorsToPyFile(locators, self.filePy)
            
        self.filePy.write('\n')
        self.filePy.write('nuke.frame('+str(self.currentFrame)+')\n\n')             
        self.filePy.write('nuke.scriptSave("'+self.outputFile+'")\n\n\n') 
        self.filePy.close()
        
        # if there is something to export, generate the nuke script file (.nk) from the python script
        if objects or cameras or locators or lights:
            # wait loop
            print " > generating and saving the nuke script ..."
            if os.path.exists(self.outputFile):
                os.remove(self.outputFile)
            t=0
            while not os.path.exists(self.outputFile):
                print ' > time spent: '+str(t)+' second(s)...'
                # generating the nuke script in the first iteration of the wait loop
                if t == 0:
                    if os.name == 'nt':
                        subprocess.Popen(generateNukeScript)
                    else:
                        subprocess.Popen('nuke -t '+pyFile+' &')
                if os.path.exists(self.outputFile):
                        break
                if t == 10:
                    break
                else:
                    time.sleep(1)
                    t += 1
            if os.path.exists(self.outputFile):
                # print some debug stuff
                print "export successfully: "+self.outputFile
                print '### debug python file:'
                print "os.system('scite "+pyFile+" &')"
                print '### nuke file:'
                print "nuke "+self.outputFile
                print "os.system('nuke "+self.outputFile+" &')"

                cmds.confirmDialog(t = 'Success !', m = 'The nuke script has been generated.\nSee script editor for more informations.')
            else:
                print 'failed to generate the nuke file...'
                print '### debug python file:'
                print "os.system('scite "+pyFile+" &')"
                
                cmds.confirmDialog(t = 'Error !', m = 'The nuke script has NOT been generated.\nSee script editor for more informations.')
        else:
            cmds.confirmDialog(t = 'Warning', m = 'There is nothing to export !')          
        
        #end
        print "----------------| end |----------------"
                
    def writeObjectsToPyFile(self, objects, filePy):
        """ export the mesh to an obj file and write the node """
        print objects
        # load objExport plugin if not already loaded
        loaded = False
        if not "objExport" in cmds.pluginInfo(query=True, listPlugins=True):
            cmds.loadPlugin('objExport')      
            loaded = True
        else:
            print 'objExport already loaded...'
            loaded = True
        if loaded:
            # search for animated meshes
            animMeshes = []
            deformedMeshes = []
            staticMeshes = []
            # check connections
            for object in objects:
                objTx = '%s.tx' % object
                objTy = '%s.ty' % object
                objTz = '%s.tz' % object
                objRx = '%s.tx' % object
                objRy = '%s.ty' % object
                objRz = '%s.tz' % object
                objSx = '%s.tx' % object
                objSy = '%s.ty' % object
                objSz = '%s.tz' % object
                objVisible = '%s.visibility' % object
                # if a connection is found in any of the above
                # consider the mesh animated/deformed
                if cmds.connectionInfo( objTx, isDestination=True) or\
                    cmds.connectionInfo( objTy, isDestination=True) or\
                    cmds.connectionInfo( objTz, isDestination=True) or\
                    cmds.connectionInfo( objRx, isDestination=True) or\
                    cmds.connectionInfo( objRy, isDestination=True) or\
                    cmds.connectionInfo( objRz, isDestination=True) or\
                    cmds.connectionInfo( objSx, isDestination=True) or\
                    cmds.connectionInfo( objSy, isDestination=True) or\
                    cmds.connectionInfo( objSz, isDestination=True) or\
                    cmds.connectionInfo( objVisible, isDestination=True):
                    deformedMeshes.append(object)
                else:
                    staticMeshes.append(object)
            print '--deformed: '+str(deformedMeshes)
            print '--static: '+str(staticMeshes)
            # mesh path
            meshPath = os.path.dirname(self.outputFile)+'/'+os.path.basename(self.outputFile).split('.')[-0]+'/'
            if not os.path.exists(meshPath):
                os.makedirs(meshPath)

            # STATIC MESHES
            if staticMeshes:
                filePy.write('# creating readGeos \n\n')
                for mesh in staticMeshes:
                    print 'exporting: '+mesh
                    filePy.write('# creating "'+mesh+'" \n')
                    cmds.select(mesh, r = True)
                    # get attr
                    rotList = ["XYZ","YZX","ZXY","XZY","YXZ","ZYX"]
                    meshRot = cmds.getAttr(mesh+".rotateOrder")
                    meshRotationOrder = rotList[meshRot]
                    # set name
                    meshClean = mesh.replace(':', '_').replace('|', '_')
                    meshname = meshPath+meshClean+'.obj'
                    # export the obj file                    
                    cmds.file(meshname, pr = 1, typ = "OBJexport", es = 1, op = "groups=0;ptgroups=0;materials=0;smoothing=0;normals=1")
                    # write to pyFile
                    filePy.write('readGeo = nuke.createNode("ReadGeo")\n')
                    filePy.write('readGeo.knob("file").setValue("'+meshname+'")\n')
                    filePy.write('readGeo.setName("'+meshClean+'")\n')
                    filePy.write('readGeo.knob("selected").setValue(False)\n')
                    filePy.write('readGeo.knob("rot_order").setValue("'+meshRotationOrder+'")\n\n')
                    
            # DEFORMED MESHES 
            if deformedMeshes:
                # first write the nuke node 
                for mesh in deformedMeshes:
                    print 'exporting animated/deformed: '+mesh
                    filePy.write('# creating "'+mesh+'" \n')
                    cmds.select(mesh, r = True)
                    # get maya attributes
                    rotList = ["XYZ","YZX","ZXY","XZY","YXZ","ZYX"]
                    meshRot = cmds.getAttr(mesh+".rotateOrder")
                    meshRotationOrder = rotList[meshRot]
                    # set name
                    meshClean = mesh.replace(':', '_').replace('|', '_')
                    meshname = meshPath+meshClean+'.####.obj'
                    # write to pyFile
                    filePy.write('readGeo = nuke.createNode("ReadGeo")\n')
                    filePy.write('readGeo.knob("file").setValue("'+meshname+'")\n')
                    filePy.write('readGeo.setName("'+meshClean+'")\n')
                    filePy.write('readGeo.knob("selected").setValue(False)\n')
                    filePy.write('readGeo.knob("rot_order").setValue("'+meshRotationOrder+'")\n\n')

                # then export obj sequence files
                for frame in range(self.firstFrame, self.lastFrame+1):
                    cmds.currentTime(frame)
                    for mesh in deformedMeshes:
                        cmds.select(mesh, r = True)
                        meshClean = mesh.replace(':', '_').replace('|', '_')
                        meshname = meshPath+meshClean+'.'+str(int(frame))+'.obj'
                        print meshname
                        cmds.file(meshname, f = True, pr = 1, typ = "OBJexport", es = 1, op = "groups=0;ptgroups=0;materials=0;smoothing=0;normals=1")

    def writeCamerasToPyFile(self, cameras, filePy):
        """ bake cameras and write the node """            
        # first create all cameras nuke nodes
        for camera in cameras:
            filePy.write('# creating "'+camera+'" \n')
            cmds.select(camera, r = True)
            cameraShape = cmds.listRelatives(camera)[0]
            # get maya attributes           
            rotList = ["XYZ","YZX","ZXY","XZY","YXZ","ZYX"]
            camRot = cmds.getAttr(camera+".rotateOrder")
            cameraRotationOrder = rotList[camRot]
            nearClip = float(cmds.getAttr(cameraShape+".nearClipPlane"))
            farClip = float(cmds.getAttr(cameraShape+".farClipPlane"))
            # write to pyFile
            filePy.write('camera = nuke.createNode("Camera2")\n')
            filePy.write('camera.setName("'+camera+'")\n')
            filePy.write('camera.knob("selected").setValue(False)\n')
            filePy.write('camera.knob("rot_order").setValue("'+cameraRotationOrder+'")\n\n')
            filePy.write('camera.knob("near").setValue('+str(nearClip)+')\n')
            filePy.write('camera.knob("far").setValue('+str(farClip)+')\n')

        # then bake in maya and animate in nuke node
        for frame in range(self.firstFrame, self.lastFrame+1):
            filePy.write('nuke.frame('+str(int(frame))+')\n')
            cmds.currentTime(frame)
            for camera in cameras:
                # get shape
                cameraShape = cmds.listRelatives(camera)[0]
                # get worldspace attributes
                xformT = cmds.xform(camera, t = True, ws=True, q = True)
                xformR = cmds.xform(camera, ro = True, ws=True, q = True)
                xformS = cmds.xform(camera, s = True, r = True, q = True)
                # get lens infos
                focal = float(cmds.getAttr(cameraShape+".focalLength"))
                hap = float(cmds.getAttr(cameraShape+".horizontalFilmAperture"))/ 0.0393700787
                vap = float(cmds.getAttr(cameraShape+".verticalFilmAperture"))/ 0.0393700787
                # write to file
                filePy.write('cameraToAnimate = nuke.toNode("'+camera+'")\n')
                # set translate
                filePy.write('cameraToAnimate.knob("translate").setValueAt('+str(float(xformT[0]))+',\
                            '+str(float(frame))+', 0)\n')
                filePy.write('cameraToAnimate.knob("translate").setValueAt('+str(float(xformT[1]))+',\
                            '+str(float(frame))+', 1)\n')
                filePy.write('cameraToAnimate.knob("translate").setValueAt('+str(float(xformT[2]))+',\
                            '+str(float(frame))+', 2)\n')
                filePy.write('cameraToAnimate.knob("translate").setKeyAt('+str(frame)+')\n')
                # set rotate                 
                filePy.write('cameraToAnimate.knob("rotate").setValueAt('+str(float(xformR[0]))+',\
                            '+str(float(frame))+', 0)\n')
                filePy.write('cameraToAnimate.knob("rotate").setValueAt('+str(float(xformR[1]))+',\
                            '+str(float(frame))+', 1)\n')
                filePy.write('cameraToAnimate.knob("rotate").setValueAt('+str(float(xformR[2]))+',\
                            '+str(float(frame))+', 2)\n')
                filePy.write('cameraToAnimate.knob("rotate").setKeyAt('+str(frame)+')\n')
                # set scale
                filePy.write('cameraToAnimate.knob("scaling").setValueAt('+str(float(xformS[0]))+',\
                            '+str(float(frame))+', 0)\n')
                filePy.write('cameraToAnimate.knob("scaling").setValueAt('+str(float(xformS[1]))+',\
                            '+str(float(frame))+', 1)\n')
                filePy.write('cameraToAnimate.knob("scaling").setValueAt('+str(float(xformS[2]))+',\
                            '+str(float(frame))+', 2)\n')
                filePy.write('cameraToAnimate.knob("scaling").setKeyAt('+str(frame)+')\n')
                # set focal hap and vap
                filePy.write('cameraToAnimate.knob("focal").setValueAt('+str(focal)+',\
                            '+str(float(frame))+', 0)\n')
                filePy.write('cameraToAnimate.knob("focal").setKeyAt('+str(frame)+')\n')
                filePy.write('cameraToAnimate.knob("haperture").setValueAt('+str(hap)+',\
                            '+str(float(frame))+', 0)\n')
                filePy.write('cameraToAnimate.knob("haperture").setKeyAt('+str(frame)+')\n')
                filePy.write('cameraToAnimate.knob("vaperture").setValueAt('+str(vap)+',\
                            '+str(float(frame))+', 0)\n')
                filePy.write('cameraToAnimate.knob("vaperture").setKeyAt('+str(frame)+')\n')      
        
    def writeLocatorsToPyFile(self, locators, filePy):
        """ bake cameras and write the node """            
        print locators
        print '--locators: '+str(locators)
        # creating all locators nuke nodes
        for locator in locators:
            filePy.write('# creating "'+locator+'" \n')
            cmds.select(locator, r = True)
            # get maya attributes           
            rotList = ["XYZ","YZX","ZXY","XZY","YXZ","ZYX"]
            locRot = cmds.getAttr(locator+".rotateOrder")
            locatorRotationOrder = rotList[locRot]            
            # write to pyFile
            filePy.write('locator = nuke.createNode("Axis")\n')
            filePy.write('locator.setName("'+locator+'")\n')
            filePy.write('locator.knob("selected").setValue(False)\n')
            filePy.write('locator.knob("rot_order").setValue("'+locatorRotationOrder+'")\n\n')

        # bake in maya and animate all locators nuke nodes
        for frame in range(self.firstFrame, self.lastFrame+1):
            filePy.write('nuke.frame('+str(int(frame))+')\n')
            cmds.currentTime(frame)
            for locator in locators:
                # get worldspace attributes
                xformT = cmds.xform(locator, t = True, ws=True, q = True)
                xformR = cmds.xform(locator, ro = True, ws=True, q = True)
                xformS = cmds.xform(locator, s = True, r = True, q = True)
                # write to file                
                filePy.write('locatorToAnimate = nuke.toNode("'+locator+'")\n')
                # set translate
                filePy.write('locatorToAnimate.knob("translate").setValueAt('+str(float(xformT[0]))+',\
                            '+str(float(frame))+', 0)\n')
                filePy.write('locatorToAnimate.knob("translate").setValueAt('+str(float(xformT[1]))+',\
                            '+str(float(frame))+', 1)\n')
                filePy.write('locatorToAnimate.knob("translate").setValueAt('+str(float(xformT[2]))+',\
                            '+str(float(frame))+', 2)\n')
                filePy.write('locatorToAnimate.knob("translate").setKeyAt('+str(frame)+')\n')
                # set rotate                 
                filePy.write('locatorToAnimate.knob("rotate").setValueAt('+str(float(xformR[0]))+',\
                            '+str(float(frame))+', 0)\n')
                filePy.write('locatorToAnimate.knob("rotate").setValueAt('+str(float(xformR[1]))+',\
                            '+str(float(frame))+', 1)\n')
                filePy.write('locatorToAnimate.knob("rotate").setValueAt('+str(float(xformR[2]))+',\
                            '+str(float(frame))+', 2)\n')
                filePy.write('locatorToAnimate.knob("rotate").setKeyAt('+str(frame)+')\n')
                # set scale
                filePy.write('locatorToAnimate.knob("scaling").setValueAt('+str(float(xformS[0]))+',\
                            '+str(float(frame))+', 0)\n')
                filePy.write('locatorToAnimate.knob("scaling").setValueAt('+str(float(xformS[1]))+',\
                            '+str(float(frame))+', 1)\n')
                filePy.write('locatorToAnimate.knob("scaling").setValueAt('+str(float(xformS[2]))+',\
                            '+str(float(frame))+', 2)\n')
                filePy.write('locatorToAnimate.knob("scaling").setKeyAt('+str(frame)+')\n')
