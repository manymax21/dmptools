import maya.cmds as cmds
import maya.mel as mel

# source dead space combine script
mel.eval('source "D:/tools_pf/maya/mel/MODEL_vgm_combine.mel";')

fileName = cmds.file(q=True, sceneName=True)

selection = cmds.ls(sl=True)
if selection:
    cmds.file(save=True, force=True)
    assetName = selection[0].split("_")[0]
    outputPath = "D:/projects/AO4FB/Dev/Data/Raw/DSX_levels/Mesh/"+assetName+".fbx"
    outputPath = "C:/Users/mhavart/Documents/maya/projects/default/scenes/ds4/"+assetName+".fbx"

    asset = selection[0]
    assetParent = cmds.listRelatives(asset)
    main = assetParent[0]
    collision = assetParent[1]
    # mesh
    lodGroup = cmds.listRelatives(main)[0]
    lodGroupFullName = cmds.listRelatives(main, fullPath=True)[0]
    meshGroups = cmds.listRelatives(lodGroup, fullPath=True)
    for item in meshGroups:
        cmds.select(item, replace=True)
        mel.eval('MODEL_vgm_combine();')
        cmds.rename(assetName)
        cmds.parent(cmds.ls(sl=True), lodGroupFullName)
        cmds.delete(item)
    #export
    cmds.select(asset, r=True)
    cmds.file(outputPath, force=True, options="v=0", typ="FBX export", pr=True, es=True)
    # reopen original file
    #cmds.file(fileName, force=True, options="v=0", typ="mayaAscii", o=True)
else:
    cmds.warning('please select the asset you want to export!')