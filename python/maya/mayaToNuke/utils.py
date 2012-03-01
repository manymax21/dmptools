import os
import sys
import time

import maya.cmds as cmds

from dmptools.presets import PresetsManager

PRESETS = PresetsManager()

class Utils(object):
    """
        some utility methods for mayaToNuke tool
    """
    def __init__(self):
        # os infos
        self.os = os.name
        self.platform = sys.platform
        self.user = os.getenv('USERNAME')
        self.computer = os.getenv('COMPUTERNAME')
        self.nukeexe = self.getNukeExe()
        # maya display infos
        self.panelsDisplay = {}
        self.modelPanelObjects = [
                    'cameras', 'deformers',
                    'dimensions', 'dynamics',
                    'fluids', 'follicles',
                    'hairSystems', 'handles',
                    'hulls', 'ikHandles',
                    'joints', 'lights',
                    'locators', 'manipulators',
                    'nCloths', 'nParticles',
                    'nRigids', 'nurbsCurves',
                    'nurbsSurfaces', 'pivots',
                    'planes', 'polymeshes',
                    'strokes', 'subdivSurfaces',
                    ]
        # set presets
        PRESETS.addPreset('user', self.user)
        PRESETS.addPreset('os', self.os)
        PRESETS.addPreset('platform', self.platform)
        
    def getTime(self, arg=''):
        # get time
        if arg == 'str':
            timeStr = str(time.strftime('%d/%m/%y at %H:%M:%S'))
            return timeStr
        if arg == 'current':
            currTime = time.strftime('%d%m%y_%H%M%S')
            return currTime

    def getFramerange(self):
        """
            return the actual frame, first and last frame.
        """
        framerange = {}
        framerange['current'] = int(cmds.currentTime(q = True))
        framerange['first'] = int(cmds.playbackOptions(q = True, min = True))
        framerange['last'] = int(cmds.playbackOptions(q = True, max = True))
        framerange['frames'] = int((framerange['last'] - framerange['first']) + 1)

        return framerange

    def strFromList(self, inputlist=[]):
        """
            return two from a given list.
            [0] is a straight string line
            [1] is a string with break lines.
        """
        return ''.join(inputlist), '    - '+'\n    - '.join(inputlist)

    def filterSelection(self):
        """
            from a raw list of items, returns 1 dict containing:
            {[objects], [cameras], [locators], [lights]}
        """
        # get selection
        cmds.select(hi = True)
        selection = [str(item) for item in cmds.ls(sl = True)]

        # fill the 4 lists from the raw selection
        meshes = [cmds.listRelatives(node, p = True)[0] for node in selection if cmds.nodeType(node) == "mesh"]
        cameras = [cmds.listRelatives(node, p = True)[0] for node in selection if cmds.nodeType(node) == "camera"]
        locators = [cmds.listRelatives(node, p = True)[0] for node in selection if cmds.nodeType(node) == "locator"]
        lights = [cmds.listRelatives(node, p = True)[0] for node in selection if 'Light' in cmds.nodeType(node)]
        
        items = \
            {
                'objects' : meshes,
                'cameras' : cameras,
                'locators' : locators,
                'lights' : lights,
            }

        return items

    def getDisplayItems(self):
        """
            fill self.panelsDisplay with the all panels found
            and the state value of all the items in them.
        """
        panels = cmds.getPanel(allPanels = True)
        for panel in panels:
            try:
                self.panelsDisplay[panel] = {}
                for object in self.modelPanelObjects:
                    self.panelsDisplay[panel][object] = eval("cmds.modelEditor('"+panel+"', query = True, "+object+" = True)")
            except:
                pass
        
    def setDisplayOn(self):
        """
           show all the stuff in the viewport 
        """
        for panel in self.panelsDisplay.keys():
            for object, value in self.panelsDisplay[panel].items():
                eval("cmds.modelEditor('"+panel+"', edit = True, "+object+" = "+str(value)+")")
    
    def setDisplayOff(self):
        """
            hide all the stuff in the viewport
        """
        for panel in self.panelsDisplay.keys():
            for object, value in self.panelsDisplay[panel].items():
                eval("cmds.modelEditor('"+panel+"', edit = True, "+object+" = False)")

    def getNukeExe(self):

        defaultNukePath = [
        'C:/Program Files/Nuke6.0v5/Nuke6.0.exe',
        'C:/Program Files/Nuke6.3v4/Nuke6.3.exe',
        'C:/Program Files (x86)/Nuke6.3v4/Nuke6.3.exe',
        ]
        for path in defaultNukePath:
            if os.path.exists(path):
                PRESETS.addPreset('nukeexe', path)
                
        # get the nuke path preset if exists
        nukeexe = PRESETS.getPreset('nukeexe')
        if nukeexe:
            if os.path.exists(nukeexe[0]):
                return nukeexe[0]
            else:
                raise UserWarning('No exe found !')
        else:
            # ask for the sublime text exe path
            filedialog = cmds.fileDialog2(cap='Please give me the path of Nuke.exe !',
                            fm=1,
                            dir='C:\\Program Files\\',
                            ff='*.exe')
            if filedialog:
                nukeexe = str(filedialog[0])
                if os.path.exists(nukeexe):
                    # setting preset
                    PRESETS.addPreset('nukeexe', nukeexe)
                    return nukeexe
                else:
                    raise UserWarning('No exe found !')
            else:
                raise UserWarning('No exe found !')
