import maya.cmds as cmds
import maya.mel as mel

def extract(obj, tri_limit):
    # grow selection
    cmds.select(obj+'.f[1]')
    while cmds.polyEvaluate(fc=True) < tri_limit:
        mel.eval('GrowPolygonSelectionRegion;')
    # extract
    cmds.polyChipOff(ch=False, kft=True, dup=False, off=False)
    parts = cmds.polySeparate(obj, ch=False)
    # select the mesh with the higher polycount
    nodes = {}
    for part in parts:
        nodes[obj+'|'+part] = cmds.polyEvaluate(part, f=True)
    sortList = nodes.values()
    sortList.sort()
    key = [key for key in nodes.keys() if nodes[key] == sortList[-1]]
    cmds.select(key)
    # return created parts
    return nodes.keys()

def clean_parts(nodes):
    # clean parts
    parts = nodes.values()
    cmds.select(clear=True)
    [[cmds.select(p, add=True) for p in part] for part in parts]
    cmds.group(n='terrain_grp')
    cmds.parent(w=True)

def prepare_geo(smooth=True, projectUV=True, scaleUV=True):
    if smooth:
        cmds.polySoftEdge(a=80, ch=False) 
    if projectUV:
        cmds.polyProjection(cmds.ls(sl=True)[0]+'.f[*]', ch=False, type='Planar', ibd=True, isu=scaleUV, isv=scaleUV, md='y')

def UI(obj):
    win = cmds.window(t='Separate '+obj)
    form = cmds.formLayout()
    triLimit = cmds.textFieldGrp('triLimit', label='tri-count limit per part:', text='5000' )
    smoothCmd = 'cmds.textFieldGrp("smoothValue", e=True, enable=cmds.checkBox("smooth", value=True, q=True))'
    smooth = cmds.checkBox('smooth', label='smooth normals', value=False, cc=smoothCmd)
    smoothValue = cmds.textFieldGrp('smoothValue', label='smooth Value:', text='80', enable=False)
    projectCmd = 'cmds.textFieldGrp("scaleUV", e=True, enable=cmds.checkBox("project", value=True, q=True))'
    projectUV = cmds.checkBox('project', label='project UV on Y', value=False, cc=projectCmd)
    scaleUV = cmds.textFieldGrp('scaleUV', label='UV scale:', text='1.0', enable=False)
    keepOriginal = cmds.checkBox('keepOriginal', label='keep original mesh', value=False)
    okButton = cmds.button('okbutton',
                    label="Go!",
                    c=start,
                    annotation='Generate Nuke script from selected items')
    cancelButton = cmds.button('cancelbutton',
                    label="Cancel",
                    c='cmds.deleteUI(win)',
                    annotation='Close the mayaToNuke interface - Have a nice day -')
    tab = 150
    cmds.formLayout(form, e=True, attachForm = 
                        [
                            (triLimit, 'top', 5),
                            (triLimit, 'left', 5),
                            (triLimit, 'right', 5),
                            (smooth, 'left', tab),
                            (smooth, 'right', 5),
                            (smoothValue, 'left', 5),
                            (smoothValue, 'right', 5),
                            (projectUV, 'left', tab),
                            (projectUV, 'right', 5),
                            (scaleUV, 'left', 5),
                            (scaleUV, 'right', 5),
                            (keepOriginal, 'left', tab),
                            (okButton, 'left', 5),
                            (okButton, 'bottom', 5),
                            (cancelButton, 'right', 5),
                            (cancelButton, 'bottom', 5),
    
                        ],
                                    attachControl = 
                        [
                            (smooth, 'top', 5, triLimit),
                            (smoothValue, 'top', 5, smooth),
                            (projectUV, 'top', 5, smoothValue),
                            (scaleUV, 'top', 5, projectUV),
                            (keepOriginal, 'top', 5, scaleUV),
                        ],
                                    attachPosition = 
                        [
                            (okButton, "right", 5, 50),
                            (cancelButton, "left", 5, 50)
                        ]
                        )
    cmds.showWindow()

def start(none=None):
    # get values
    triLimit = int(cmds.textFieldGrp('triLimit', text=True, q=True))
    projectUV = cmds.checkBox('checkbox', value=True, q=True)
    scaleUV = float(cmds.textFieldGrp('scaleUV', text=True, q=True))
    keepOriginal = cmds.checkBox('keepOriginal', value=True, q=True)
    # prepare geo
    if keepOriginal:
        cmds.duplicate()
    original = cmds.ls(sl=True)[0]
    prepare_geo(projectUV=projectUV, scaleUV=scaleUV)
    # extract parts
    nodes = {}
    loop=True
    iteration = 0
    while loop:
        try:
            nodes[iteration] = extract(cmds.ls(sl=True)[0], triLimit)
        except:
            loop=False
        iteration += 1
    # clean
    clean_parts(nodes)
    # delete empty group
    cmds.delete(original)
        
if __name__ == '__main__':
    if cmds.ls(sl=True):
        UI(cmds.ls(sl=True)[0])
