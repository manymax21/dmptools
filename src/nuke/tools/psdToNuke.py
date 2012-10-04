#============================================
#
# michael-ha@moving-picture.com
# psd 'reader' for nuke
# create cropped cards from psd layers
# posix, nt supported
#
#============================================

import os
import sys
import re
import time
import nuke
import nukescripts
import commands as cmd
from nukescripts import PythonPanel
from stat import S_ISREG, ST_MTIME, ST_MODE

class Psdutils:
    'psd2nuke utility functions'
    
    def __init__(self):
        pass
        
    def getEnvVar(self, osname):
        
        if osname == 'posix':
            try:
                user = os.environ['USER']
            except:
                user = 'n/a'
            try:
                job = os.environ['JOB']
            except:
                job = 'n/a'
            try:
                shot = os.environ['SHOTNAME']
            except:
                shot = 'n/a'
            try:
                scene = os.environ['SCENE']
            except:
                scene = 'n/a'
            try:
                discipline = os.environ['DISCIPLINE']
            except:
                discipline = 'n/a'
            
        if osname == 'nt':
            USER = os.popen("echo %USERNAME%")
            user,  job, shot, scene, discipline = USER.read(), 'n/a', 'n/a', 'n/a', 'n/a'
            USER.close()
    
        return user, job, shot, scene, discipline
    
    def unselectAll(self):
        for node in nuke.allNodes():
            node.knob('selected').setValue(False)

    def selectReplace(self, node):
        for n in nuke.allNodes():
            n.knob('selected').setValue(False)
        node['selected'].setValue(True)

    def selectAdd(self, node):
        if type(node).__name__ == 'list':
            for n in node:
                n.knob('selected').setValue(True)
        else:
            node.knob('selected').setValue(True)

    def autoplace(self, nodes):
        for node in nodes:
            nuke.autoplace(node)
    
    def logToLin(self, nodes):

        convertnodes = []
        
        for node in nodes:
            
            self.selectReplace(node)
            convertnode = nuke.createNode('MPC_ColIO_!MPC_COLIO_VERSION!', inpanel = False)
            convertnode['inspace'].setValue('Log')
            convertnode['output_space'].setValue('Linear')
            convertnodes.append(convertnode)
        return convertnodes
        
