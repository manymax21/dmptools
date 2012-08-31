import maya.cmds as cmds
import maya.mel as mel

class Extract(object):
    def __init__(self):
        self.original = cmds.ls(sl=True)

    def start(self, none=None):
        """start the extraction process"""
        original_mesh = self.original[0]
        original = cmds.duplicate()[0]
        # get UI values
        polycount = int(cmds.textFieldGrp('polycount', text=True, q=True))
        projectUV = cmds.checkBox('project', value=True, q=True)
        scaleUV = float(cmds.textFieldGrp('scaleUV', text=True, q=True))
        smooth = float(cmds.checkBox('smooth', value=True, q=True))
        smoothValue = float(cmds.textFieldGrp('smoothValue', text=True, q=True))
        keepOriginal = cmds.checkBox('keepOriginal', value=True, q=True)
        # keep original if needed
        if keepOriginal:
            cmds.duplicate()
        # prepare geo
        cmds.select(original, r=True)
        self.prepare_geo(original, smooth, smoothValue, projectUV, scaleUV)
        # duplicate the geo for normal transfer and reselect the original node
        cmds.select(original, r=True)
        tmp_geo = cmds.duplicate()[0]
        cmds.select(original, r=True)
        # while true, extract parts and fill {parts}
        parts = {}
        loop=True
        i = 0
        print '> extracting...'
        while loop:
            try:
                print ' ', i
                parts[i] = self.extract_part(cmds.ls(sl=True)[0], polycount)
            except:
                loop=False
            i += 1
        # clean (delete empty groups, group parts and transfer normals)
        self.clean_parts(parts, tmp_geo)
        cmds.delete(tmp_geo)
        cmds.delete(original)
        cmds.delete(original_mesh)
        # close the ui at the end
        cmds.deleteUI('separateUI')

        print '> done.'

    def prepare_geo(self, original, smooth, smoothValue, projectUV, scaleUV):
        if smooth:
            print '> smooth normals...'
            cmds.polySoftEdge(a=smoothValue, ch=False) 
        if projectUV:
            print '> project uvs...'
            cmds.polyProjection(original+'.f[*]',
                                    ch=False,
                                    type='Planar',
                                    ibd=True,
                                    isu=scaleUV,
                                    isv=scaleUV,
                                    md='y')
        cmds.select(original, r=True)

    def extract_part(self, mesh, polycount):
        # grow selection
        cmds.select(mesh+'.f[1]')
        while cmds.polyEvaluate(tc=True) < polycount:
            mel.eval('GrowPolygonSelectionRegion;')
        # extract
        cmds.polyChipOff(ch=False, kft=True, dup=False, off=False)
        parts = cmds.polySeparate(mesh, ch=False)
        # select the mesh with the higher polycount
        nodes = {}
        for part in parts:
            nodes[mesh+'|'+part] = cmds.polyEvaluate(part, f=True)
        sortList = nodes.values()
        sortList.sort()
        key = [key for key in nodes.keys() if nodes[key] == sortList[-1]]
        cmds.select(key)
        # return created parts
        return nodes.keys()

    def clean_parts(self, parts, mesh):
        # group parts
        cmds.select(clear=True)
        [[cmds.select(node, add=True) for node in part] for part in parts.values()]
        cmds.group(n='terrain_grp')
        cmds.parent(w=True)
        partsList = cmds.listRelatives(cmds.ls(sl=True), f=True)
        # delete empty groups and transfer normals
        i = 1
        for part in partsList:
            if cmds.listRelatives(part):
                newname = 'terrain_part'+str(i)
                print '> transfering normals on', newname
                cmds.transferAttributes(mesh, part,
                                        transferPositions=0,
                                        transferNormals=1,
                                        transferUVs=0,
                                        transferColors=2,
                                        sampleSpace=0,
                                        sourceUvSpace="map1",
                                        targetUvSpace="map1",
                                        searchMethod=3,
                                        flipUVs=0,
                                        colorBorders=1)
                cmds.delete(part, ch=True)
                cmds.rename(part, newname)
                i += 1
            else:
                cmds.delete(part)

    def refresh(self, none=None):
        sel = cmds.ls(sl=True)
        if sel:
            self.original = sel
            cmds.window('separateUI', t='Separate: '+self.original[0], e=True)

    def closeUI(self, none=None):
        """close the UI"""
        cmds.deleteUI('separateUI')

    def UI(self, mesh):

        # delete window if exists
        if cmds.window('separateUI', exists=True):
            cmds.deleteUI('separateUI', window=True)
        
        win = cmds.window('separateUI', t='Separate: '+mesh, s=False)
        form = cmds.formLayout()
        separator1 = cmds.separator('separator1', style='single')
        polycount = cmds.textFieldGrp('polycount',
                                    label='poly-count limit per part:',
                                    text='5000' )
        smoothCmd = 'import maya.cmds as cmds;cmds.textFieldGrp("smoothValue", e=True,\
                    enable=cmds.checkBox("smooth", value=True, q=True))'
        smooth = cmds.checkBox('smooth',
                                    label='smooth normals',
                                    value=True,
                                    cc=smoothCmd)
        smoothValue = cmds.textFieldGrp('smoothValue',
                                    label='smooth Value:',
                                    text='80',
                                    enable=True)
        projectCmd = 'import maya.cmds as cmds;cmds.textFieldGrp("scaleUV",\
                    e=True, enable=cmds.checkBox("project", value=True, q=True))'
        projectUV = cmds.checkBox('project',
                                    label='project UV on Y',
                                    value=True,
                                    cc=projectCmd)
        scaleUV = cmds.textFieldGrp('scaleUV',
                                    label='UV scale:',
                                    text='1.0',
                                    enable=True)
        keepOriginal = cmds.checkBox('keepOriginal',
                                    label='keep original mesh',
                                    value=True)
        refreshButton = cmds.button('refreshButton',
                                    label="Refresh selection",
                                    c=self.refresh)
        okButton = cmds.button('okbutton',
                                    label="Go!",
                                    c=self.start)
        cancelButton = cmds.button('cancelbutton',
                                    label="Cancel",
                                    c=self.closeUI)
        tab = 150
        cmds.formLayout(form, e=True,
                        attachForm = 
                                [
                                    (polycount, 'top', 5),
                                    (polycount, 'left', 5),
                                    (polycount, 'right', 5),
                                    (smooth, 'left', tab),
                                    (smooth, 'right', 5),
                                    (smoothValue, 'left', 5),
                                    (smoothValue, 'right', 5),
                                    (projectUV, 'left', tab),
                                    (projectUV, 'right', 5),
                                    (scaleUV, 'left', 5),
                                    (scaleUV, 'right', 5),
                                    (keepOriginal, 'left', tab),
                                    (separator1, 'left', 5),
                                    (separator1, 'right', 5),
                                    (refreshButton, 'left', 5),
                                    (refreshButton, 'right', 5),
                                    (okButton, 'left', 5),
                                    (okButton, 'bottom', 5),
                                    (cancelButton, 'right', 5),
                                    (cancelButton, 'bottom', 5),

                                ],
                                    attachControl = 
                                [
                                    (smooth, 'top', 5, polycount),
                                    (smoothValue, 'top', 5, smooth),
                                    (projectUV, 'top', 5, smoothValue),
                                    (scaleUV, 'top', 5, projectUV),
                                    (keepOriginal, 'top', 5, scaleUV),
                                    (separator1, 'top', 5, keepOriginal),
                                    (refreshButton, 'top', 5, separator1),
                                    (okButton, 'top', 5, refreshButton),
                                    (cancelButton, 'top', 5, refreshButton),
                                ],
                                    attachPosition = 
                                [
                                    (okButton, "right", 5, 50),
                                    (cancelButton, "left", 5, 50)
                                ]
                            )
        cmds.showWindow()

def main():
    # start if something is selected
    extract = Extract()
    if extract.original:
        polycount = cmds.polyEvaluate(extract.original[0], t=True)
        confirm = 'Yes'
        if polycount > 150000:
            confirm = cmds.confirmDialog(t = "Warning! polycount: "+str(polycount)+" poly",
                                         m = 'This may take a while. Do you want to continue?',
                                         ma = "center",
                                         b = ['Yes','No'],
                                         db = 'Yes',
                                         cb = 'No',
                                         ds = 'No' )
        
        if confirm == 'Yes':
            extract.UI(extract.original[0])

if __name__ == '__main__':
    main()
