import nuke
import nukescripts
import os
import sys
import time
import math
import socket
import commands as cmd

sys.setrecursionlimit(100)

class ExportToMaya():
    def __init__(self,
                mayapy,
                objects=[],
                cameras=[],
                axiis=[],
                lights=[],
                filePath=None,
                saveObj=None,
                sendToMaya=None):
        
        # save script
        if nuke.root()['name'].value():
            nuke.scriptSave()
        else:
            print 'no script to save...'
            
        self.mayapy = mayapy
        self.objects = objects
        self.cameras = cameras
        self.axiis = axiis
        self.lights = lights
        self.filePath = filePath
        self.saveObj = saveObj

        self.startFrame = int(nuke.root()['first_frame'].getValue())
        self.lastFrame = int(nuke.root()['last_frame'].getValue())
        
        currTime = time.strftime('%d%m%y_%H%M%S')
        timeStr = str(time.strftime('%d/%m/%y at %H:%M:%S'))
        self.filePathPy = "/tmp/"+self.filePath.split('/')[-1].split('.')[-2]+"_"+currTime+".py"

        # path of .obj files

        if saveObj == 1:
            self.objPath = os.path.dirname(self.filePath)+"/"+self.filePath.split('/')[-1].split('.')[-2]+"/"
        else:
            self.objPath = "/tmp/"+self.filePath.split('/')[-1].split('.')[-2]+"_"+currTime+"/"

        # writing python file in order to generate the maya scene

        self.filePy = open(self.filePathPy, "a")
        self.filePy.write("# this python file is generated automatically by the 'exportNukeToMaya.py' tool.\n")
        self.filePy.write("# it will be processed by mayapy and will create a .ma file.\n")
        self.filePy.write("# michael havart 2010 (C)\n\n")
        self.filePy.write("# path of mayapy: "+mayapy+"\n")
        self.filePy.write("# name of the python file: "+self.filePathPy+"\n")
        self.filePy.write("# name of the maya file: "+self.filePath+"\n")
        self.filePy.write("# generated the : "+timeStr+"\n\n")
        self.filePy.write("import maya.standalone\n")
        self.filePy.write("maya.standalone.initialize(name = 'python')\n")
        self.filePy.write("import maya.cmds as cmds\n\n")
        
        self.filePy.write("cmds.playbackOptions(min = "+str(self.startFrame)+")\n")
        self.filePy.write("cmds.playbackOptions(max = "+str(self.lastFrame)+")\n\n")

        if self.objects:
            
            print "-exporting "+str(len(self.objects))+" objects:"
            if os.path.exists(self.objPath) == 0:
                os.mkdir(self.objPath)
            self.exportObj(self.filePy, self.objects, self.filePath, self.objPath)
        
        if self.axiis:
            
            print "-exporting "+str(len(self.axiis))+" objects:"
            self.exportAxis(self.filePy, self.axiis, self.filePath, self.startFrame, self.lastFrame)
        
        if self.cameras:
            
            print "-exporting "+str(len(self.cameras))+" cameras:"
            self.exportCam(self.filePy, self.cameras, self.filePath, self.startFrame, self.lastFrame)
        
        if self.lights:
            
            print "-exporting "+str(len(self.lights))+" lights:"
            self.exportLights(self.filePy, self.lights, self.filePath, self.startFrame, self.lastFrame)
        
        self.filePy.write("cmds.setAttr('perspShape.farClipPlane', 100000)\n")		
        self.filePy.write("cmds.setAttr('perspShape.nearClipPlane', 10)\n\n")		
        self.filePy.write("# rename the scene and save it ...\n")
        self.filePy.write("cmds.file( rename= '"+self.filePath+"' )\n")
        self.filePy.write("cmds.file( save=True, type='mayaAscii' )\n")
        self.filePy.write("\n")
        
        self.filePy.close()
        
        # generate the maya file
        
        if os.path.exists(mayapy):
            print "generating and saving .ma ..."
            os.system(self.mayapy+' '+self.filePathPy+'')
            if os.path.exists(self.filePath):
                print "export successfully: "+self.filePath
                #nuke.message("export successfully: "+self.filePath+" (see script editor for more infos)")
            else:
                print "failed to create maya file..."
                nuke.message("failed to create maya file (see script editor for more infos)...")
        else:
            nuke.message("failed to create maya file (see script editor for more infos)...")
            print "failed to create maya file..."
        
        print "-- debug"	
        print "scite "+self.filePathPy
        print "os.system('scite "+self.filePathPy+"&')"
        print "os.system('maya "+self.filePath+"&')"
        print "--------"
        
        # send the scene directly into maya
        
        if sendToMaya == 1:
            self.sendStuffToMaya(self.filePath)
            
        # write nukeToMaya.info with the path of the maya file
        
        crosswalkFile = '/tmp/nukeToMaya.info'
        fileInfo = open(crosswalkFile, "a")
        fileInfo.write('filePath='+self.filePath+'\n')
        fileInfo.close()
        
        #writeInfos("nuketoMaya","export done properly.\n    -exported:\n        "+self.filePath+'\n        '+self.filePathPy)
    

    def sendStuffToMaya(self, mayaScene):

        host = os.environ['HOSTNAME']	
        
        mayaShots = []
        #print cmd.getstatusoutput('echo `more /tmp/mayaInfo.shot`')[1]
        
        FILE = open("/tmp/mayaInfo.shot", "r")
        
        text = FILE.readlines()
        
        for line in text:
            mayahost = line.split(":")[0]
            mayaport = line.split(":")[1]
            mayajob = line.split(":")[2]
            mayashot = line.split(":")[3]	
            mayascene = line.split(":")[4][:-1]	
            
            if mayashot == os.environ['SHOTNAME']:
                mayaShots.append(line[:-1])
        
        FILE.close()
        
        os.system('rm /tmp/mayaInfo.shot')

        print mayaShots
        if len(mayaShots) is not 1:
            mayalist = ''
            for item in mayaShots:
                mayalist += item+" "
            mayalist[:-1]
            askPanel = nuke.Panel('I found more than one maya')
            askPanel.addEnumerationPulldown("send to: ", mayalist)
            val = askPanel.show()
            if val == 1:
                port = int(askPanel.value("send to: ").split(':')[1])
            else:
                port = 0
        else:
            port = int(mayaShots[0].split(':')[1])
        try:
            maya = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            maya.connect((host,port))
            message = 'file -import -type "mayaAscii" -options "v=0" -loadReferenceDepth "all" "'+mayaScene+'";'
            maya.send(message)
            maya.close()
            print "scene sent to maya:"+str(port)
        except:
            print 'failed to send to maya: bad port (:'+str(port)+')'


    def exportObj(self, filePy, objects, filePath, objPath):

        objPathList = []
        
        filePy.write("# importing obj files...\n\n")
        
        for node in objects:
            
            for i in nuke.allNodes():
                i['selected'].setValue(0)
        
            print "processing "+node.name()+" ..."
            node['selected'].setValue(1)
            writeObj = nuke.createNode('WriteGeo', inpanel = False)
            writeObj['name'].setValue(node.name()+"_export")
            writeObj['file'].setValue(objPath+node.name()+".obj")
            writeObj['file_type'].setValue('obj')
            writeObj['views'].setValue('left')
            
            objPathList.append(objPath+node.name()+".obj")
            nuke.execute(writeObj, int(nuke.root()['first_frame'].getValue()), int(nuke.root()['first_frame'].getValue()))
            for i in nuke.allNodes():
                i['selected'].setValue(0)
            writeObj['selected'].setValue(1)
            nukescripts.node_delete()
                
        for object in objPathList:
            filePy.write("cmds.file('"+object+"', i = True, type = 'OBJ', ra = True)\n")
            
        filePy.write("\n")
        filePy.write("# make group of all the *_Mesh nodes ...\n\n")
        filePy.write("cmds.select('*_Mesh')\n")
        filePy.write("cmds.group(name = 'geo_GRP')\n\n")
        filePy.write("# renaming the files without '_Mesh' ...\n\n")
        filePy.write("meshes = cmds.ls('*_Mesh')\n")
        filePy.write("for node in meshes:\n")
        filePy.write("	cmds.rename(node, node[-0:-5])\n\n")

    def exportAxis(self, filePy, axiis, filePath, startFrame, lastFrame):

        filePy.write("# creating locators ... \n\n")
        filePy.write("locatorList = []\n\n")

        for node in axiis:
            
            print "proccessing axis "+node.name()+" ..."
            
            locatorName = str(node.name())
            filePy.write("##############\n")
            filePy.write("# creating the locator: "+node.name()+"\n")
            filePy.write("##############\n\n")
            filePy.write("locator = cmds.spaceLocator()\n")
        
            for frame in range(startFrame,lastFrame+1):
                
                filePy.write("cmds.currentTime("+str(frame)+")\n")
                # translateX
                trX = str(self.getWorldMatrix(node, frame)[2][0])
                filePy.write("cmds.setAttr(locator[0]+'.translateX', "+trX+")\n")
                filePy.write("cmds.setKeyframe(locator[0]+'.tx')\n")
                
                # translateY
                trY = str(self.getWorldMatrix(node, frame)[2][1])
                filePy.write("cmds.setAttr(locator[0]+'.translateY', "+trY+")\n")
                filePy.write("cmds.setKeyframe(locator[0]+'.ty')\n")
                
                # translateZ
                trZ = str(self.getWorldMatrix(node, frame)[2][2])
                filePy.write("cmds.setAttr(locator[0]+'.translateZ', "+trZ+")\n")
                filePy.write("cmds.setKeyframe(locator[0]+'.tz')\n")
                
                # rotateX
                roX = str(self.getWorldMatrix(node, frame)[1][0])
                filePy.write("cmds.setAttr(locator[0]+'.rotateX', "+roX+")\n")
                filePy.write("cmds.setKeyframe(locator[0]+'.rx')\n")
                
                # rotateY
                roY = str(self.getWorldMatrix(node, frame)[1][1])
                filePy.write("cmds.setAttr(locator[0]+'.rotateY', "+roY+")\n")
                filePy.write("cmds.setKeyframe(locator[0]+'.ry')\n")
                
                # rotateZ
                roZ = str(self.getWorldMatrix(node, frame)[1][2])
                filePy.write("cmds.setAttr(locator[0]+'.rotateZ', "+roZ+")\n")
                filePy.write("cmds.setKeyframe(locator[0]+'.rz')\n")

                # scaleX
                scX = str(self.getWorldMatrix(node, frame)[0][0])
                filePy.write("cmds.setAttr(locator[0]+'.scaleX', "+scX+")\n")
                filePy.write("cmds.setKeyframe(locator[0]+'.sx')\n")
                
                # scaleY
                scY = str(self.getWorldMatrix(node, frame)[0][1])
                filePy.write("cmds.setAttr(locator[0]+'.scaleY', "+scY+")\n")
                filePy.write("cmds.setKeyframe(locator[0]+'.sy')\n")
                
                # scaleZ
                scZ = str(self.getWorldMatrix(node, frame)[0][2])
                filePy.write("cmds.setAttr(locator[0]+'.scaleZ', "+scZ+")\n")
                filePy.write("cmds.setKeyframe(locator[0]+'.sz')\n")

                # rotation order
                rotOrderL = {'XYZ':0,'YZX':1,'ZXY':2,'XZY':3,'YXZ':4,'ZYX':5}
                rotOrder = str(int(rotOrderL[node['rot_order'].value()]))
                filePy.write("cmds.setAttr(locator[0]+'.rotateOrder', "+rotOrder+")\n\n")
                
            filePy.write("cmds.rename(locator[0], '"+node.name()+"')\n")
            filePy.write("locatorList.append('"+node.name()+"')\n\n")
            
            filePy.write("cmds.currentTime("+str(startFrame)+")\n\n")

        filePy.write("cmds.select(cl = True)\n")
        filePy.write("for loc in locatorList:\n")
        filePy.write("	cmds.select(loc, add = True)\n")
        filePy.write("cmds.group(name = 'locators_GRP')\n")
        filePy.write("cmds.select(cl = True)\n\n")

    def exportAxis_old(self, filePy, axiis, filePath, startFrame, lastFrame):

        filePy.write("# creating locators ... \n\n")
        filePy.write("locatorList = []\n\n")

        for node in axiis:
            
            print "proccessing axis "+node.name()+" ..."
            
            locatorName = str(node.name())
            filePy.write("##############\n")
            filePy.write("# creating the locator: "+node.name()+"\n")
            filePy.write("##############\n\n")
            filePy.write("locator = cmds.spaceLocator()\n")
        
            for frame in range(startFrame,lastFrame+1):
                
                filePy.write("cmds.currentTime("+str(frame)+")\n")
                # translateX
                trX = str(float(node['translate'].getValueAt(frame)[0]))
                filePy.write("cmds.setAttr(locator[0]+'.translateX', "+trX+")\n")
                filePy.write("cmds.setKeyframe(locator[0]+'.tx')\n")
                
                # translateY
                trY = str(float(node['translate'].getValueAt(frame)[1]))
                filePy.write("cmds.setAttr(locator[0]+'.translateY', "+trY+")\n")
                filePy.write("cmds.setKeyframe(locator[0]+'.ty')\n")
                
                # translateZ
                trZ = str(float(node['translate'].getValueAt(frame)[2]))
                filePy.write("cmds.setAttr(locator[0]+'.translateZ', "+trZ+")\n")
                filePy.write("cmds.setKeyframe(locator[0]+'.tz')\n")
                
                # rotateX
                roX = str(float(node['rotate'].getValueAt(frame)[0]))
                filePy.write("cmds.setAttr(locator[0]+'.rotateX', "+roX+")\n")
                filePy.write("cmds.setKeyframe(locator[0]+'.rx')\n")
                
                # rotateY
                roY = str(float(node['rotate'].getValueAt(frame)[1]))
                filePy.write("cmds.setAttr(locator[0]+'.rotateY', "+roY+")\n")
                filePy.write("cmds.setKeyframe(locator[0]+'.ry')\n")
                
                # rotateZ
                roZ = str(float(node['rotate'].getValueAt(frame)[2]))
                filePy.write("cmds.setAttr(locator[0]+'.rotateZ', "+roZ+")\n")
                filePy.write("cmds.setKeyframe(locator[0]+'.rz')\n")

                # scaleX
                scX = str(float(node['scaling'].getValueAt(frame)[0]))
                filePy.write("cmds.setAttr(locator[0]+'.scaleX', "+scX+")\n")
                filePy.write("cmds.setKeyframe(locator[0]+'.sx')\n")
                
                # scaleY
                scY = str(float(node['scaling'].getValueAt(frame)[1]))
                filePy.write("cmds.setAttr(locator[0]+'.scaleY', "+scY+")\n")
                filePy.write("cmds.setKeyframe(locator[0]+'.sy')\n")
                
                # scaleZ
                scZ = str(float(node['scaling'].getValueAt(frame)[2]))
                filePy.write("cmds.setAttr(locator[0]+'.scaleZ', "+scZ+")\n")
                filePy.write("cmds.setKeyframe(locator[0]+'.sz')\n")

                # rotation order
                rotOrderL = {'XYZ':0,'YZX':1,'ZXY':2,'XZY':3,'YXZ':4,'ZYX':5}
                rotOrder = str(int(rotOrderL[node['rot_order'].value()]))
                filePy.write("cmds.setAttr(locator[0]+'.rotateOrder', "+rotOrder+")\n\n")
                
            filePy.write("cmds.rename(locator[0], '"+node.name()+"')\n")
            filePy.write("locatorList.append('"+node.name()+"')\n\n")
            
            filePy.write("cmds.currentTime("+str(startFrame)+")\n\n")

        filePy.write("cmds.select(cl = True)\n")
        filePy.write("for loc in locatorList:\n")
        filePy.write("	cmds.select(loc, add = True)\n")
        filePy.write("cmds.group(name = 'locators_GRP')\n")
        filePy.write("cmds.select(cl = True)\n\n")

    def exportCam(self, filePy, cameras, filePath, startFrame, lastFrame):

        filePy.write("# creating cameras ... \n\n")

        filePy.write("camerasList = []\n\n")

        for node in cameras:
            
            print "processing "+node.name()+" ..."
            
            if node.knob('read_from_file'):
                if node['read_from_file'].value() == 1:
                    node['read_from_file'].setValue(0)
            
            camName = str(node.name())
            filePy.write("##############\n")
            filePy.write("# creating the camera: "+node.name()+"\n")
            filePy.write("##############\n\n")
            #filePy.write("# "+reafFilePath+"\n\n")
            filePy.write("camera = cmds.camera()\n")
            
            for frame in range(startFrame, lastFrame+1):
                
                filePy.write("cmds.currentTime("+str(frame)+")\n")
                
                # translateX
                trX = str(self.getWorldMatrix(node, frame)[2][0])
                filePy.write("cmds.setAttr(camera[0]+'.translateX', "+trX+")\n")
                filePy.write("cmds.setKeyframe(camera[0]+'.tx')\n")
                
                # translateY
                trY = str(self.getWorldMatrix(node, frame)[2][1])
                filePy.write("cmds.setAttr(camera[0]+'.translateY', "+trY+")\n")
                filePy.write("cmds.setKeyframe(camera[0]+'.ty')\n")
                
                # translateZ
                trZ = str(self.getWorldMatrix(node, frame)[2][2])
                filePy.write("cmds.setAttr(camera[0]+'.translateZ', "+trZ+")\n")
                filePy.write("cmds.setKeyframe(camera[0]+'.tz')\n")
                
                # rotateX
                roX = str(self.getWorldMatrix(node, frame)[1][0])
                filePy.write("cmds.setAttr(camera[0]+'.rotateX', "+roX+")\n")
                filePy.write("cmds.setKeyframe(camera[0]+'.rx')\n")
                
                # rotateY
                roY = str(self.getWorldMatrix(node, frame)[1][1])
                filePy.write("cmds.setAttr(camera[0]+'.rotateY', "+roY+")\n")
                filePy.write("cmds.setKeyframe(camera[0]+'.ry')\n")
                
                # rotateZ
                roZ = str(self.getWorldMatrix(node, frame)[1][2])
                filePy.write("cmds.setAttr(camera[0]+'.rotateZ', "+roZ+")\n")
                filePy.write("cmds.setKeyframe(camera[0]+'.rz')\n")
                
                # wintranslateX
                winX = str(float(node['win_translate'].getValueAt(frame)[0]))
                filePy.write("cmds.setAttr(camera[1]+'.horizontalFilmOffset', "+winX+")\n")
                filePy.write("cmds.setKeyframe(camera[1]+'.filmTranslateH')\n")

                # wintranslateY
                winY = str(float(node['win_translate'].getValueAt(frame)[1]))
                filePy.write("cmds.setAttr(camera[1]+'.verticalFilmOffset', "+winY+")\n")
                filePy.write("cmds.setKeyframe(camera[1]+'.filmTranslateV')\n")

                # focal length
                focalLength = str(float(node['focal'].getValueAt(frame)))
                filePy.write("cmds.setAttr(camera[1]+'.focalLength', "+focalLength+")\n")
                filePy.write("cmds.setKeyframe(camera[1]+'.focalLength')\n")
                
                # rotation order
                rotOrderL = {'XYZ':0,'YZX':1,'ZXY':2,'XZY':3,'YXZ':4,'ZYX':5}
                rotOrder = str(int(rotOrderL[node['rot_order'].value()]))
                filePy.write("cmds.setAttr(camera[0]+'.rotateOrder', "+rotOrder+")\n\n")
            
            # hap and vap	
            hAp = float(node['haperture'].getValue())
            vAp = float(node['vaperture'].getValue())
            
            mayaHap = str(hAp*0.0393700787)
            mayaVap = str(vAp*0.0393700787)
            
            filePy.write("cmds.setAttr(camera[1]+'.horizontalFilmAperture', "+mayaHap+")\n")
            filePy.write("cmds.setAttr(camera[1]+'.verticalFilmAperture', "+mayaVap+")\n\n")
            
            # farClip
            farClip = str(float(node['far'].getValueAt(frame)))
            filePy.write("cmds.setAttr(camera[1]+'.farClipPlane', "+farClip+")\n")
            
            # farClip
            nearClip = str(float(node['near'].getValueAt(frame)))
            filePy.write("cmds.setAttr(camera[1]+'.nearClipPlane', "+nearClip+")\n\n")
            
            filePy.write("cmds.rename(camera[0], '"+node.name()+"')\n")
            filePy.write("camerasList.append('"+node.name()+"')\n\n")
            
            filePy.write("cmds.currentTime("+str(startFrame)+")\n\n")
            
        filePy.write("cmds.select(cl = True)\n")
        filePy.write("for cam in camerasList:\n")
        filePy.write("	cmds.select(cam, add = True)\n")
        filePy.write("cmds.group(name = 'cameras_GRP')\n")
        filePy.write("cmds.select(cl = True)\n\n")

    def exportCam_old(self, filePy, cameras, filePath, startFrame, lastFrame):

        filePy.write("# creating cameras ... \n\n")

        filePy.write("camerasList = []\n\n")

        for node in cameras:
            
            print "processing "+node.name()+" ..."
            
            if node.knob('read_from_file'):
                if node['read_from_file'].value() == 1:
                    node['read_from_file'].setValue(0)
            
            camName = str(node.name())
            filePy.write("##############\n")
            filePy.write("# creating the camera: "+node.name()+"\n")
            filePy.write("##############\n\n")
            #filePy.write("# "+reafFilePath+"\n\n")
            filePy.write("camera = cmds.camera()\n")
            
            for frame in range(startFrame, lastFrame+1):
                
                filePy.write("cmds.currentTime("+str(frame)+")\n")
                
                # translateX
                trX = str(float(node['translate'].getValueAt(frame)[0]))
                filePy.write("cmds.setAttr(camera[0]+'.translateX', "+trX+")\n")
                filePy.write("cmds.setKeyframe(camera[0]+'.tx')\n")
                
                # translateY
                trY = str(float(node['translate'].getValueAt(frame)[1]))
                filePy.write("cmds.setAttr(camera[0]+'.translateY', "+trY+")\n")
                filePy.write("cmds.setKeyframe(camera[0]+'.ty')\n")
                
                # translateZ
                trZ = str(float(node['translate'].getValueAt(frame)[2]))
                filePy.write("cmds.setAttr(camera[0]+'.translateZ', "+trZ+")\n")
                filePy.write("cmds.setKeyframe(camera[0]+'.tz')\n")
                
                # rotateX
                roX = str(float(node['rotate'].getValueAt(frame)[0]))
                filePy.write("cmds.setAttr(camera[0]+'.rotateX', "+roX+")\n")
                filePy.write("cmds.setKeyframe(camera[0]+'.rx')\n")
                
                # rotateY
                roY = str(float(node['rotate'].getValueAt(frame)[1]))
                filePy.write("cmds.setAttr(camera[0]+'.rotateY', "+roY+")\n")
                filePy.write("cmds.setKeyframe(camera[0]+'.ry')\n")
                
                # rotateZ
                roZ = str(float(node['rotate'].getValueAt(frame)[2]))
                filePy.write("cmds.setAttr(camera[0]+'.rotateZ', "+roZ+")\n")
                filePy.write("cmds.setKeyframe(camera[0]+'.rz')\n")
                
                # wintranslateX
                winX = str(float(node['win_translate'].getValueAt(frame)[0]))
                filePy.write("cmds.setAttr(camera[1]+'.horizontalFilmOffset', "+winX+")\n")
                filePy.write("cmds.setKeyframe(camera[1]+'.filmTranslateH')\n")

                # wintranslateY
                winY = str(float(node['win_translate'].getValueAt(frame)[1]))
                filePy.write("cmds.setAttr(camera[1]+'.verticalFilmOffset', "+winY+")\n")
                filePy.write("cmds.setKeyframe(camera[1]+'.filmTranslateV')\n")

                # focal length
                focalLength = str(float(node['focal'].getValueAt(frame)))
                filePy.write("cmds.setAttr(camera[1]+'.focalLength', "+focalLength+")\n")
                filePy.write("cmds.setKeyframe(camera[1]+'.focalLength')\n")
                
                # rotation order
                rotOrderL = {'XYZ':0,'YZX':1,'ZXY':2,'XZY':3,'YXZ':4,'ZYX':5}
                rotOrder = str(int(rotOrderL[node['rot_order'].value()]))
                filePy.write("cmds.setAttr(camera[0]+'.rotateOrder', "+rotOrder+")\n\n")
            
            # hap and vap	
            hAp = float(node['haperture'].getValue())
            vAp = float(node['vaperture'].getValue())
            
            mayaHap = str(hAp*0.0393700787)
            mayaVap = str(vAp*0.0393700787)
            
            filePy.write("cmds.setAttr(camera[1]+'.horizontalFilmAperture', "+mayaHap+")\n")
            filePy.write("cmds.setAttr(camera[1]+'.verticalFilmAperture', "+mayaVap+")\n\n")
            
            # farClip
            farClip = str(float(node['far'].getValueAt(frame)))
            filePy.write("cmds.setAttr(camera[1]+'.farClipPlane', "+farClip+")\n")
            
            # farClip
            nearClip = str(float(node['near'].getValueAt(frame)))
            filePy.write("cmds.setAttr(camera[1]+'.nearClipPlane', "+nearClip+")\n\n")
            
            filePy.write("cmds.rename(camera[0], '"+node.name()+"')\n")
            filePy.write("camerasList.append('"+node.name()+"')\n\n")
            
            filePy.write("cmds.currentTime("+str(startFrame)+")\n\n")
            
        filePy.write("cmds.select(cl = True)\n")
        filePy.write("for cam in camerasList:\n")
        filePy.write("	cmds.select(cam, add = True)\n")
        filePy.write("cmds.group(name = 'cameras_GRP')\n")
        filePy.write("cmds.select(cl = True)\n\n")

    def exportLights(self, filePy, lights, filePath, startFrame, lastFrame):

        filePy.write("# creating lights ... \n\n")

        filePy.write("lightsList = []\n\n")

        for light in lights:
            print light.name()
        
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
        
        return scale, rotate, translate