class PsdToNuke_2d:
    
    def __init__(self, dir = None, useSel = 1, mode = '2d', log2lin = 0):
        'psd2nuke 2d default values and variables'
        
        self.mode = mode
        self.path = dir
        self.useSel = useSel
        self.convert = log2lin
        self.mergeOp = ('atop', 'average', 'color-burn', 'color-dodge', 'conjoint-over', 'copy', 'difference', 'disjoint-over', 
                    'divide', 'exclusion', 'from', 'geometric', 'hard-light', 'hypot', 'in', 'mask', 'matte', 'max', 'min', 'minus',
                    'multiply', 'out', 'over', 'overlay', 'plus', 'screen', 'soft-light', 'stencil', 'under', 'xor')
    
    def build2d(self):
    
        'start the creation process'

        # using path filled by user
        if self.useSel == 0:
            
            # get all entries in the directory w/ stats
            entries = (os.path.join(self.path, fn) for fn in os.listdir(self.path))
            entries = ((os.stat(path), path) for path in entries)

            # leave only regular files, insert creation date
            entries = ((stat[ST_MTIME], path) for stat, path in entries if S_ISREG(stat[ST_MODE]))
            
            files = [os.path.basename(path) for cdate, path in sorted(entries)]

            #self.layers = cmd.getstatusoutput('ls -1tr '+self.path+'')[1]
            #self.layersL = cmd.getstatusoutput('ls -1tr '+self.path+'')[1].split('\n')
            
            # create read node for each layer
            self.readnodes = self.createReadNodes(files)

        #using node selection instead of path
        if self.useSel == 1:
            
            nodes = nuke.selectedNodes()
            readnames = []
            for node in nodes:
                
                # searche the correct order
                file = node.knob('file').value().split('/')[-1].split('.')[0]
                ext = node.knob('file').value().split('/')[-1].split('.')[1]
                pattern = re.compile(r'^\w*layer_(\d{4})\w*$')
                output = pattern.search(file).groups()
                readnames.append('%s_%s' %(output[0], node.name()))
                
            readnames.sort()	
            
            self.readnodes = [nuke.toNode(readname[5:]) for readname in readnames]
            
        # convert log to lin if selected
        if self.convert:
            # unpremult white
            self.unpremultnodes0 = self.unpremultLayers(self.readnodes)
            self.unpremultnodes = Psdutils().logToLin(self.unpremultnodes0)
        else:
            # unpremult white
            self.unpremultnodes = self.unpremultLayers(self.readnodes)
            
        # premult the alpha channel
        self.premultnodes = self.premultLayers(self.unpremultnodes)

        # autocrop premult nodes
        self.autocropnodes = []
        for node in self.premultnodes:
            
            Psdutils().selectReplace(node)
            autocropnode = self.autocropLayers()
            self.autocropnodes.append(autocropnode)
        
        # merge and return the nodes
        
        if self.mode == '2d' and self.convert:

            # tranform layers
            self.transforms = self.transformLayers(self.autocropnodes)

            #  merge layers
            self.mergenodes = self.mergeLayers(self.transforms)
            
            # select all nodes autoplace and backdrop
            self.backdrop = self.autoLayoutNodes()
        
            return self.readnodes, self.unpremultnodes, self.unpremultnodes0, self.premultnodes, self.autocropnodes, self.transforms, self.mergenodes, self.backdrop
            
        if self.mode == '2d' and not self.convert:

            # tranform layers
            self.transforms = self.transformLayers(self.autocropnodes)

            #  merge layers
            self.mergenodes = self.mergeLayers(self.transforms)
            
            # select all nodes autoplace and backdrop
            self.backdrop = self.autoLayoutNodes()
        
            return self.readnodes, self.unpremultnodes, self.premultnodes, self.autocropnodes, self.transforms, self.mergenodes, self.backdrop
            
        if not self.mode == '2d' and self.convert:
            
            return self.readnodes, self.unpremultnodes, self.unpremultnodes0, self.premultnodes, self.autocropnodes
            
        if not self.mode == '2d' and not self.convert:
            
            return self.readnodes, self.unpremultnodes, self.premultnodes, self.autocropnodes
            
            
    def createReadNodes(self, files):
        
        readNodes = []
        
        for file in files:
            
            pattern = re.compile(r'^\w*layer_(\d{4})\w*\.\w*$')
            
            if pattern.search(file):
                
                fileName = file.split('.')[0]
                readNode = nuke.createNode('Read', inpanel = False)
                readNodes.append(readNode)
                readNode.knob('file').setValue(self.path+'/'+file)
                readNode.setName(fileName)
                if self.convert == 0:
                    readNode.knob('colorspace').setValue(0)
                    readNode.knob('raw').setValue(0)
                if self.convert == 1:
                    readNode.knob('raw').setValue(1)
            
        return readNodes
    
    def unpremultLayers(self, nodes):
        
        unpremultnodes = []
        
        for node in nodes:
            Psdutils().selectReplace(node)
            unpremultnode = nuke.createNode('Expression', inpanel = False)
            unpremultnode.setName('unpremult white')
            unpremultnode['expr0'].setValue("a>0?(r-(1-a))/a:r")
            unpremultnode['expr1'].setValue("a>0?(g-(1-a))/a:g")
            unpremultnode['expr2'].setValue("a>0?(b-(1-a))/a:b")
            unpremultnode['expr3'].setValue("a")
            
            unpremultnodes.append(unpremultnode)
        
        return unpremultnodes
    
    def premultLayers(self, nodes):
        
        premults = []
        
        for node in nodes:
            Psdutils().selectReplace(node)
            premult = nuke.createNode('Premult', inpanel = False)
            premults.append(premult)
            
        return premults
        
    def autocropLayers(self, first=None, last=None, inc=None, layer="rgba"):
        
        root = nuke.root()
        if first is None:
            first = int(root.knob("first_frame").value())
        if last is None:
            last = int(root.knob("first_frame").value())
        if inc is None:
            inc = 1
        original_nodes = nuke.selectedNodes()
        all_nodes = nuke.allNodes()
        for i in all_nodes:
            i.knob("selected").setValue(False)
        for i in original_nodes:
            i.knob("selected").setValue(True)
            autocropper = nuke.createNode("CurveTool", '''operation 0 ROI {0 0 input.width input.height} Layer %s label "Processing Crop..." selected true''' % (str(layer), ), False)
            nuke.executeMultiple([autocropper,], ([first, last, inc],))
            autocropper.knob("selected").setValue(True)
            cropnode = nuke.createNode("Crop", "label AutoCrop", False)
            cropbox = cropnode.knob("box");
            autocropbox = autocropper.knob("autocropdata");
            cropbox.copyAnimations(autocropbox.animations())
            cropnode.knob("indicators").setValue(1)
            all_nodes = nuke.allNodes()
            for j in all_nodes:
                j.knob("selected").setValue(False)
            autocropper.knob("selected").setValue(True)
            nukescripts.node_delete()
            all_nodes = nuke.allNodes()
            for j in all_nodes:
                j.knob("selected").setValue(False)
            nuke.autoplace(cropnode)
            cropnode.knob("selected").setValue(True)
            cropnode.knob("reformat").setValue(True)
            nuke.autoplace(cropnode)
            
        return cropnode
        
    def transformLayers(self, nodes):
        
        transforms = []
        for node in nodes:
            
            cropx = node['box'].getValue()[0]
            cropy = node['box'].getValue()[1]
            
            Psdutils().selectReplace(node)
            transform = nuke.createNode("Transform",inpanel = False)
            transform.setName('Transform')
            transform['translate'].setValue([cropx,cropy])

            transforms.append(transform)
            
        return transforms

    def mergeLayers(self, nodes):
    
        # invert nodes order
        nodes = nodes[::-1]

        mergenodes = []
        ID = 1
        Psdutils().selectReplace(nodes[0])
        
        while ID <= len(nodes)-1:
            Psdutils().selectAdd(nodes[ID])
            merge = nuke.createNode('Merge', inpanel = False)
            nukescripts.swapAB(merge)
            mergenodes.append(merge)
            Psdutils().selectReplace(merge)
            ID = ID+1
            
        return mergenodes

    def autoLayoutNodes(self):
        
        Psdutils().unselectAll()
        Psdutils().selectAdd(self.readnodes)
        try:
            Psdutils().selectAdd(self.unpremultnodes0)
        except:
            pass
        Psdutils().selectAdd(self.unpremultnodes)
        Psdutils().selectAdd(self.premultnodes)
        Psdutils().selectAdd(self.autocropnodes)
        Psdutils().selectAdd(self.transforms)
        Psdutils().selectAdd(self.mergenodes)
        try:
            _autoplace()
        except:
            Psdutils().autoplace(nuke.selectedNodes())

        backdrop2d = nukescripts.autoBackdrop()
        backdrop2d.setName('toto')
        
        return backdrop2d
    
