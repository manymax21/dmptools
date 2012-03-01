import os
import sys
import time

import maya.cmds as cmds

class Utils(object):
    """
        some utility methods for mayaToNuke tool
    """
    def __init__(self):
        # os infos
        self.os = os.name
        self.platform = sys.platform
        self.user = os.environ['USERNAME']
        self.panelsDisplay = {}
        # maya display
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

    def getTime(self, arg=''):
        # get time
        if arg == 'str':
            timeStr = str(time.strftime('%d/%m/%y at %H:%M:%S'))
            return timeStr
        if arg == 'current':
            currTime = time.strftime('%d%m%y_%H%M%S')
            return currTime

    def getFramerange(self, arg=''):
        """
            return the actual frame, first and last frame.
        """
        if arg == 'currentFrame':
            current = int(cmds.currentTime(q = True))
            return current
        if arg == 'first':
            first = int(cmds.playbackOptions(q = True, min = True))
            return first
        if arg == 'last':
            last = int(cmds.playbackOptions(q = True, max = True))
            return last
        if arg == 'frames':
            frames = int((last - first) + 1)
            return frames

    def strFromList(self, inputlist=[]):
        """
            return twoo from a given list.
            [0] is a straight string line
            [1] is a string with break lines.
        """
        return ''.join(inputlist), '    - '+'\n    - '.join(inputlist)

    def filterSelection(self):
        """
            from a raw list of items, returns 4 lists:
            (objects, cameras, locators, lights)
        """
        # get selection
        cmds.select(hi = True)
        selection = [str(item) for item in cmds.ls(sl = True)]

        # fill the 4 lists from the raw selection
        meshes = [cmds.listRelatives(node, p = True)[0] for node in selection if cmds.nodeType(node) == "mesh"]
        cameras = [cmds.listRelatives(node, p = True)[0] for node in selection if cmds.nodeType(node) == "camera"]
        locators = [cmds.listRelatives(node, p = True)[0] for node in selection if cmds.nodeType(node) == "locator"]
        lights = [cmds.listRelatives(node, p = True)[0] for node in selection if 'Light' in cmds.nodeType(node)]
        
        return (meshes, cameras, locators, lights)

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

