# hotkeys list
HOTKEYS = \
[
    {
        'name':'softEdgeSelection',
        'key':'N',
        'alt':True,
        'ctrl':False,
        'release':False,
        'command':'python("import dmptools.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.softEdgeSelection()");'
    },
    {
        'name':'invertSelection',
        'key':'I',
        'alt':False,
        'ctrl':True,
        'release':False,
        'command':'python("import dmptools.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.invertSelection()");'
    },
    {
        'name':'showHotkeysList',
        'key':'H',
        'alt':True,
        'ctrl':False,
        'release':False,
        'command':'python("import dmptools.createHotkeys as createHotkeys;\
            reload(createHotkeys);createHotkeys.showHotkeysList()");'
    },
    {
        'name':'createHotkeys',
        'key':'H',
        'alt':True,
        'ctrl':True,
        'release':False,
        'command':'python("import dmptools.createHotkeys as createHotkeys;\
            reload(createHotkeys);createHotkeys.main()");'
    },
    {
        'name':'bufMove',
        'key':'a',
        'alt':False,
        'ctrl':False,
        'release':True,
        'command':'python("import dmptools.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.bufMove()");',
        'releaseCommand':'python("import dmptools.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.bufMoveRelease()");'
    },
    {
        'name':'bufMoveMulti',
        'key':'q',
        'alt':False,
        'ctrl':False,
        'release':True,
        'command':'python("import dmptools.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.bufMoveMulti()");',
        'releaseCommand':'python("import dmptools.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.bufMoveRelease()");'
    },
    {
        'name':'hideSelectionSwitch',
        'key':'h',
        'alt':False,
        'ctrl':False,
        'release':False,
        'command':'python("import dmptools.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.hideSelSwitch()");'
    },
    {
        'name':'isolateSelection',
        'key':'h',
        'alt':True,
        'ctrl':False,
        'release':False,
        'command':'python("import dmptools.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.isolateSelection()");',
    },
    {
        'name':'toggleNormals',
        'key':'n',
        'alt':True,
        'ctrl':False,
        'release':False,
        'command':'python("import dmptools.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.toggleNormals()");',
    },
    {
        'name':'setWireframe',
        'key':'w',
        'alt':True,
        'ctrl':False,
        'release':False,
        'command':'python("import dmptools.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.setWireframe()");',
    },
    {
        'name':'setBackfaceCulling',
        'key':'B',
        'alt':True,
        'ctrl':False,
        'release':False,
        'command':'python("import dmptools.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.setBackfaceCulling()");',
    },
    {
        'name':'setDefaultMaterial',
        'key':'d',
        'alt':True,
        'ctrl':False,
        'release':False,
        'command':'python("import dmptools.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.setDefaultMaterial()");',
    },
    {
        'name':'cameraPanTool',
        'key':'z',
        'alt':True,
        'ctrl':False,
        'release':False,
        'command':'python("import dmptools.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.cameraPanTool()");',
    },
    {
        'name':'cameraZoomTool',
        'key':'Z',
        'alt':True,
        'ctrl':False,
        'release':False,
        'command':'python("import dmptools.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.cameraZoomTool()");',
    },
    {
        'name':'resetPanZoom',
        'key':'Z',
        'alt':True,
        'ctrl':True,
        'release':False,
        'command':'python("import dmptools.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.resetPanZoom()");',
    },
    {
        'name':'selectNgones',
        'key':'q',
        'alt':True,
        'ctrl':False,
        'release':False,
        'command':'python("import dmptools.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.switchSelectNgones()");',
    },
    {
        'name':'selectTriangles',
        'key':'p',
        'alt':True,
        'ctrl':False,
        'release':False,
        'command':'python("import dmptools.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.switchSelectTriangles()");',
    },
    {
        'name':'switchLight',
        'key':'l',
        'alt':True,
        'ctrl':False,
        'release':False,
        'command':'python("import dmptools.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.switchLight()");'
    },
    {
        'name':'switchHighlightedSelection',
        'key':'f',
        'alt':True,
        'ctrl':False,'release':False,
        'command':'python("import dmptools.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.switchHighlightedSelection()");'
    },
    {
        'name':'askFlushUndo',
        'key':'f',
        'alt':False,
        'ctrl':True,
        'release':False,
        'command':'python("import dmptools.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.askFlushUndo()");'
    },
    {
        'name':'saveAs',
        'key':'S',
        'alt':False,
        'ctrl':True,
        'release':False,
        'command':'SaveSceneAs;'
    },
    {
        'name':'freezeHistory',
        'key':'F',
        'alt':True,
        'ctrl':False,
        'release':False,
        'command':'python("import dmptools.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.freezeHistory()");'
    },
    {
        'name':'freezeHistoryCenterPivot',
        'key':'F',
        'alt':True,
        'ctrl':True,
        'release':False,
        'command':'python("import dmptools.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.freezeCenterPivot()");'
    },
    {
        'name':'centerPivot',
        'key':'F',
        'alt':False,
        'ctrl':True,
        'release':False,
        'command':'python("import dmptools.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.centerPivot()");'
    },
    {
        'name':'setDefaultRenderer',
        'key':'1',
        'alt':True,
        'ctrl':False,
        'release':False,
        'command':'python("import dmptools.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.setDefaultRenderer()");'
    },
    {
        'name':'setHardwareRenderer',
        'key':'2',
        'alt':True,
        'ctrl':False,
        'release':False,
        'command':'python("import dmptools.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.setHardwareRenderer()");'
    },
    {
        'name':'setViewport2Renderer',
        'key':'3',
        'alt':True,
        'ctrl':False,
        'release':False,
        'command':'python("import dmptools.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.setViewport2Renderer()");'
    },
    {
        'name':'launchConsole',
        'key':'x',
        'alt':True,
        'ctrl':False,
        'release':False,
        'command':'python("import dmptools.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.launchConsole()");'
    },
    {
        'name':'mergeVertex',
        'key':'m',
        'alt':False,
        'ctrl':True,
        'release':False,
        'command':'python("import dmptools.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.mergeVertex()");'
    },
    {
        'name':'openUvTextureEditor',
        'key':'1',
        'alt':True,
        'ctrl':True,
        'release':False,
        'command':'python("import dmptools.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.openUvTextureEditor()");'
    },
    {
        'name':'openHypershade',
        'key':'2',
        'alt':True,
        'ctrl':True,
        'release':False,
        'command':'python("import dmptools.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.openHypershade()");'
    },
    {
        'name':'proMode',
        'key':'F11',
        'alt':False,
        'ctrl':False,
        'release':False,
        'command':'python("import dmptools.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.proMode()");'
    },
    {
        'name':'unselectAll',
        'key':'space',
        'alt':False,
        'ctrl':True,
        'release':False,
        'command':'python("import dmptools.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.unselectAll()");'
    },
    {
        'name':'switchObjectTumble',
        'key':'Q',
        'alt':True,
        'ctrl':False,
        'release':False,
        'command':'python("import dmptools.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.switchObjectTumble()");'
    },
    {
        'name':'toggleVertexColorDisplay',
        'key':'C',
        'alt':True,
        'ctrl':False,
        'release':False,
        'command':'python("import dmptools.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.toggleVertexColorDisplay()");'
    },
    {
        'name':'shortestEdgePath',
        'key':'a',
        'alt':True,
        'ctrl':False,
        'release':True,
        'command':'python("import dmptools.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.shortestEdgePath()");',
        'releaseCommand':'python("import dmptools.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.shortestEdgePathRelease()");'
    },
    {
        'name':'mergeUVs',
        'key':'X',
        'alt':False,
        'ctrl':True,
        'release':False,
        'command':'python("import dmptools.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.mergeUVs()");'
    },
]
# end of hotkeys