class PsdToNuke_uv:
    
    def __init__(self, dir = None, useSel = 1, mode = 'uv', log2lin = 0):
        'psd2nuke 3d uv cards default values and variables'
        
        self.mode = mode
        self.path = dir
        self.useSel = useSel
        self.convert = log2lin		
            
        self.readnodes, self.unpremultnodes,self.convertnodes, self.premultnodes, self.autocropnodes = PsdToNuke_2d(self.path, self.useSel, self.mode, self.convert).build2d()
        
        self.cards, self.xformgeos = self.createCards(self.autocropnodes)

    def createCards(self, autocropnodes):
        
        cards = []
        xformgeos = []
        ID = 0
        trZ = 0
        
        for node in autocropnodes:
            
            Psdutils().selectReplace(node)
            
            X, Y, w, h, r, t, trX, trY, scaleX, scaleY, cardcol, cardrow = self.getXform(node, ID)
            
            card = nuke.createNode('Card2', inpanel = False)
            card.knob('rows').setValue(cardrow)
            card.knob('columns').setValue(cardcol)
            card.knob('image_aspect').setValue(0)
            cards.append(card)
            
            tr3d = nuke.createNode('TransformGeo', inpanel = False)			
            tr3d.knob('translate').setValue([trX, trY, trZ])
            tr3d.knob('scaling').setValue([scaleX, scaleY, 1])
            
            xformgeos.append(tr3d)
            ID = ID+1
            trZ = trZ-1.5
            
        return cards, xformgeos
        
    def getXform(self, node, ID):
    
        X, Y = self.readnodes[ID].width(), self.readnodes[ID].height()
        w, h = int(node.knob('box').getValue()[0]), int(node.knob('box').getValue()[1])
        r, t = int(node.knob('box').getValue()[2]), int(node.knob('box').getValue()[3])

        if r == 0:
            r = X
        if t == 0:
            t = Y

        #~ trX = int((-X/2)+(w+(r-w))/2)
        #~ trY = int((-Y/2)+(h+(t-h))/2)
        
        trX = int((-X+(r-w)+(w*2))/2)
        trY = int((-Y+(t-h)+(h*2))/2)
        
        scaleX = r-w
        scaleY = t-h
        
        cardcol, cardrow = 10, int(10.0/(float(scaleX)/float(scaleY)))

        return X, Y, w, h, r, t, trX, trY, scaleX, scaleY, cardcol, cardrow
        
