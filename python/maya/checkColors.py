import maya.cmds as cmds

class CheckColors(object):
    def __init__(self):
        pass

    def getColors(self, selection):
        colors = {}
        for obj in selection:
            try:
                colors[obj] = {}
                for v in range(cmds.polyEvaluate(obj, v=True)):
                    cmds.select(obj+'.vtx['+str(v)+']', r=True)
                    colors[obj][v] = cmds.polyColorPerVertex(query=True,
                                                             r=True,
                                                             g=True,
                                                             b=True)
            except:
                pass 
        cmds.select(selection, r=True)
        
        return colors

    def checkBadMeshes(self, colors={}):
        
        badMeshes = []
        for c in colors:
            for val in colors[c].values():
                if 1.0 in val:
                    print c
                    mesh = [key for key in colors.keys() if colors[key] == colors[c]]
                    if mesh:
                        badMeshes.append(mesh)
                    break

        return badMeshes

    def selectNode(self, none=None):
        node = cmds.textScrollList('textScroll', selectItem=True, q=True)
        try:
            cmds.select(node, r=True)
        except:
            pass

    def UI(self, meshes=[]):
        if cmds.window('CheckColorVertex', exists=True):
            cmds.deleteUI('CheckColorVertex', window=True)
        
        win = cmds.window('CheckColorVertex', t='Check Color Vertex')
        cmds.paneLayout()
        cmds.textScrollList('textScroll',
                            numberOfRows=8,
                            allowMultiSelection=True,
                            selectCommand=self.selectNode,
                            append=[str(mesh) for mesh in meshes])
        cmds.showWindow()

def main():
    cmds.select(hi=True)
    selection = cmds.ls(sl=True)
    if selection:
        checkColors = CheckColors()
        colors = checkColors.getColors(selection)
        badMeshes = checkColors.checkBadMeshes(colors)

        if badMeshes:
            checkColors.UI(badMeshes)
        else:
            confirm = cmds.confirmDialog(t = "Hey!",
                                         m = 'There is no mesh with white color vertex.')    
if __name__ == '__main__':
    main()