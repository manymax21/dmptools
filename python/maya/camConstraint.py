import maya.cmds as cmds

class camConstraintUI:

    def __init__(self):
        self.cameras = self.getSceneCameras()
        self.UIName='camConstraintUI'
        self.UI = self.createUI()
        self.menuUI = ''
        cmds.showWindow(self.UI)        

    def getSceneCameras(self):
        print 'Getting scene cameras ...'
        
        allCameras = cmds.ls(typ='camera')
        cameras = []
        for camera in allCameras:
            if cmds.getAttr('%s.orthographic' %camera) == False:
                cameras.append(self.getTransform(camera))
                
        return cameras
                
    def createUI(self):
        print 'creating UI'
        if cmds.window(self.UIName, exists = True):
            cmds.deleteUI(self.UIName, window = True)
        if cmds.windowPref(self.UIName, exists = True):
            cmds.windowPref(self.UIName, remove = True)

        ui = cmds.window(self.UIName, title = "Cam Constraint UI" )
        cmds.columnLayout(adj = True)
        self.menuUI = cmds.optionMenu(label='Constraint to camera :', cc=self.setPivotPoint)
        for cam in self.getSceneCameras():
            cmds.menuItem(label = cam)
            
        return ui

    def setPivotPoint(self,selectedCamera):
        print selectedCamera
        pivot = cmds.xform(selectedCamera, q=True, translation = True, ws = True)
        for mesh in self.getSelection():
            print mesh
            cmds.xform(mesh,scalePivot=pivot,ws = True)
        
    def getSelection(self):
        selectedMeshes = cmds.ls(selection = True,typ='mesh', o = True, dag=True)
        transforms = []
        for mesh in selectedMeshes:
            transforms.append (self.getTransform(mesh))
        return transforms
    def getTransform(self,dag):
        return cmds.listRelatives(dag,parent=True)[0]
    
camConstraintUI()