class PsdToNuke_proj:
    
    def __init__(self, dir = None, useSel = 1, mode = 'proj', log2lin = 0):
        'psd2nuke 3d projection cards default values and variables'
        
        self.mode = mode
        self.path = dir
        self.useSel = useSel
        self.convert = log2lin
        
        self.readnodes, self.premultnodes, self.autocropnodes = PsdToNuke_2d(self.path, self.useSel, self.mode).build2d()
    

class PsdToNukeUI:
    
    def __init__(self):
        
        osname = os.name

        self.user, self.job, self.shot, self.scene, self.discipline = Psdutils().getEnvVar(osname)
        
        self.buildPanel()

    def buildPanel(self):
        
        if nuke.selectedNodes():
            useCheck = 1
        else:
            useCheck = 0
        
        # define panel labels
        titleLabel = self.user+' : Psd layers to Nuke - '+self.job+' '+self.shot
        dirLabel = 'Layers directory:'
        useSelLabel = 'Use selected nodes'
        lin2logLabel = 'Convert to Linear'
        modeLabel = 'Mode:'

        # building panel
        panel = nuke.Panel(titleLabel, 450)
        panel.addClipnameSearch(dirLabel, '/mpc/lot10/training/environment/psdToNuke/maya/textures/images/env/psd/psdToNuke_example/layers/')
        panel.addBooleanCheckBox(useSelLabel, useCheck)
        panel.addBooleanCheckBox(lin2logLabel, 0)
        panel.addEnumerationPulldown(modeLabel, '2d uv-cards proj-cards')
        
        #show the panel
        returnValue = panel.show()
        if returnValue:
            
            # get panel values
            dir = panel.value(dirLabel)
            useSel = panel.value(useSelLabel)
            mode = panel.value(modeLabel)
            log2lin = panel.value(lin2logLabel)
            
            if not dir and useSel == 1 or dir and not useSel or dir and useSel == 1:				
                if mode == '2d':
                    PsdToNuke_2d(dir, useSel, mode, log2lin).build2d()
                if mode == 'uv-cards':
                    mode = 'uv'
                    PsdToNuke_uv(dir, useSel, mode, log2lin)					
                if mode == 'proj-cards':
                    mode = 'proj'
                    PsdToNuke_proj(dir, useSel, mode, log2lin)
                
            if not dir and useSel == 0:				
                nuke.message('you need to specify the layers directory !')
            
        else:
            print 'abort'
            
def psdToNuke():
    PsdToNukeUI()