def exportToMayaUI():

    if os.name == 'posix':
        
        mayaVersion = os.environ['MAYA_VERSION']
        platform = os.environ['PLATFORM']
        mayapy = '/software/maya/'+mayaVersion+'/'+platform+'/bin/mayapy'
        
        # collect info for each open maya
        # test all maya found between port 9700-9711 and ask for the actual job, shot, host ...
        
        host = os.environ['HOSTNAME']

        for port in range (9700, 9711):
            try:
                maya = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                maya.connect((host,port))
                
                message = 'python ("import mpc.nuke.dmpTools.tools.askMaya as askMaya");'
                message += 'python ("askMaya.writeToFile()");'
                
                maya.send(message)
                maya.close()
                print "gather maya:"+str(port)+" infos..."
            except:
                pass
            
        #---------

    if os.name == 'nt':
        panel = nuke.Panel('please give me the path of mayapy.exe')
        panel.addFilenameSearch("mayapy.exe: ","")
        val = panel.show()
        if val:
            mayapy = panel.value("mayapy.exe: ")

    selOriginal = nuke.selectedNodes()

    for item in selOriginal:
        try:
            if item['disable'].value() == 1:
                item['selected'].setValue(0)
        except:
            continue

    sel = nuke.selectedNodes()

    if os.path.exists(mayapy):
        
        if sel:
            panel = nuke.Panel("Export stuff from nuke to maya")
            panel.setWidth(400)
            panel.addFilenameSearch("Maya output file: ","")
            panel.addBooleanCheckBox("Save obj files ? (also save .obj separately)", 0)
            if os.name == 'posix':
                panel.addBooleanCheckBox("Send to Maya ?", 0)
            retVar = panel.show()
            if retVar == 1:
                
                cameras = []
                objects = []
                axiis = []
                lights = []
                
                for node in sel:
                    
                    goodCam = ["Camera2","Camera", "hubCamera"]
                    goodGeo = ["ReadGeo","ReadGeo2","Sphere","Cube","Cylinder","Card", "Card2", "LookupGeo", "UVProject", "TransformGeo", "MergeGeo", "ApplyMaterial", "GiggleGeoLoader"]
                    goodAxis = ["Axis", "Axis2"]
                    goodLights = ["Spotlight", "Light", "DirectLight"]
                    
                    if node.Class() in goodCam:
                        cameras.append(node)
                    if node.Class() in goodGeo:
                        objects.append(node)			
                    if node.Class() in goodAxis:
                        axiis.append(node)
                    if node.Class() in goodLights:
                        lights.append(node)
                
                outputFile = panel.value("Maya output file: ")
                
                if outputFile.split('.')[-1] == "ma":
                    if os.name == 'posix':
                        ExportToMaya(mayapy, objects, cameras, axiis, lights, outputFile, panel.value("Save obj files ? (also save .obj separately)"), panel.value("Send to Maya ?"))
                    if os.name == 'nt':
                        ExportToMaya(mayapy, objects, cameras, axiis, lights, outputFile, panel.value("Save obj files ? (also save .obj separately)"), False)
                else:
                    nuke.message('the output file is not correct !\nex: /path/mayafile.ma')
            else:
                print "abort..."
            
            #for node in selOriginal:
            #	node['selected'].setValue(1)
            for node in sel:
                node['selected'].setValue(1)
                
        else:
            nuke.message("select some stuff !")
    else:
        nuke.message("I can't find the mayapy binary. It's crucial to create ma files !")
